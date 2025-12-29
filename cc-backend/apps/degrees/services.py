import os
import requests
import re
import time
from django.conf import settings
from pgvector.django import L2Distance

from apps.syllabus.models import CollegeDegree, CollegeCourse
from apps.courses.models import Course
from apps.degrees.models import Degree, Semester

from apps.ml.services import get_embedding_model 

class DegreeGenerator:
    """
    A service to generate a Degree roadmap by matching a CollegeDegree syllabus
    against the available online Course catalog using a RAG pipeline.
    
    UPDATED FOR CLOUD DEPLOYMENT (Hugging Face Serverless API)
    """
    def __init__(self, college_degree_id: int):
        try:
            self.source_syllabus = CollegeDegree.objects.get(id=college_degree_id)
        except CollegeDegree.DoesNotExist:
            raise ValueError("A CollegeDegree with the specified ID does not exist.")
        
        # Load the LLM API URL and Token from Django settings
        self.llm_api_url = settings.HF_INFERENCE_ENDPOINT_URL
        self.hf_token = settings.HF_TOKEN # New: Needed for Cloud API
        self.generated_degree = None

    def _find_candidate_courses(self, syllabus_course: CollegeCourse, used_course_ids: list, num_candidates=5) -> list[Course]:
        """
        STEP 1: Vector Search (Retrieval).
        Finds the top N candidate courses, excluding any courses that have already been
        selected for this degree plan.
        """
        # Lazy-load the embedding model
        embedding_model = get_embedding_model()
        
        text_to_embed = f"{syllabus_course.title}. {syllabus_course.description}"
        syllabus_embedding = embedding_model.encode(text_to_embed)
        
        # Start with a base query for all courses that have an embedding.
        base_query = Course.objects.filter(embedding__isnull=False)
        
        # Exclude courses that are already in our "used" list for this degree.
        if used_course_ids:
            base_query = base_query.exclude(pk__in=used_course_ids)
        
        # Annotate with distance, order by it, and take the top N candidates.
        candidates = base_query.annotate(
            distance=L2Distance('embedding', syllabus_embedding)
        ).order_by('distance')[:num_candidates]
        
        return list(candidates)

    def _select_best_course_with_llm(self, syllabus_course: CollegeCourse, candidates: list[Course], completed_courses: list[str]) -> Course:
        """
        STEP 2: LLM Reasoning (Generation).
        Selects the best candidate using the Hugging Face Serverless API.
        """
        if not self.llm_api_url or not self.hf_token:
            print("Warning: HF_INFERENCE_ENDPOINT_URL or HF_TOKEN not set. Falling back to top vector result.")
            return candidates[0]

        candidate_map = {c.id: c for c in candidates}
        
        completed_courses_text = "- " + "\n- ".join(completed_courses) if completed_courses else "None yet."

        # Prompt engineering for Phi-3 / Mistral / Llama
        prompt = f"""<|user|>
You are an expert academic advisor. Select the single best online course from the list below to fulfill the given syllabus requirement.
You MUST consider the prerequisite context. The student has already completed the courses listed under "Completed Courses."
Choose a candidate that is a good topical match AND for which the prerequisites seem to be met by the completed courses.
Respond ONLY with the numeric ID of the winning course. If none of the candidates are a good fit, respond with "ID: 0".

**Syllabus Requirement:**
- Title: "{syllabus_course.title}"
- Description: "{syllabus_course.description}"

**Completed Courses:**
{completed_courses_text}

**Candidate Online Courses:**
"""
        for i, candidate in enumerate(candidates):
            prereqs = f"Prerequisites: {candidate.prerequisites}" if candidate.prerequisites else "Prerequisites: None listed."
            prompt += f"\n{i+1}. **{candidate.title}** (ID: {candidate.id})\n   - Provider: {candidate.provider}\n   - {prereqs}"
        
        prompt += """
<|end|>
<|assistant|>
"""
        
        # --- CLOUD API CONFIGURATION ---
        headers = {
            "Authorization": f"Bearer {self.hf_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 50,     # Small number to save time/tokens
                "temperature": 0.1,       # Low temperature = strict, logical answers
                "return_full_text": False # CRITICAL: Do not repeat the prompt in the output
            }
        }

        # Retry logic for model loading (Cold Boot)
        for attempt in range(3):
            try:
                print(f"     > Sending request to LLM API (Attempt {attempt+1})...")
                response = requests.post(self.llm_api_url, headers=headers, json=payload, timeout=30)
                
                # Check for "Model Loading" state (common on free tier)
                if response.status_code == 503:
                    estimated_time = response.json().get("estimated_time", 20)
                    print(f"     ! Model is loading. Waiting {estimated_time} seconds...")
                    time.sleep(estimated_time)
                    continue # Try again

                response.raise_for_status()
                result = response.json()
                
                # Parse response
                # HF returns list: [{'generated_text': 'ID: 105'}]
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                else:
                    generated_text = str(result)

                print(f"     > Raw LLM Output: '{generated_text.strip()}'")

                # Regex to find the ID
                match = re.search(r'\d+', generated_text)
                if match:
                    winning_id = int(match.group(0))
                    
                    if winning_id == 0:
                        print("     ! LLM indicated no good fit. Falling back to top vector result.")
                        return candidates[0]
                    
                    winner = candidate_map.get(winning_id)
                    if winner:
                        print(f"     < LLM selected Course ID: {winning_id} ('{winner.title}')")
                        return winner
                    else:
                        print(f"     ! LLM hallucinated ID {winning_id}. Falling back to top vector result.")
                        return candidates[0]
                else:
                    print("     ! LLM response did not contain a numeric ID. Falling back.")
                    return candidates[0]

            except Exception as e:
                print(f"     ! LLM selection failed: {e}. Falling back to top vector search result.")
                return candidates[0]
        
        # If we exit the loop, all attempts failed
        return candidates[0]

    def generate_roadmap(self):
        """
        The main orchestration method that runs the entire pipeline.
        """
        print(f"--- Starting roadmap generation for '{self.source_syllabus.title}' ---")
        
        self.generated_degree, created = Degree.objects.update_or_create(
            degree_id=self.source_syllabus.degree_id,
            defaults={
                'discipline': self.source_syllabus.title, 
                'level': self.source_syllabus.level,
                'description': self.source_syllabus.overview,
                'exit_requirements': self.source_syllabus.exit_requirements,
            }
        )
        if not created:
            self.generated_degree.semesters.all().delete()
        print(f"Created/updated generated Degree object with ID: {self.generated_degree.id}")

        selected_course_titles = []
        used_course_ids = []

        for year_obj in self.source_syllabus.years.all().order_by('number'):
            for semester_obj in year_obj.semesters.all().order_by('number'):
                new_semester = Semester.objects.create(
                    degree=self.generated_degree,
                    year=year_obj.number,
                    number=semester_obj.number,
                    theme=semester_obj.theme
                )
                print(f"\nProcessing: Year {year_obj.number}, Semester {semester_obj.number}")

                for syllabus_course in semester_obj.courses.all():
                    print(f"  -> Matching syllabus course: '{syllabus_course.title}'")
                    
                    candidates = self._find_candidate_courses(syllabus_course, used_course_ids)

                    if not candidates:
                        print(f"     ! No unique candidates found for '{syllabus_course.title}'. Skipping.")
                        continue

                    best_course = self._select_best_course_with_llm(syllabus_course, candidates, selected_course_titles)
                    
                    new_semester.courses.add(best_course)
                    
                    selected_course_titles.append(best_course.title)
                    used_course_ids.append(best_course.id)
                    
                    print(f"  ++ Added matched course: '{best_course.title}' (ID: {best_course.id})")
        
        print("\n--- Roadmap generation complete! ---")
        return self.generated_degree