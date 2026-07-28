// =========================================
// Dashboard JavaScript
// AI Personality Prediction System
// =========================================


// =========================================
// Navbar Scroll Effect
// =========================================

window.addEventListener("scroll", function () {

    const navbar = document.querySelector(".custom-navbar");

    if (window.scrollY > 50) {

        navbar.style.background = "#08111F";
        navbar.style.boxShadow = "0 8px 25px rgba(0,0,0,.35)";

    } else {

        navbar.style.background = "rgba(8,17,31,.90)";
        navbar.style.boxShadow = "none";

    }

});


// =========================================
// Page Fade Animation
// =========================================

window.addEventListener("load", function () {

    document.body.style.opacity = "0";

    setTimeout(function () {

        document.body.style.transition = "opacity .8s ease";

        document.body.style.opacity = "1";

    }, 100);

});


// =========================================
// Dashboard Card Animation
// =========================================

const cards = document.querySelectorAll(".dashboard-card");

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.style.opacity = "1";

            entry.target.style.transform = "translateY(0)";

        }

    });

}, {

    threshold: 0.2

});

cards.forEach(card => {

    card.style.opacity = "0";

    card.style.transform = "translateY(40px)";

    card.style.transition = "all .8s ease";

    observer.observe(card);

});


// =========================================
// Progress Bar Animation
// =========================================

const progressBars = document.querySelectorAll(".progress-bar");

const progressObserver = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            const progressBar = entry.target;

            const width = progressBar.style.width;

            progressBar.style.width = "0%";

            setTimeout(() => {

                progressBar.style.transition = "width 2s ease";

                progressBar.style.width = width;

            }, 200);

        }

    });

}, {

    threshold: 0.5

});

progressBars.forEach(bar => {

    progressObserver.observe(bar);

});


// =========================================
// Hover Effect
// =========================================

cards.forEach(card => {

    card.addEventListener("mouseenter", () => {

        card.style.transform = "translateY(-8px)";

    });

    card.addEventListener("mouseleave", () => {

        card.style.transform = "translateY(0)";

    });

});


// =========================================
// Current Date
// =========================================

const dateElement = document.querySelector(".dashboard-card p:nth-child(4)");

if (dateElement) {

    const today = new Date();

    const options = {

        day: "2-digit",
        month: "long",
        year: "numeric"

    };

    dateElement.innerHTML =
        "<strong>Date :</strong> " +
        today.toLocaleDateString("en-GB", options);

}


// =========================================
// Console
// =========================================

console.log("Dashboard Loaded Successfully 🚀");
// =====================================
// Personality Chart
// =====================================

const chartCanvas = document.getElementById("personalityChart");

if (chartCanvas) {

    new Chart(chartCanvas, {

        type: "bar",

        data: {

            labels: [

                "Introvert",

                "Thinking",

                "Judging",

                "Intuition"

            ],

            datasets: [{

                label: "Personality Score",

                data: [

                    90,

                    85,

                    88,

                    82

                ],

                backgroundColor: [

                    "#4F46E5",

                    "#22C55E",

                    "#F59E0B",

                    "#EF4444"

                ],

                borderRadius: 8

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    max: 100

                }

            }

        }

    });

}
// ================================
// Dark / Light Theme
// ================================

const themeBtn = document.getElementById("themeToggle");

if (themeBtn) {

    themeBtn.addEventListener("click", () => {

        document.body.classList.toggle("light-mode");

        if (document.body.classList.contains("light-mode")) {

            themeBtn.innerHTML =
                '<i class="bi bi-sun-fill"></i>';

        } else {

            themeBtn.innerHTML =
                '<i class="bi bi-moon-fill"></i>';

        }

    });

}