document.addEventListener('DOMContentLoaded', (event) => {
  setTimeout(() => {
    document.body.classList.add('fade-in');
  }, 100);

  const scrollAnimations = document.querySelectorAll('.scroll-animation');
  const imageAnimations = document.querySelectorAll('.image-animation');

  function checkScroll() {
    const triggerBottom = window.innerHeight / 5 * 4;

    scrollAnimations.forEach(animation => {
      const animationTop = animation.getBoundingClientRect().top;

      if (animationTop < triggerBottom) {
        animation.classList.add('animate');
      }
    });

    imageAnimations.forEach(image => {
      const imageTop = image.getBoundingClientRect().top;

      if (imageTop < triggerBottom) {
        image.classList.add('animate');
      }
    });
  }

  window.addEventListener('scroll', checkScroll);
  checkScroll(); // Check on load
});

document.addEventListener('DOMContentLoaded', (event) => {
  const navLinks = document.querySelectorAll('.nav-link');

  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      navLinks.forEach(l => l.classList.remove('active'));
      this.classList.add('active');
    });
  });
});

document.getElementById('skill-select').addEventListener('change', function() {
    const url = this.value;
    if (url) {
      window.location.href = url;
    }
});

// Lấy username từ localStorage
function getUsername() {
  return localStorage.getItem('username') || null;
}

function updateUsernameDisplay() {
  const tenNguoiDung = getUsername();
  const usernameSpan = document.getElementById('username');
  if (tenNguoiDung) {
    usernameSpan.textContent = tenNguoiDung;
  } else {
    usernameSpan.textContent = '(Chưa đăng nhập)';
  }
}

// Gọi update để hiển thị username khi tải trang
updateUsernameDisplay();

function redirectToUser() {
  const tenNguoiDung = getUsername();
  if (tenNguoiDung) {
    window.location.href = '/user';
  } else {
    window.location.href = '/login';
  }
}

function batDauPhongVan() {
  const tenNguoiDung = getUsername();
  if (!tenNguoiDung) {
    alert('Vui lòng đăng nhập để bắt đầu phỏng vấn.');
    window.location.href = '/login';
    return;
  }
  window.location.href = '/pvan';
}
