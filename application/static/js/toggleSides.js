document.addEventListener('DOMContentLoaded', () => {
    const sidebarLeft = document.getElementById('sidebarLeft');
    const sidebarRight = document.getElementById('sidebarRight');
    const toggleLeftBtn = document.getElementById('toggleLeft');
    const toggleRightBtn = document.getElementById('toggleRight');
    const mainContent = document.querySelector('.main-content');
  
    console.log("DOM Content Loaded");
  
    if (window.innerWidth < 500) {
      if (sidebarLeft) {
        sidebarLeft.classList.add('collapsed');
        sidebarLeft.classList.remove('expanded');
      }
      if (sidebarRight) {
        sidebarRight.classList.add('collapsed');
        sidebarRight.classList.remove('expanded');
      }
    }
  
    if (toggleLeftBtn) {
      toggleLeftBtn.addEventListener('click', () => {
        console.log("Left Toggle Clicked");
        sidebarLeft.classList.toggle('expanded');
        sidebarLeft.classList.toggle('collapsed');
      });
    }
  
    if (toggleRightBtn) {
      toggleRightBtn.addEventListener('click', () => {
        console.log("Right Toggle Clicked");
        sidebarRight.classList.toggle('expanded');
        sidebarRight.classList.toggle('collapsed');
      });
    }
  
    window.addEventListener('resize', () => {
      if (window.innerWidth < 500) {
        if (sidebarLeft && !sidebarLeft.classList.contains('collapsed')) {
          sidebarLeft.classList.add('collapsed');
          sidebarLeft.classList.remove('expanded');
        }
        if (sidebarRight && !sidebarRight.classList.contains('collapsed')) {
          sidebarRight.classList.add('collapsed');
          sidebarRight.classList.remove('expanded');
        }
      }
    });
  });