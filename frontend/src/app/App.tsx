import { RouterProvider } from "react-router-dom";
import { router } from "./router";
import Providers from "./providers";
import MainLayout from '@/shared/components/layouts/MainLayout';  // Import Layout component
import AuthLayout from "@/shared/components/layouts/AuthLayout";


function App() {
  return (
    <Providers>
        <RouterProvider router={router} />
    </Providers>
  );
}

export default App