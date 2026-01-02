import type { ReactNode } from "react";
import { AuthProvider } from "@/features/auth/context/AuthContext";

type Props = {
    children: ReactNode;
};

const Providers = ({ children }: Props) => {
    return <AuthProvider>{children}</AuthProvider>;
};

export default Providers;
