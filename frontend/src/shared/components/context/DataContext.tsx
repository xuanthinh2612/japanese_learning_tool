import { createContext, useContext, useState } from "react";


type DataContextType = {
    isLoadingData: boolean;
    setIsLoadingData: (isLoading: boolean) => void;
};

const DataContext = createContext<DataContextType | null>(null);

export const DataContextProvider = ({ children }: { children: React.ReactNode }) => {

    const [isLoadingData, setIsLoadingData] = useState(true);

    // const toggleSidebar = () => {
    //     setIsSidebarOpen((prev) => !prev);
    // };

    return (
        <DataContext.Provider value={{ isLoadingData, setIsLoadingData }}>
            {children}
        </DataContext.Provider>
    );
};

export const useData = () => {
    const ctx = useContext(DataContext);
    if (!ctx) throw new Error("useData must be used inside DataContextProvider");
    return ctx;
};
