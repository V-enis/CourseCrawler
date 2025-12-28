import { useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { fetchDegreeBySlug } from '../queries';
import { toast } from 'react-hot-toast';
import { useQueryClient } from '@tanstack/react-query';
import api from '../api';
import Course from '../components/Course';
import "../css/DegreeDetail.css";
import "../css/Course.css";

function DegreeDetail() {
    const queryClient = useQueryClient();
    const { slug } = useParams();
    const navigate = useNavigate();

    const {
        data: degree,
        isLoading,
        isError,
        error
    } = useQuery({
        queryKey: ['degree', slug],
        queryFn: fetchDegreeBySlug,
    });

    const handleEnroll = async () => {
        try {
            const response = await api.post(`degrees/${slug}/enroll/`);

            if (response.status === 201) {
                toast.success('Successfully enrolled!');
                await queryClient.invalidateQueries({ queryKey: ['myEnrollments'] });
                navigate('/dashboard');
            }
            else if (response.status === 200) {
                toast('You are already enrolled in this degree.');
            }
        } catch (err) {
            if (err.response?.status === 401) {
                toast.error('Please log in to enroll.');
            } else {
                toast.error('An unexpected error occurred. Please try again.');
                console.error("Enrollment error:", err);
            }
        }
    };

    const semestersByYear = useMemo(() => {
        if (!degree?.semesters) return {};

        return degree.semesters.reduce((groups, semester) => {
            const year = semester.year;
            if (!groups[year]) {
                groups[year] = [];
            }
            groups[year].push(semester);
            return groups;
        }, {});
    }, [degree]);

    if (isLoading) {
        return <div style={{ maxWidth: '900px', margin: 'auto', paddingBottom: '50px' }}>Loading...</div>;
    }

    if (isError) {
        return <div style={{ maxWidth: '900px', margin: 'auto', paddingBottom: '50px' }}>Error: {error.message}</div>;
    }

    return (
        <div className="degree-detail-pg" style={{ maxWidth: '900px', margin: 'auto', paddingBottom: '50px' }}>
            <header style={{ marginBottom: '40px', marginTop: '40px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                        <h1 style={{ fontSize: '3rem', textTransform: 'uppercase' }}>{degree.discipline}</h1>
                        <h2 style={{ color: '#8b949e' }}>{degree.level}</h2>
                    </div>
                    <button onClick={handleEnroll} className="cta-button" style={{ fontSize: '0.9rem' }}>
                        Enroll Now
                    </button>
                </div>
                {degree.description && (
                    <p className="degree-detail-description">{degree.description}</p>
                )}
                <hr className="divider" style={{ margin: '2rem 0' }} />
            </header>

            <div className="degree-structure">
                {Object.keys(semestersByYear).sort().map((year) => (
                    <div key={year} className="year-section">
                        <div className="year-number">Year {year}</div>
                        <div className="year-content">
                            {semestersByYear[year].sort((a, b) => a.number - b.number).map((semester) => (
                                <div key={semester.id} className="semester">
                                    <div className="semester-number">
                                        Semester {semester.number} {semester.theme && `- ${semester.theme}`}
                                    </div>
                                    <div className="semester-courses">
                                        <ul>
                                            {semester.courses.map((course) => (
                                                <li key={course.id}>
                                                    <Course course={course} />
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default DegreeDetail;