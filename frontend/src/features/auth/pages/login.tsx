import { useState } from "react";
import api from "@/services/service";
import styles from "../components/auth.module.css";
import clsx from "clsx";
import { useNavigate } from "react-router-dom";


const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();


    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            const res = await api.post("/login", {
                username,
                password,
            });

            localStorage.setItem("token", res.data.access_token);
            navigate("/profile", { replace: true });
        } catch (error) {
            alert("Login failed");
        }
    };

    return (
        <div className={clsx(styles.container)}>
            <form className={clsx(styles.form)} onSubmit={handleSubmit}>
                <input
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                />
                <button type="submit">Login</button>
            </form>
        </div>
    );

};

export default Login;
