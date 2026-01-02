import { RouterProvider } from "react-router-dom";
import { router } from "./router";
import Providers from "./providers";
import MainLayout from '@/shared/components/layouts/MainLayout';  // Import Layout component
import AuthLayout from "@/shared/components/layouts/AuthLayout";


function App() {
  return (
    <Providers>
      <MainLayout>
        <RouterProvider router={router} />
      </MainLayout>

    </Providers>
  );
}

export default App