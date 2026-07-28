
// ==========================================
// History Page JavaScript
// AI Personality Prediction System
// ==========================================


// ================================
// Navbar Scroll Effect
// ================================

window.addEventListener("scroll", function () {

    const navbar = document.querySelector(".custom-navbar");

    if (navbar) {

        if (window.scrollY > 50) {

            navbar.style.background = "#08111F";
            navbar.style.boxShadow = "0 8px 25px rgba(0,0,0,.35)";

        } else {

            navbar.style.background = "rgba(8,17,31,.90)";
            navbar.style.boxShadow = "none";

        }

    }

});


// ================================
// Back Button Hover Effect
// ================================

const button = document.querySelector(".btn-primary");

if (button) {

    button.addEventListener("mouseenter", function () {

        button.style.transform = "translateY(-4px)";

    });

    button.addEventListener("mouseleave", function () {

        button.style.transform = "translateY(0px)";

    });

}


// ================================
// Table Animation
// ================================

window.addEventListener("load", function () {

    const rows = document.querySelectorAll("tbody tr");

    rows.forEach((row, index) => {

        row.style.opacity = "0";
        row.style.transform = "translateY(20px)";

        setTimeout(() => {

            row.style.transition = "all 0.5s ease";
            row.style.opacity = "1";
            row.style.transform = "translateY(0)";

        }, index * 150);

    });

});


// ================================
// Search History
// ================================

const searchInput = document.getElementById("searchInput");

if (searchInput) {

    searchInput.addEventListener("keyup", function () {

        const filter = this.value.toLowerCase();

        const rows = document.querySelectorAll("tbody tr");

        rows.forEach(function (row) {

            const username = row.cells[1].textContent.toLowerCase();

            if (username.includes(filter)) {

                row.style.display = "";

            } else {

                row.style.display = "none";

            }

        });

    });

}


// ================================
// Delete Row (Temporary)
// ================================

function deleteRow(button) {

    const confirmDelete = confirm("Are you sure you want to delete this record?");

    if (confirmDelete) {

        button.closest("tr").remove();

        alert("Record Deleted Successfully!");

    }

}


// ================================
// Page Fade Animation
// ================================

window.addEventListener("load", function () {

    document.body.style.opacity = "0";

    setTimeout(function () {

        document.body.style.transition = "opacity .8s";
        document.body.style.opacity = "1";

    }, 100);

});


// ================================
// Console
// ================================

console.log("History Page Loaded Successfully 🚀");

