import type { ReactNode } from "react";

type Props = {
    children: ReactNode;
};

const Providers = ({ children }: Props) => {
    return <>{children}</>;
};

export default Providers;
