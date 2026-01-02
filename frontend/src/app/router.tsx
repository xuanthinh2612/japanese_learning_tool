import { createBrowserRouter } from "react-router-dom";
import Login from "@/features/auth/pages/Login";
import Profile from "@/features/auth/pages/Profile";
import Register from "@/features/auth/pages/Register";
import MainLayout from "@/shared/components/layouts/MainLayout";

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/profile",
    element: <Profile />,
  },
  {
    path: "/register",
    element: <Register />,
  },
]);
