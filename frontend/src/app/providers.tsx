import type { ReactNode } from "react";
import { AuthProvider } from "@/features/auth/context/AuthContext";
import { UIProvider } from "@/shared/components/context/UIContext";

type Props = {
    children: ReactNode;
};

const Providers = ({ children }: Props) => {
    return (
        <UIProvider>
            <AuthProvider>
                {children}
            </AuthProvider>
        </UIProvider>
    );
};

export default Providers;
