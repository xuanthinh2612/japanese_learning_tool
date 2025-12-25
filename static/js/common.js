// Toggle sidebar
function loadSideBar() {
    const sidebar = document.getElementById('sidebar');

    // Đọc trạng thái localStorage khi onload
    const collapsed = localStorage.getItem('sidebarCollapsed') === 'true';

    if (collapsed) {
        sidebar.classList.add('collapsed')
    } else {
        // Show sidebar sau khi set đúng trạng thái
        sidebar.classList.add('loaded');
    };


    const menuToggle = document.getElementById('menuToggle');
    menuToggle.addEventListener('click', () => {
        toggleClass('collapsed', 'loaded')
        localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
    });
}

// toggle class
function toggleClass(collapsed, loaded) {
        if (sidebar.classList.contains(collapsed)) {
            sidebar.classList.remove(collapsed);
            sidebar.classList.add(loaded);
        } else {
            sidebar.classList.remove(loaded);
            sidebar.classList.add(collapsed);
        }        
}

document.addEventListener('DOMContentLoaded', () => { loadSideBar() })

function goBack() {
    history.back()
}


// Show Suggestion 
const input = document.getElementById('key_search');
const searchBtn = document.getElementById('search-btn');

// Hàm gửi dữ liệu lên server
function sendSearchKeyword(keyword) {
    fetch("/api/search-suggest", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ keyword })
    })
    .then(res => res.json())
    .then(data => {
        renderSuggest(data);
    })
    .catch(err => console.error(err));
}

// Gọi AJAX khi người dùng gõ
input.addEventListener("input", function() {
    const keyword = this.value.trim();
    if(keyword.length > 0) {
        sendSearchKeyword(keyword);
    }
});

const suggestBox = document.getElementById("search-suggest");

function renderSuggest(data) {
    suggestBox.innerHTML = "";

    if (!data.success) {
        suggestBox.classList.add("hidden");
        return;
    }

    const { words, kanji_list, grammars } = data;

    let hasData = false;

    // ===== WORDS =====
    if (words && words.length > 0) {
        hasData = true;
        suggestBox.innerHTML += `
            <div class="suggest-section">
                <div class="suggest-title">📘 Từ vựng</div>
                ${words.map(w => `
                    <div class="suggest-item" data-word="${w.form}" data-type="word">
                            <div class="word-main">${w.form}</div>
                            <div class="word-meaning">${w.means_vi}</div>
                    </div>
                `).join("")}
            </div>
        `;
    }

    // ===== KANJI =====
    if (kanji_list && kanji_list.length > 0) {
        hasData = true;
        suggestBox.innerHTML += `
            <div class="suggest-section">
                <div class="suggest-title">🈶 Kanji</div>
                ${kanji_list.map(k => `
                    <div class="suggest-item kanji-search" data-kanji=${k.id} data-type="kanji">
                        <span class="word-main">${k.character || ""}</span>
                        <span class="word-meaning"> — ${k.means_vi}</span>
                    </div>
                `).join("")}
            </div>
        `;
    }

    // ===== GRAMMAR =====
    if (grammars && grammars.length > 0) {
        hasData = true;
        suggestBox.innerHTML += `
            <div class="suggest-section">
                <div class="suggest-title">✍️ Ngữ pháp</div>
                ${grammars.map(g => `
                    <div class="suggest-item grammar-search" data-grammar=${g.id} data-type="grammar">
                        <div class="word-main">${g.pattern}</div>
                        <div class="word-meaning">${g.meaning}</div>
                    </div>
                `).join("")}
            </div>
        `;
    }

    if (hasData) {
        suggestBox.classList.remove("hidden");
    } else {
        suggestBox.classList.add("hidden");
    }
}



suggestBox.addEventListener("click", function (e) {
    const item = e.target.closest(".suggest-item");
    if (!item) return;

    e.stopPropagation(); // ⭐ CHẶN click bubbling lên document

    const type = item.dataset.type;

    let url = "";

    if (type === "word") {
        const value = item.dataset.word;
        url = `/word/${encodeURIComponent(value)}`;
    } else if (type === "kanji") {
        const value = item.dataset.kanji;
        url = `/kanji/${encodeURIComponent(value)}`;
    } else if (type === "grammar") {
        const value = item.dataset.grammar;
        url = `/grammar/${encodeURIComponent(value)}`;
    }

    window.location.href = url;
});


input.addEventListener("focus", function () {
    if (this.value.trim().length > 0) {
        suggestBox.classList.remove("hidden");
    }
});

document.addEventListener("mousedown", function (e) {
    const searchDiv = document.querySelector(".search-div");

    if (!searchDiv.contains(e.target)) {
        suggestBox.classList.add("hidden");
    }
});

// Gọi AJAX khi bấm nút tìm kiếm
// searchBtn.addEventListener("click", function() {
//     const keyword = input.value.trim();
//     if(keyword.length > 0) {
//         sendSearchKeyword(keyword);
//     }
// });
