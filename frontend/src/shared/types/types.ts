
export interface Pagination {
    pages: number;
    current_page: number;
    has_prev: boolean;
    has_next: boolean;
    prev_num?: number;
    next_num?: number;
}