document.addEventListener('DOMContentLoaded', function() {
    if (sessionStorage.getItem('welcomePopupDismissed') !== 'true') {
      const popup = document.getElementById('welcomePopup');
      const closeButton = document.querySelector('.close-popup');
      popup.style.display = 'flex';
      closeButton.addEventListener('click', function() {
        popup.style.display = 'none';
        sessionStorage.setItem('welcomePopupDismissed', 'true');
      });
      
      popup.addEventListener('click', function(e) {
        if (e.target === popup) {
          popup.style.display = 'none';
          sessionStorage.setItem('welcomePopupDismissed', 'true');
        }
      });
    }
  });