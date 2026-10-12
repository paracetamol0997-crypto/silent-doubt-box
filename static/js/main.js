// Silent Classroom Doubt Box - Main Client Scripts

document.addEventListener('DOMContentLoaded', function () {
  // 1. Mobile Menu Toggle
  const mobileToggle = document.querySelector('.mobile-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', function () {
      navLinks.classList.toggle('open');
      const isOpen = navLinks.classList.contains('open');
      mobileToggle.setAttribute('aria-expanded', isOpen);
    });
  }

  // 2. Alert Dismissal
  const alertCloseButtons = document.querySelectorAll('.alert-close');
  alertCloseButtons.forEach(button => {
    button.addEventListener('click', function () {
      const alert = this.closest('.alert');
      if (alert) {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 200);
      }
    });
  });

  // 3. Demo Fill Credentials Helper
  window.fillStudentCredentials = function (regNo, name, pwd) {
    const regInput = document.querySelector('input[name="register_number"]');
    const nameInput = document.querySelector('input[name="student_name"]');
    const pwdInput = document.querySelector('input[name="password"]');

    if (regInput) regInput.value = regNo;
    if (nameInput) nameInput.value = name;
    if (pwdInput) pwdInput.value = pwd;
  };

  window.fillTeacherCredentials = function (teacherId, pwd) {
    const idInput = document.querySelector('input[name="teacher_id"]');
    const pwdInput = document.querySelector('input[name="password"]');

    if (idInput) idInput.value = teacherId;
    if (pwdInput) pwdInput.value = pwd;
  };

  // 4. Character counter for doubt question
  const questionInput = document.getElementById('doubt-question-input');
  const charCounter = document.getElementById('question-char-count');
  if (questionInput && charCounter) {
    questionInput.addEventListener('input', function () {
      charCounter.textContent = `${this.value.length} characters`;
    });
  }
});
