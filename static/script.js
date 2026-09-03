const header = document.getElementById("header");
const menuBtn = document.getElementById("menuBtn");
const nav = document.getElementById("nav");

window.addEventListener("scroll", () => {
  header.classList.toggle("scrolled", window.scrollY > 10);
  document.getElementById("backTop").classList.toggle("show", window.scrollY > 500);
});

menuBtn.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
});

document.querySelectorAll(".drop-btn").forEach(btn => {
  btn.addEventListener("click", e => {
    if (window.innerWidth <= 900) {
      e.preventDefault();
      btn.parentElement.classList.toggle("open");
    }
  });
});

document.querySelectorAll(".nav a").forEach(a => {
  a.addEventListener("click", () => nav.classList.remove("open"));
});

/* Hero slider */
const slides = [...document.querySelectorAll(".hero-slide")];
const dots = document.getElementById("heroDots");
let current = 0;
let timer;

slides.forEach((_, i) => {
  const dot = document.createElement("button");
  dot.className = "hero-dot" + (i === 0 ? " active" : "");
  dot.setAttribute("aria-label", `Go to slide ${i + 1}`);
  dot.addEventListener("click", () => goToSlide(i));
  dots.appendChild(dot);
});

function goToSlide(i) {
  current = (i + slides.length) % slides.length;
  slides.forEach((s, n) => s.classList.toggle("active", n === current));
  [...dots.children].forEach((d, n) => d.classList.toggle("active", n === current));
  clearInterval(timer);
  timer = setInterval(() => goToSlide(current + 1), 5500);
}
document.getElementById("prevSlide").addEventListener("click", () => goToSlide(current - 1));
document.getElementById("nextSlide").addEventListener("click", () => goToSlide(current + 1));
timer = setInterval(() => goToSlide(current + 1), 5500);

/* Client slider */
const clientTrack = document.getElementById("clientTrack");
const clientPages = [...document.querySelectorAll(".client-page")];
const clientDots = document.getElementById("clientDots");
let clientIndex = 0;

clientPages.forEach((_, i) => {
  const d = document.createElement("button");
  d.className = "client-dot" + (i === 0 ? " active" : "");
  d.setAttribute("aria-label", `Client group ${i + 1}`);
  d.addEventListener("click", () => goClient(i));
  clientDots.appendChild(d);
});

function goClient(i) {
  clientIndex = (i + clientPages.length) % clientPages.length;
  clientTrack.style.transform = `translateX(-${clientIndex * 100}%)`;
  [...clientDots.children].forEach((d, n) => d.classList.toggle("active", n === clientIndex));
}
document.getElementById("clientPrev").addEventListener("click", () => goClient(clientIndex - 1));
document.getElementById("clientNext").addEventListener("click", () => goClient(clientIndex + 1));
setInterval(() => goClient(clientIndex + 1), 6000);

/* Reveal on scroll */
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    }
  });
}, {threshold: 0.12});
document.querySelectorAll(".reveal").forEach(el => observer.observe(el));

/* Contact form -> Django database */
const contactForm = document.getElementById("contactForm");
if (contactForm) {
  contactForm.addEventListener("submit", async e => {
    e.preventDefault();
    const button = contactForm.querySelector("button[type=submit]");
    const status = document.getElementById("formStatus");
    const csrf = contactForm.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
    const payload = Object.fromEntries(new FormData(contactForm).entries());
    button.disabled = true;
    button.textContent = "Sending…";
    status.textContent = "Submitting your enquiry securely…";
    status.classList.remove("success", "error");

    try {
      const response = await fetch("/api/enquiries/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrf,
          "Accept": "application/json"
        },
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      if (!response.ok || !data.ok) throw new Error(data.message || "Unable to submit enquiry.");
      status.textContent = `${data.message} Reference: ${data.reference}`;
      status.classList.add("success");
      contactForm.reset();
    } catch (error) {
      status.textContent = error.message || "Something went wrong. Please try again.";
      status.classList.add("error");
    } finally {
      button.disabled = false;
      button.textContent = "Send Enquiry →";
    }
  });
}

document.getElementById("backTop").addEventListener("click", () => window.scrollTo({top:0, behavior:"smooth"}));
document.getElementById("year").textContent = new Date().getFullYear();
