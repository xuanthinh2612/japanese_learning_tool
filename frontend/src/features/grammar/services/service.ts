import api from '@/services/service';

// Hàm để lấy danh sách từ vựng
export const fetchGrammarList = async (page: number) => {
    try {
        const response = await api.get('/grammar', {
            params: {
                page,  // Truyền tham số page vào URL
            },
        });
        return response.data; // Trả về dữ liệu từ response
    } catch (error) {
        console.error("Error fetching grammar list:", error);
        throw error;
    }
};

// Hàm để thêm từ vào danh sách học
export const addGrammar = async (grammarId: string) => {
    try {
        const response = await api.post(`/add_to_learning/${grammarId}`);
        return response.data;  // Trả về dữ liệu từ response
    } catch (error) {
        console.error("Error adding grammar to list:", error);
        throw error;
    }
};

// Hàm để lấy chi tiết ngữ pháp
export const fetchGrammarDetail = async (grammarId: string) => {
    try {
        const response = await api.get(`/grammar/${grammarId}`);
        return response.data;  // Trả về dữ liệu từ response
    } catch (error) {
        console.error("Error fetching grammar detail:", error);
        throw error;
    }
};
