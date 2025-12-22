// JS vẫn giữ nguyên
function showToast(msg){
    const box = document.getElementById("toast-container");
    const t = document.createElement("div");
    t.innerText = msg;
    t.style.cssText = `
        background: linear-gradient(90deg, #3498db, #2ecc71);
        color: #fff;
        padding: 12px 20px;
        margin-top: 10px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        font-weight: 500;
        min-width: 180px;
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.3s, transform 0.3s;
    `;
    // Thêm vào container ở dưới cùng (hiển thị từ dưới lên)
    box.insertBefore(t, box.firstChild);

    setTimeout(()=>{
        t.style.opacity = 1;
        t.style.transform = 'translateY(0)';
    }, 10);

    setTimeout(()=>{
        t.style.opacity = 0;
        t.style.transform = 'translateY(20px)';
        setTimeout(()=>t.remove(), 300);
    }, 2500);
}

function addWordToMyList (wordId){
        fetch(`/add_to_learning/${wordId}`,{
            method:"POST",
            headers:{"Content-Type":"application/json"}
        }).then(r=>r.json()).then(res=>{
            showToast(res.message);
            if(res.success){
                // updateUI(li, "learning");
            }
        });

};


document.addEventListener("click", function(e) {
    // Kiểm tra xem click có phải vào button không
    const btn = e.target.closest(".action-btn");

    if (btn) {
        // Tìm thẻ cha chứa button
        const parentCard = btn.closest(".topword-card"); // hoặc div cha gần nhất
        if (parentCard) {
            // Tìm thẻ topword-text trong thẻ cha
            const topword = parentCard.querySelector(".topword-text");
            if (topword) {
                const wordId = topword.dataset.id; // hoặc dataset.href / dataset.id tùy bạn đặt
                // Gọi hàm khác và truyền word
                addWordToMyList(wordId);
                // Thêm attribute disabled
                btn.setAttribute("disabled", "true");
                btn.innerText = "Đã thêm";
                btn.classList.remove("add-btn");
                updateStatus(parentCard);
            }
        }
        return; // dừng hàm, không chạy click card
    }

    // Nếu click vào text
    const card = e.target.closest(".topword-text");
    if (card) {
        const href = card.dataset.href;
        if (href) {
            window.location.href = href;
        }
    }
});

function updateStatus(parentCard) {
    // Lấy element span có class 'status'
    let leaning_status = parentCard.querySelector(".status");

    if (leaning_status) {
        // Xóa tất cả class cũ (hoặc chỉ xóa class 'none')
        leaning_status.className = "status learning";

        // Thay đổi text
        leaning_status.innerText = "📘 Đang học";
    }
}