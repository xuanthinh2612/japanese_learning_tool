import { createContext, useContext, useState, useEffect } from "react";
import { getProfileRequest } from "../services";

type AuthUser = {
    username: string;
};

type AuthContextType = {
    user: AuthUser | null;
    setUser: (user: AuthUser | null) => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<AuthUser | null>(null);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const res = await getProfileRequest();
                const profileData = res.data as AuthUser;  
                setUser(profileData);
            } catch {
                setUser(null);
            }
        };

        if (localStorage.getItem("token")) {
            fetchProfile();
        }
    }, []);

    return (
        <AuthContext.Provider value={{ user, setUser }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
    return ctx;
};
