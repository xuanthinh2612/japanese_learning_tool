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
        const response = await api.get(`/word-detail/${word_text}`);
        return response.data;  // Trả về dữ liệu từ response
    } catch (error) {
        console.error("Error adding word to list:", error);
        throw error;
    }
};

// Hàm để lấy danh sách từ vựng
export const fetchLearningWords = async (page: number, status: string) => {
    try {
        const response = await api.get('/my-words', {
            params: {
                page,  // Truyền tham số page vào URL
                status
            },
        });
        return response.data; // Trả về dữ liệu từ response
    } catch (error) {
        console.error("Error fetching vocabulary list:", error);
        throw error;
    }
};

// Hàm để lấy danh sách từ vựng
export const updateWordStatus = async (word_id: string, status: string) => {
    try {
        const response = await api.post(`/update-word-status/${word_id}`, {
            status
        });

        return response.data; // Trả về dữ liệu từ response
    } catch (error) {
        console.error("Error updating word status:", error);
        throw error;
    }
};
