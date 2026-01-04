import { createContext, useContext, useState } from "react";


type UIContextType = {
    isSidebarOpen: boolean;
    toggleSidebar: () => void;
};

const UIContext = createContext<UIContextType | null>(null);

export const UIProvider = ({ children }: { children: React.ReactNode }) => {

    const [isSidebarOpen, setIsSidebarOpen] = useState(true);

    const toggleSidebar = () => {
        setIsSidebarOpen((prev) => !prev);
    };

    return (
        <UIContext.Provider value={{ isSidebarOpen, toggleSidebar }}>
            {children}
        </UIContext.Provider>
    );
};

export const useUI = () => {
    const ctx = useContext(UIContext);
    if (!ctx) throw new Error("useUI must be used inside UIProvider");
    return ctx;
};
