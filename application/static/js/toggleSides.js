document.addEventListener('DOMContentLoaded', () => {
    const sidebarLeft = document.getElementById('sidebarLeft');
    const sidebarRight = document.getElementById('sidebarRight');
    const toggleLeftBtn = document.getElementById('toggleLeft');
    const toggleRightBtn = document.getElementById('toggleRight');
    const mainContent = document.querySelector('.main-content');
    const LS_LEFT_KEY = 'sidebarLeftState';
    const LS_RIGHT_KEY = 'sidebarRightState';

    console.log("DOM Content Loaded");

    const savedLeftState = localStorage.getItem(LS_LEFT_KEY);
    const savedRightState = localStorage.getItem(LS_RIGHT_KEY);

    if (sidebarLeft) {
        if (savedLeftState === 'expanded') {
            sidebarLeft.classList.add('expanded');
            sidebarLeft.classList.remove('collapsed');
        } else if (savedLeftState === 'collapsed') {
            sidebarLeft.classList.add('collapsed');
            sidebarLeft.classList.remove('expanded');
        } else if (window.innerWidth < 500) {
            sidebarLeft.classList.add('collapsed');
            sidebarLeft.classList.remove('expanded');
        }
    }

    if (sidebarRight) {
        if (savedRightState === 'expanded') {
            sidebarRight.classList.add('expanded');
            sidebarRight.classList.remove('collapsed');
        } else if (savedRightState === 'collapsed') {
            sidebarRight.classList.add('collapsed');
            sidebarRight.classList.remove('expanded');
        } else if (window.innerWidth < 500) {
            sidebarRight.classList.add('collapsed');
            sidebarRight.classList.remove('expanded');
        }
    }

    if (toggleLeftBtn) {
        toggleLeftBtn.addEventListener('click', () => {
            console.log("Left Toggle Clicked");
            sidebarLeft.classList.toggle('expanded');
            sidebarLeft.classList.toggle('collapsed');
            localStorage.setItem(LS_LEFT_KEY, sidebarLeft.classList.contains('expanded') ? 'expanded' : 'collapsed');
        });
    }

    if (toggleRightBtn) {
        toggleRightBtn.addEventListener('click', () => {
            console.log("Right Toggle Clicked");
            sidebarRight.classList.toggle('expanded');
            sidebarRight.classList.toggle('collapsed');
            localStorage.setItem(LS_RIGHT_KEY, sidebarRight.classList.contains('expanded') ? 'expanded' : 'collapsed');
        });
    }

    window.addEventListener('resize', () => {
        if (window.innerWidth < 500) {
            if (sidebarLeft && !sidebarLeft.classList.contains('collapsed')) {
                sidebarLeft.classList.add('collapsed');
                sidebarLeft.classList.remove('expanded');
                localStorage.setItem(LS_LEFT_KEY, 'collapsed'); 
            }
            if (sidebarRight && !sidebarRight.classList.contains('collapsed')) {
                sidebarRight.classList.add('collapsed');
                sidebarRight.classList.remove('expanded');
                localStorage.setItem(LS_RIGHT_KEY, 'collapsed'); 
            }
        }
    });
});