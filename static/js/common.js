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
