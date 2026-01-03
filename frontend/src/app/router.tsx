import { createBrowserRouter } from "react-router-dom";
import Login from "@/features/auth/pages/Login";
import Profile from "@/features/auth/pages/Profile";
import Register from "@/features/auth/pages/Register";
import MainLayout from "@/shared/components/layouts/MainLayout";
import AuthLayout from "@/shared/components/layouts/AuthLayout";
import HomePage from "@/features/homePage/pages/HomePage";
import TopWords from "@/features/vocabulary/pages/TopWords";
import WordDetail from "@/features/vocabulary/pages/WordDetail";

export const router = createBrowserRouter([
  { path: "/login", element: <AuthLayout><Login /></AuthLayout>, },
  { path: "/register", element: <AuthLayout><Register /></AuthLayout>, },
  { path: "/profile", element: <MainLayout><Profile /></MainLayout>, },
  { path: "/", element: <MainLayout><HomePage /></MainLayout>, },
  { path: "/top-words", element: <MainLayout><TopWords /></MainLayout>, },
  { path: "/word-detail/:wordText", element: <MainLayout><WordDetail /></MainLayout>, },
]);
