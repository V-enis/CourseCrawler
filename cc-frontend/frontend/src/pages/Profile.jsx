import { useEffect, useState } from "react";
import api from "../api";
import "../css/Profile.css";

function Profile() {
    const [user, setUser] = useState({ name: "", email: "", username: "" });
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        getProfile();
    }, []);

    const getProfile = async () => {
        try {
            const res = await api.get("auth/profile/");
            setUser(res.data);
        } catch (err) {
            alert("Failed to load profile.");
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            // We only send name and email, as username is read-only
            await api.patch("auth/profile/", {
                name: user.name,
                email: user.email
            });
            alert("Profile updated successfully!");
        } catch (err) {
            alert("Error updating profile.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="profile-container">
            <header className="profile-header">
                <img src="/profile.png" className="profile-avatar-large" alt="Profile" />
                <h1>{user.username}</h1>
            </header>

            <form onSubmit={handleSubmit} className="profile-form">
                <div className="form-group">
                    <label>Full Name</label>
                    <input
                        className="profile-input"
                        type="text"
                        value={user.name}
                        onChange={(e) => setUser({ ...user, name: e.target.value })}
                        placeholder="Enter your name"
                    />
                </div>

                <div className="form-group">
                    <label>Email Address</label>
                    <input
                        className="profile-input"
                        type="email"
                        value={user.email}
                        onChange={(e) => setUser({ ...user, email: e.target.value })}
                        placeholder="name@example.com"
                    />
                </div>

                <button className="save-button" type="submit" disabled={loading}>
                    {loading ? "Saving..." : "Save Changes"}
                </button>
            </form>
        </div>
    );
}

export default Profile;