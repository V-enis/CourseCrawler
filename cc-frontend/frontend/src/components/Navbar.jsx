import { Link, useNavigate, useLocation } from "react-router-dom";
import "../css/NavBar.css"
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

function NavBar() {
    const navigate = useNavigate();
    const location = useLocation();

    const isLoggedIn = !!localStorage.getItem(ACCESS_TOKEN);

    const handleLogout = () => {
        localStorage.removeItem(ACCESS_TOKEN);
        localStorage.removeItem(REFRESH_TOKEN);
        navigate("/login");
        queryClient.invalidateQueries({ queryKey: ['myEnrollments'] });
    };

    return (
        <>
            <div className="navbar-container">
                <div className="site-logo">
                    <img src="/LogoWD.png" className="logo-img" alt="Logo" />
                </div>

                <div className="navbar-links">
                    <Link to="/dashboard">Dashboard</Link>
                    <Link to="/degrees">Browse Degrees</Link>
                    <Link to="/about">About</Link>

                    <div className="auth-links">
                        {isLoggedIn ? (
                            // Show LOGOUT if logged in
                            <button onClick={handleLogout} className="nav-logout-btn">
                                Logout
                            </button>
                        ) : (
                            // Show LOGIN / REGISTER if logged out
                            <>
                                <Link to="/login">Login</Link>
                                <Link to="/register" className="nav-register-btn">Register</Link>
                            </>
                        )}
                    </div>
                </div>

                <div className="profile-info">
                    <a href="https://github.com/V-enis/CourseCrawler" target="_blank" rel="noreferrer">
                        <img src="/github-mark-white.png" className="github-logo" alt="Github" />
                    </a>
                    {isLoggedIn && (
                        <Link to="/profile">
                            <img src="/profile.png" className="profile-img" alt="Profile" />
                        </Link>
                    )}
                </div>
            </div>
        </>
    );
}

export default NavBar;