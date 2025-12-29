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