// JS vẫn giữ nguyên
// function showToast(msg){
//     const box = document.getElementById("toast-container");
//     const t = document.createElement("div");
//     t.innerText = msg;
//     t.style.cssText = `
//         background: linear-gradient(90deg, #3498db, #2ecc71);
//         color: #fff;
//         padding: 12px 20px;
//         margin-top: 10px;
//         border-radius: 10px;
//         box-shadow: 0 4px 10px rgba(0,0,0,0.2);
//         font-weight: 500;
//         min-width: 180px;
//         opacity: 0;
//         transform: translateY(20px);
//         transition: opacity 0.3s, transform 0.3s;
//     `;
//     // Thêm vào container ở dưới cùng (hiển thị từ dưới lên)
//     box.insertBefore(t, box.firstChild);

//     setTimeout(()=>{
//         t.style.opacity = 1;
//         t.style.transform = 'translateY(0)';
//     }, 10);

//     setTimeout(()=>{
//         t.style.opacity = 0;
//         t.style.transform = 'translateY(20px)';
//         setTimeout(()=>t.remove(), 300);
//     }, 2500);
// }

// document.getElementById("word-list").addEventListener("click", function(e){
//     const btn = e.target.closest(".action-btn");
//     if(!btn) return;

//     const li = btn.closest("li");
//     const wordId = li.dataset.id;
//     const action = btn.dataset.action;

//     if(action=="add"){
//         fetch(`/add_to_learning/${wordId}`,{
//             method:"POST",
//             headers:{"Content-Type":"application/json"}
//         }).then(r=>r.json()).then(res=>{
//             showToast(res.message);
//             if(res.success){
//                 li.dataset.itemId = res.item_id;
//                 updateUI(li, "learning");
//             }
//         });
//         return;
//     }

//     let newStatus;
//     if(action=="drop") newStatus = "dropped";
//     else if(action=="reset") newStatus = "learning";
//     else if(action=="reviewing") newStatus = "reviewing";
//     else if(action=="mastered") newStatus = "mastered";

//     fetch(`/update_learning_status/${wordId}`,{
//         method:"POST",
//         headers:{"Content-Type":"application/json"},
//         body: JSON.stringify({status:newStatus})
//     }).then(r=>r.json()).then(res=>{
//         showToast(res.message);
//         if(res.success){
//             updateUI(li, newStatus);
//         }
//     });
// });

// function updateUI(li, status){
//     const statusSpan = li.querySelector(".status");
//     const actionsSpan = li.querySelector(".actions");
//     let statusText="", actionsHtml="";

//     if(status=="learning"){
//         statusText="📘 Đang học";
//         actionsHtml=`<button class="action-btn" data-action="drop">❌ Bỏ</button>
//                      <button class="action-btn" data-action="reviewing">🔁 Đang ôn</button>`;
//     } else if(status=="reviewing"){
//         statusText="🔁 Đang ôn";
//         actionsHtml=`<button class="action-btn" data-action="drop">❌ Bỏ</button>
//                      <button class="action-btn" data-action="mastered">✔ Đã thuộc</button>`;
//     } else if(status=="mastered"){
//         statusText="✔ Đã thuộc";
//         actionsHtml=`<button class="action-btn" data-action="reset">↩ Học lại</button>`;
//     } else if(status=="dropped"){
//         statusText="❌ Đã bỏ";
//         actionsHtml=`<button class="action-btn" data-action="reset">↩ Học lại</button>`;
//     }

//     statusSpan.innerText = statusText;
//     actionsSpan.innerHTML = actionsHtml;
// }

// =====================
document.addEventListener("click", function (e) {
    const btn = e.target.closest(".action-btn");
    if (btn) {
        e.stopPropagation(); // ❌ không click card
        return;
    }

    const card = e.target.closest(".topword-card");
    if (card) {
        const href = card.dataset.href;
        if (href) {
            window.location.href = href;
        }
    }
});

// function toggleDropdown() {
//     const menu = document.getElementById("user-dropdown");
//     menu.style.display = menu.style.display === "flex" ? "none" : "flex";
// }

// Ẩn dropdown nếu click ra ngoài
// document.addEventListener("click", function(event){
//     const dropdown = document.querySelector(".dropdown");
//     const menu = document.getElementById("user-dropdown");
//     if(dropdown && !dropdown.contains(event.target)){
//         menu.style.display = "none";
//     }
// });