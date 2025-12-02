import os
import requests
import re
from django.conf import settings
from sentence_transformers import SentenceTransformer
from pgvector.django import L2Distance

from apps.syllabus.models import CollegeDegree, CollegeCourse
from apps.courses.models import Course
from apps.degrees.models import Degree, Semester


print("Loading embedding model for DegreeGenerator service...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("Embedding model loaded.")

class DegreeGenerator:
    """
    A service to generate a Degree roadmap by matching a CollegeDegree syllabus
    against the available online Course catalog.
    """
    def __init__(self, college_degree_id: int):
        try:
            self.source_syllabus = CollegeDegree.objects.get(id=college_degree_id)
        except CollegeDegree.DoesNotExist:
            raise ValueError("A CollegeDegree with the specified ID does not exist.")
        
        self.llm_api_url = settings.HF_INFERENCE_ENDPOINT_URL
        self.generated_degree = None


    def _find_candidate_courses(self, syllabus_course: CollegeCourse, num_candidates=5) -> list[Course]:
        """
        STEP 1: Vector Search. Finds the top N candidate courses.
        """
        text_to_embed = f"{syllabus_course.title}. {syllabus_course.description}"
        syllabus_embedding = embedding_model.encode(text_to_embed)
        
        # Query the database for courses with embeddings, order by similarity (distance)
        candidates = Course.objects.filter(embedding__isnull=False).annotate(
            distance=L2Distance('embedding', syllabus_embedding)
        ).order_by('distance')[:num_candidates]
        
        return list(candidates)

    def _select_best_course_with_llm(self, syllabus_course: CollegeCourse, candidates: list[Course]) -> Course:
        """
        STEP 2: LLM Reasoning. Selects the best candidate using the local LLM API.
        """
        if not self.llm_api_url:
            print("Warning: HF_INFERENCE_ENDPOINT_URL not set. Falling back to top vector result.")
            return candidates[0]

        candidate_map = {c.id: c for c in candidates}
        
        # This prompt format is for Phi-3 and Mistral. It guides the model to the desired output.
        prompt = f"""<|user|>
You are an expert academic advisor building a curriculum. Select the single best online course from the list below to fulfill the given syllabus requirement.
Respond ONLY with the numeric ID of the winning course and nothing else.

**Syllabus Requirement:**
- Title: "{syllabus_course.title}"
- Description: "{syllabus_course.description}"

**Candidate Online Courses:**
"""
        for i, candidate in enumerate(candidates):
            prompt += f"\n{i+1}. **{candidate.title}** (ID: {candidate.id})\n   - Provider: {candidate.provider}\n   - Description: {candidate.description}"
        
        prompt += """<|end|>
<|assistant|>
"""
        
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": 10}}

        try:
            print(f"     > Sending request to LLM API at {self.llm_api_url}...")
            response = requests.post(self.llm_api_url, json=payload, timeout=120)
            response.raise_for_status() 
            result = response.json()
            generated_text = result[0]['generated_text']
            
            match = re.search(r'\d+', generated_text)
            if match:
                winning_id = int(match.group(0))
                if winning_id == 0: # no good fit case.
                    print("     ! LLM indicated no good fit. Falling back to top vector result.")
                    return candidates[0]
                winner = candidate_map.get(winning_id)
                if winner:
                    print(f"     < LLM selected Course ID: {winning_id} ('{winner.title}')")
                    return winner
                else:
                    raise ValueError(f"LLM returned ID {winning_id}, which was not in the candidate list.")
            else:
                raise ValueError("LLM response did not contain a numeric ID.")

        except (requests.exceptions.RequestException, KeyError, ValueError, IndexError) as e:
            print(f"     ! LLM selection failed: {e}. Falling back to the top vector search result.")
            return candidates[0]


    def generate_roadmap(self):
        """
        The main orchestration method that runs the entire pipeline.
        """
        print(f"--- Starting roadmap generation for '{self.source_syllabus.title}' ---")
        
        self.generated_degree, created = Degree.objects.update_or_create(
            degree_id=f"GEN_{self.source_syllabus.degree_id}",
            defaults={
                'discipline': self.source_syllabus.title,
                'level': self.source_syllabus.level,
                'exit_requirements': self.source_syllabus.exit_requirements
            }
        )
        # Clear any old data if we are regenerating this degree
        if not created:
            self.generated_degree.semesters.all().delete()
        print(f"Created/updated generated Degree object with ID: {self.generated_degree.id}")

        # Loop through the source syllabus structure (years, semesters, courses)
        for year_obj in self.source_syllabus.years.all().order_by('number'):
            for semester_obj in year_obj.semesters.all().order_by('number'):
                new_semester = Semester.objects.create(
                    degree=self.generated_degree,
                    year=year_obj.number,
                    number=semester_obj.number,
                    theme=semester_obj.theme
                )
                print(f"\nProcessing: Year {year_obj.number}, Semester {semester_obj.number}")

                # For each course in the syllabus, find the best online match
                for syllabus_course in semester_obj.courses.all():
                    print(f"  -> Matching syllabus course: '{syllabus_course.title}'")
                    candidates = self._find_candidate_courses(syllabus_course)

                    if not candidates:
                        print(f"     ! No candidates found for '{syllabus_course.title}'. Skipping.")
                        continue

                    best_course = self._select_best_course_with_llm(syllabus_course, candidates)
                    
                    new_semester.courses.add(best_course)
                    print(f"  ++ Added matched course: '{best_course.title}'")
        
        print("\n--- Roadmap generation complete! ---")
        return self.generated_degree