import { useQuery } from '@tanstack/react-query';
import { fetchDegrees } from '../queries';
import DegreeCard from '../components/DegreeCard';
import "../css/DegreeList.css";

const MainContent = ({ children }) => (
    <div className="main-content">{children}</div>
);

export default function DegreeList() {
    const { data: degrees, isLoading, isError, error } = useQuery({
        queryKey: ['degrees'],
        queryFn: fetchDegrees,
    });

    if (isLoading) {
        return (
            <MainContent>
                <h1>Loading Degrees...</h1>
            </MainContent>
        );
    }

    if (isError) {
        return (
            <MainContent>
                <h1>Error fetching degrees: {error.message}</h1>
            </MainContent>
        );
    }

    return (
        <MainContent>
            <h1>All Degrees</h1>
            <div className="degree-grid">
                {degrees?.map(degree => (
                    <DegreeCard key={degree.id} degree={degree} />
                ))}
            </div>
        </MainContent>
    );
}