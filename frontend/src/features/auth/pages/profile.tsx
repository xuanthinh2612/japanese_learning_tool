import { useEffect, useState } from "react";
import api from "@/services/service";
import styles from "../components/auth.module.css";
import { useNavigate } from "react-router-dom";


type ProfileResponse = {
  user: string;
};

const Profile = () => {
  const [user, setUser] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.get<ProfileResponse>("/profile");
        setUser(res.data.user);
      } catch (err) {
        setError("Không thể lấy thông tin người dùng");
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login", { replace: true });
  };
  
  if (loading) {
    return <div className={styles.container}>Loading...</div>;
  }

  if (error) {
    return <div className={styles.container}>{error}</div>;
  }

  return (
    <div className={styles.container}>
      <div className={styles.form}>
        <h2>👤 Profile</h2>
        <p>
          <strong>Username:</strong> {user}
        </p>
        <button onClick={handleLogout}>🚪 Logout</button>
      </div>
    </div>
  );
};

export default Profile;
