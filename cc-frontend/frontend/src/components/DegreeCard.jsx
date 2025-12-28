import { useNavigate } from "react-router-dom";
import "../css/DegreeCard.css";
import { Link } from "react-router-dom";

function DegreeCard({ degree }) {
    const navigate = useNavigate();
    return (
        // We remove the Link wrapping the whole card for better accessibility
        // and rely on a dedicated "View" button/link inside.
        <div className="degree-card">
            <div className="degree-card-header">
                <div className="degree-id-container">
                    <span className="degree-id">{degree.degree_id}</span>
                </div>
                <div className="degree-info">
                    <h3 className="degree-title">{degree.discipline}</h3>
                    <span className="degree-level">{degree.level}</span>
                </div>
            </div>

            {degree.description && (
                <p className="degree-card-description">
                    {degree.description}
                </p>
            )}

            <Link to={`/degrees/${degree.slug}`} className="view-degree-link">
                View Full Roadmap
            </Link>
        </div>
    );
}
export default DegreeCard;