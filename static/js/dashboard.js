// =====================================================
// AI Personality Prediction Dashboard
// dashboard.js
// =====================================================

// ===============================
// Page Loading Animation
// ===============================

window.addEventListener("load", () => {

    document.body.classList.add("loaded");

});

// ===============================
// Navbar Scroll Effect
// ===============================

const navbar = document.querySelector(".dashboard-navbar");

window.addEventListener("scroll", () => {

    if (!navbar) return;

    if (window.scrollY > 50) {

        navbar.classList.add("navbar-scrolled");

    } else {

        navbar.classList.remove("navbar-scrolled");

    }

});

// ===============================
// Fade Animation
// ===============================

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.classList.add("show");

        }

    });

}, {

    threshold:0.15

});

document.querySelectorAll(

".trait-card,.overall-card,.glass-section,.insight-card,.action-card"

).forEach(card=>{

    observer.observe(card);

});

// ===============================
// Progress Bar Animation
// ===============================

const progressBars=document.querySelectorAll(".progress-bar");

progressBars.forEach(bar=>{

    const width=bar.style.width;

    bar.style.width="0%";

    setTimeout(()=>{

        bar.style.transition="width 1.8s ease";

        bar.style.width=width;

    },400);

});

// ===============================
// Overall Counter Animation
// ===============================

const counter = document.querySelector(".overall-circle");

if (counter) {

    let final = parseFloat(counter.textContent);

    let current = 0;

    const timer = setInterval(() => {

        current += 0.1;

        if (current >= final) {

            current = final;

            clearInterval(timer);

        }

        counter.textContent = current.toFixed(1) + "/5";

    }, 20);

}


// ===============================
// Floating Background Animation
// ===============================

document.querySelectorAll(".bg-circle").forEach((circle,index)=>{

circle.animate(

[

{

transform:"translateY(0px)"

},

{

transform:"translateY(-25px)"

},

{

transform:"translateY(0px)"

}

],

{

duration:6000+(index*1200),

iterations:Infinity,

direction:"alternate",

easing:"ease-in-out"

}

);

});


// ===============================
// Hover Animation
// ===============================

document.querySelectorAll(

".trait-card,.overall-card,.glass-section,.insight-card,.action-card"

).forEach(card=>{

card.addEventListener("mousemove",(e)=>{

const rect=card.getBoundingClientRect();

const x=e.clientX-rect.left;

const y=e.clientY-rect.top;

card.style.setProperty("--x",x+"px");

card.style.setProperty("--y",y+"px");

});

});


// ===============================
// Button Ripple Effect
// ===============================

document.querySelectorAll(".btn").forEach(btn=>{

btn.addEventListener("mouseenter",()=>{

btn.style.transition=".35s";

btn.style.transform="translateY(-3px)";

});

btn.addEventListener("mouseleave",()=>{

btn.style.transform="translateY(0px)";

});

});
const themeBtn = document.getElementById("themeToggle");

if(themeBtn){

    // Load saved theme
    if(localStorage.getItem("theme")==="light"){

        document.body.classList.add("light-mode");

        themeBtn.innerHTML='<i class="bi bi-sun-fill"></i>';

    }

    themeBtn.addEventListener("click",()=>{

        document.body.classList.toggle("light-mode");

        if(document.body.classList.contains("light-mode")){

            localStorage.setItem("theme","light");

            themeBtn.innerHTML='<i class="bi bi-sun-fill"></i>';

        }else{

            localStorage.setItem("theme","dark");

            themeBtn.innerHTML='<i class="bi bi-moon-fill"></i>';

        }

    });

}
