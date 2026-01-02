import { useState } from "react";
import { registerRequest } from "../services";
import { useNavigate, Link } from "react-router-dom";

// Không dùng CSS Modules
const Register = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            await registerRequest(username, password, email);

            navigate("/login", { replace: true });
        } catch (error) {
            alert(error);
        }
    };

    return (
        <>
            <h2>Create Account</h2>
            <form method="POST" onSubmit={handleSubmit}>
                <div className="formGroup">
                    <label htmlFor="username">Username</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Username"
                        required
                    />
                </div>

                <div className="formGroup">
                    <label htmlFor="email">Email</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email"
                        required
                    />
                </div>

                <div className="formGroup">
                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                    />
                </div>

                <button type="submit">Register</button>
            </form>
            <p className="registerLink">Already have an account? <Link to="/login">Login</Link></p>
        </>
    );
};

export default Register;
