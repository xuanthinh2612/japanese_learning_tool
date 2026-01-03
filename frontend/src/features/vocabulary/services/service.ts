import api from '@/services/service';

// Hàm để lấy danh sách từ vựng
export const fetchVocabularyList = async (page: number) => {
    try {
        const response = await api.get('/top-words', {
            params: {
                page,  // Truyền tham số page vào URL
            },
        });
        return response.data; // Trả về dữ liệu từ response
    } catch (error) {
        console.error("Error fetching vocabulary list:", error);
        throw error;
    }
};

// Hàm để thêm từ vào danh sách học
export const addWordToList = async (word_id: string) => {
    try {
        const response = await api.post(`/add_to_learning/${word_id}`);
        return response.data;  // Trả về dữ liệu từ response
    } catch (error) {
        console.error("Error adding word to list:", error);
        throw error;
    }
};
// Hàm để thêm từ vào danh sách học
export const fetchWordDetail = async (word_text: string) => {
    try {
        const response = await api.post(`/word-detail/${word_text}`);
        return response.data;  // Trả về dữ liệu từ response
    } catch (error) {
        console.error("Error adding word to list:", error);
        throw error;
    }
};
