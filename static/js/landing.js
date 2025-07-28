
document.addEventListener('DOMContentLoaded', () => {
const usernameInput = document.querySelector('input[name="username"]');
const passwordInput = document.querySelector('input[name="password"]');

usernameInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
    e.preventDefault(); // prevent accidental form submit
    passwordInput.focus();
    }
});


passwordInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
    e.preventDefault();
    document.querySelector('button[type="submit"]').click(); // or handle login 
    }
});
});


document.addEventListener('DOMContentLoaded', () => {
const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");

const showRegisterBtn = document.getElementById("show-register");
if (showRegisterBtn && loginForm && registerForm) {
    showRegisterBtn.addEventListener("click", function (e) {
        e.preventDefault();
        loginForm.style.display = "none";
        registerForm.style.display = "block";
    });
}

const showLoginBtn = document.getElementById("show-login");
if (showLoginBtn && loginForm && registerForm) {
    showLoginBtn.addEventListener("click", function (e) {
        e.preventDefault();
        registerForm.style.display = "none";
        loginForm.style.display = "flex";
    });
}
});