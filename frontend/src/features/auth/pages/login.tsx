import { useState } from "react";
import { loginRequest, getProfileRequest } from "../services/service.ts";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "@/features/auth/context/AuthContext";


// Không dùng styles từ module nữa
const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false); // Trạng thái loading
    const [error, setError] = useState(""); // Lưu trữ thông báo lỗi
    const navigate = useNavigate();
    const { setUser } = useAuth();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        // Kiểm tra đầu vào
        if (!username || !password) {
            setError("Both fields are required");
            return;
        }

        setLoading(true);
        setError(""); // Reset lỗi trước khi gửi yêu cầu

        try {
            const res = await loginRequest(username, password);

            // Lưu token và chuyển hướng
            localStorage.setItem("token", res.data.access_token);
            // gọi profile ngay
            const profile = await getProfileRequest();
            setUser(profile.data);

            navigate("/profile", { replace: true });
        } catch (error: any) {
            setError("Login failed. Please check your credentials and try again.");
        } finally {
            setLoading(false); // Dừng loading sau khi có kết quả
        }
    };

    return (
        <>
            <h2>Login</h2>
            <form method="POST" onSubmit={handleSubmit}>
                <div className="formGroup">
                    <label htmlFor="username">Username</label>
                    <input 
                        type="text" 
                        placeholder="Username" 
                        required     
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
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
                {error && <p className="error">{error}</p>} {/* Hiển thị lỗi */}

                <button type="submit" disabled={loading}>
                    {loading ? "Logging in..." : "Login"}
                </button>
            </form>
            <p className="registerLink">
                Don't have an account? <Link to="/register">Register</Link>
            </p>
        </>
    );
};

export default Login;
