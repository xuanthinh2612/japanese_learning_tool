import api from "@/services/service";


export const loginRequest = (username: string, password: string) => api.post("/login", {
                username,
                password,
            });


export const registerRequest = (username: string, password: string, email: string) => api.post("/register", {
                username,
                password,
                email
            });

export const getProfileRequest = () => api.get("/profile");

