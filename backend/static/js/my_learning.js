// const tabCache = {};
// const tabCache = {
//     learning: {},
//     reviewing: {},
//     mastered: {},
//     dropped: {}
// };

let currentTab = "learning";
let currentPage = 1;

function showToast(msg){
    const box = document.getElementById("toast-container");
    const t = document.createElement("div");
    t.innerText = msg;
    t.style.cssText = `
        background: linear-gradient(90deg, #3498dbb7, #2ecc7097);
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
    box.insertBefore(t, box.firstChild);

    setTimeout(()=>{ t.style.opacity = 1; t.style.transform = 'translateY(0)'; }, 10);
    setTimeout(()=>{ t.style.opacity = 0; t.style.transform = 'translateY(20px)'; setTimeout(()=>t.remove(), 300); }, 2500);
}

document.addEventListener("DOMContentLoaded", () => {
    loadTab("learning");

    document.querySelectorAll(".tabs label").forEach(label => {
        label.addEventListener("click", () => {
            setActiveTab(label);
            const status = label.dataset.status;
            loadTab(status);
        });
    });
});


function setActiveTab(activeLabel) {
    const labels = document.querySelectorAll(".tabs label");

    labels.forEach(label => {
        if (label === activeLabel) {
            label.classList.add("active-tab");
        } else {
            label.classList.remove("active-tab");
        }
    });
}


function loadTab(status, page = 1) {
    currentTab = status;
    fetch(`/api/my_learning?status=${status}&page=${page}`)
        .then(r => r.json())
        .then(res => {
            if (!res.success) return;

            // tabCache[status][page] = {
            //     items: res.data,
            //     pagination: res.pagination
            // };

            renderTable(status, res.data);
            renderPagination(status, res.pagination);
        });
}

function renderPagination(status, p) {
    const box = document.getElementById("pagination");
    box.innerHTML = "";

    if (p.pages <= 1) return;

    if (p.has_prev) {
        box.innerHTML += `
            <a class="btn" onclick="loadTab('${status}', ${p.page - 1})">← Trước</a>
        `;
    }

    box.innerHTML += `
        <span>Trang ${p.page} / ${p.pages}</span>
    `;

    if (p.has_next) {
        box.innerHTML += `
            <a class="btn" onclick="loadTab('${status}', ${p.page + 1})">Sau →</a>
        `;
    }
}


function renderTable(status, items) {    
    const panel = document.querySelector(`.panel`);
    const tbody = panel.querySelector("tbody");
    tbody.innerHTML = "";

    items.forEach(i => {
        const tr = document.createElement("tr");
        tr.setAttribute("data-row", i.word_id);
        let disp_status;

        switch (i.status) {
            case "learning":
                disp_status = "📘 Đã thêm";
                break;

            case "reviewing":
                disp_status = "🔁 Đang ôn";
                break;

            case "mastered":
                disp_status = "✔ Đã thuộc";
                break;

            case "dropped":
                disp_status = "❌ Đã bỏ";
                break;

            default:
                disp_status = "";
        }        

        tr.innerHTML = `
            <td>${i.word}</td>
            <td>
            ${disp_status}
            </td>
            <td>${renderActions(status, i.word_id)}</td>
        `;
        tbody.appendChild(tr);
    });
}


document.querySelectorAll(".tabs label").forEach(label => {
    label.addEventListener("click", () => {
        const status = label.htmlFor.replace("t-", "");
        loadTab(status);
    });
});

function update(btn, id, newStatus) {
    

    fetch(`/update_learning_status/${id}`,
        {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({status: newStatus})
        }
    )
    .then(r => r.json())
    .then(res => {
        if (!res.success) return;
        showToast(res.message);
        loadTab(currentTab);
    });
}

function renderActions(status, id) {
    if (status === "learning") {
        return `
            <button class="action-btn primary" onclick="update(this, ${id}, 'reviewing')">Đang ôn</button>
            <button class="action-btn ghost" data-action="droped" onclick="update(this, ${id}, 'dropped')">Bỏ</button>
        `;
    }
    if (status === "reviewing") {
        return `
            <button class="action-btn primary" onclick="update(this, ${id}, 'mastered')">Đã thuộc</button>
            <button class="action-btn ghost" onclick="update(this, ${id}, 'dropped')">Bỏ</button>
        `;
    }
    if (status === "mastered" || status === "dropped") {
        return `
            <button class="action-btn ghost" onclick="update(this, ${id}, 'learning')">Học lại</button>
        `;
    }
    return "";
}
