import { useEffect, useState, useRef } from "react";
import api from "../api";
import DegreeCard from "../components/DegreeCard";
import "../css/LandingPage.css";

function LandingPage() {
    const [degrees, setDegrees] = useState([]);
    const listRef = useRef(null); // Reference to scroll to

    useEffect(() => {
        // Fetch degrees for the list at bottom
        api.get('degrees/').then(res => setDegrees(res.data));
    }, []);

    const scrollToDegrees = () => {
        listRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    return (
        <main className="landingpage-content">
            <div className="head">
                <div className="description-container">
                    <img src="/art.png" className="site-art" alt="Art" />
                    <div className="description">
                        <h1 className="title-hook">A Guided Path Through Open Knowledge</h1>
                        <p className="title-description">University-level knowledge is more accessible than ever, yet a clear educational path is often missing. Inspired by the proven structure of accredited degree programs, this application serves as a bridge. It programmatically connects official syllabi to the wealth of open courseware, generating a guided curriculum for the dedicated self-learner.</p>
                        <button className="cta-button" onClick={scrollToDegrees}>Browse Degrees</button>
                    </div>
                </div>
            </div>

            <hr className="divider"></hr>

            <div className="degree-grid" ref={listRef}>
                {degrees.map(d => (
                    <DegreeCard
                        key={d.id}
                        degree={d}
                        description={d.exit_requirements || "A rigorous academic track."}
                    />
                ))}
            </div>
        </main>
    );
}
export default LandingPage;