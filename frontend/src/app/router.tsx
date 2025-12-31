import { createBrowserRouter } from "react-router-dom";
import Login from "@/features/auth/pages/login";
import Profile from "@/features/auth/pages/profile";

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/profile",
    element: <Profile />,
  },
]);
