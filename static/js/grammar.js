function addGrammar(grammarId, btn) {
    let addKanjiUrl = `/api/add-grammar/${grammarId}`;
    callAPI(addKanjiUrl, btn)
};

function addKanji(kanjiId, btn) {
    let addKanjiUrl = `/api/add-kanji/${kanjiId}`;
    callAPI(addKanjiUrl, btn)
};

function disabledBtn(btn) {
    // Thêm attribute disabled
    btn.setAttribute("disabled", "true");
    btn.innerText = "Đã thêm";

}

function callAPI(url, btn) {
    fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    }).then(r => r.json()).then(res => {
        showToast(res.message);
        if (res.success) {
            disabledBtn(btn)
        }
    });
}