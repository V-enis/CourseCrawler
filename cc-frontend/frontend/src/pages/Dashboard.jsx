import { useQuery } from '@tanstack/react-query';
import { fetchMyEnrollments } from '../queries';
import DegreeCard from '../components/DegreeCard';
import "../css/Dashboard.css";
import "../css/DegreeList.css";

const MainContent = ({ children }) => (
    <div className="main-content">{children}</div>
);

function Dashboard() {
    // Use the useQuery hook to manage fetching and caching.
    const {
        data: enrollments,
        isLoading,
        isError,
        error
    } = useQuery({
        queryKey: ['myEnrollments'],
        queryFn: fetchMyEnrollments,
    });

    if (isLoading) {
        return <MainContent><h1>Loading Your Dashboard...</h1></MainContent>;
    }

    if (isError) {
        return (
            <MainContent>
                <h1 className="dashboard-title">My Learning Dashboard</h1>
                <p className="no-enrollments">Please log in to view your enrollments.</p>
            </MainContent>
        );
    }

    return (
        <MainContent>
            <h1 className="dashboard-title">My Learning Dashboard</h1>

            {enrollments && enrollments.length > 0 ? (
                <div className="degree-grid">
                    {/* The API returns Enrollment objects, which have a 'degree' nested inside */}
                    {enrollments.map((enrollment) => (
                        <DegreeCard key={enrollment.id} degree={enrollment.degree} />
                    ))}
                </div>
            ) : (
                <p className="no-enrollments">You haven't enrolled in any degrees yet. Go find one!</p>
            )}
        </MainContent>
    );
}

export default Dashboard;