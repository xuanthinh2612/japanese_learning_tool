import { useEffect, useState } from "react";
import { fetchLearningWords, updateWordStatus } from "../services/service";
// import { Pagination } from "@/shared/types/types";
import Loading from "@/shared/components/layouts/Loading";

const MyWords = () => {
  const [listWords, setListWords] = useState<any[]>([]);
  // const [pagination, setPagination] = useState<Pagination | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [statusFilter, setStatusFilter] = useState<string>("learning");

  const fetchWordsByPage = async (page: number, status: string) => {
    try {
      setLoading(true);
      const response = await fetchLearningWords(page, status);
      console.log(response);

      setListWords(response.words);
      // setPagination(response.pagination);
      setLoading(false);
    } catch (error) {
      setLoading(false);
      console.error('Error fetching words:', error);
    }
  };

  useEffect(() => {
    fetchWordsByPage(1, statusFilter);
  }, []);

  const updateStatus = async (word_id: number, newStatus: string) => {
    try {
      // Gọi API để cập nhật trạng thái từ vựng
      // await updateWordStatus(word_id, newStatus);
      setLoading(true);
      await updateWordStatus(word_id.toString(), newStatus);
      // Sau khi cập nhật thành công, tải lại danh sách từ vựng
      await fetchWordsByPage(1, statusFilter);
      setLoading(false);
    } catch (error) {
      console.error('Error updating word status:', error);
    }
  };

  const renderActions = (status: string, id: number) => {
    if (status === "learning") {
      return (
        <>
          <button className="action-btn primary" onClick={() => updateStatus(id, "reviewing")}>Đang ôn</button>
          <button className="action-btn ghost" onClick={() => updateStatus(id, "dropped")}>Bỏ</button>
        </>
      );
    }
    if (status === "reviewing") {
      return (
        <>
          <button className="action-btn primary" onClick={() => updateStatus(id, "mastered")}>Đã thuộc</button>
          <button className="action-btn ghost" onClick={() => updateStatus(id, "dropped")}>Bỏ</button>
        </>
      );
    }
    if (status === "mastered" || status === "dropped") {
      return (
        <button className="action-btn ghost" onClick={() => updateStatus(id, "learning")}>Học lại</button>
      );
    }
    return "";
  };

  const setActiveTab = async (activeLabel: HTMLElement) => {
    setLoading(true);
    const newStatus = activeLabel.getAttribute("data-status") || "learning";
    await fetchWordsByPage(1, newStatus);
    setLoading(false);
    
    setStatusFilter(newStatus);

    const labels = document.querySelectorAll(".tabs label");

    labels.forEach(label => {
      if (label === activeLabel) {
        label.classList.add("active-tab");
      } else {
        label.classList.remove("active-tab");
      }
    });
  }


  return (
    <div className="container">
      {loading && <Loading isLoading={loading} />}
      <div className="tabs">
        <label className="lable active-tab" htmlFor="t-learning" data-status="learning" onClick={(e) => setActiveTab(e.target as HTMLElement)}>📘 Đang học</label>
        <label className="lable" htmlFor="t-reviewing" data-status="reviewing" onClick={(e) => setActiveTab(e.target as HTMLElement)}>🔁 Đang ôn</label>
        <label className="lable" htmlFor="t-mastered" data-status="mastered" onClick={(e) => setActiveTab(e.target as HTMLElement)}>✔ Đã thuộc</label>
        <label className="lable" htmlFor="t-dropped" data-status="dropped" onClick={(e) => setActiveTab(e.target as HTMLElement)}>❌ Đã bỏ</label>
      </div>

      <div className="content">
        <div className="panel">
          <table>
            <thead>
              <tr>
                <th>Từ vựng</th>
                <th>Trạng thái</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {listWords.map((word) => (
                <tr key={word.word_id} data-row={word.word_id}>
                  <td>{word.word}</td>
                  <td>{word.status}</td>
                  <td>
                    {renderActions(word.status, word.word_id)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default MyWords;
