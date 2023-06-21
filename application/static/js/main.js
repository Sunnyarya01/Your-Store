function togglePassword() {
    var passwordInput = document.getElementById('password');
    var toggleBtn = document.getElementById('toggle-btn');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleBtn.textContent = 'Hide';
    } else {
        passwordInput.type = 'password';
        toggleBtn.textContent = 'Show';
    }
}

var slides = document.getElementsByClassName("slide");
var currentSlide = 0;

// Show the first slide
slides[currentSlide].style.display = "block";

// Function to move to the next slide
function nextSlide() {
    slides[currentSlide].style.display = "none";
    currentSlide = (currentSlide + 1) % slides.length;
    slides[currentSlide].style.display = "block";
}

// Function to move to the previous slide
function prevSlide() {
    slides[currentSlide].style.display = "none";
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    slides[currentSlide].style.display = "block";
}

// Add event listeners to navigation controls
setInterval(() => {
    nextSlide()
}, 1500);
