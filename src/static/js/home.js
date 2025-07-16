let currentIndex = 0;
let totalCards = 0;
const cardWidth = 300;

// GLOBAL: slider fonksiyonları
function slideLeft() {
    if (currentIndex > 0) {
        currentIndex--;
        updateSlider();
    }
}

function slideRight() {
    if (currentIndex < totalCards - 1) {
        currentIndex++;
        updateSlider();
    }
}

function updateSlider() {
    const slider = document.getElementById("bookSlider");
    slider.style.transform = `translateX(-${currentIndex * cardWidth}px)`;
}

// DOM yüklendiğinde API çağrılarını yap
document.addEventListener("DOMContentLoaded", () => {
    // EN SEVİLENLER
    fetch("/api/top-rated-books/")
        .then(response => response.json())
        .then(data => {
            const slider = document.getElementById("bookSlider");
            slider.innerHTML = "";

            data.forEach(book => {
                const card = document.createElement("div");
                card.className = "book-card";
                card.innerHTML = `
                    <img src="${book.image_url}" alt="${book.title}">
                    <p>${book.title}</p>
                `;
                slider.appendChild(card);
            });

            totalCards = data.length;
        });

    // İNCELEMELER
    fetch("/api/top-reviews/")
        .then(res => res.json())
        .then(data => {
            const reviewsContainer = document.getElementById("reviewsContainer");
            reviewsContainer.innerHTML = "";

            data.forEach(review => {
                const reviewCard = document.createElement("div");
                reviewCard.classList.add("review-card");
                reviewCard.innerHTML = `
                    <p><strong>${review.username}</strong> - ${review.book_title}</p>
                    <div>${getStars(review.rating)}</div>
                    <p>${review.review_text}</p>
                `;
                reviewsContainer.appendChild(reviewCard);
            });
        })
        .catch(error => console.error("Error fetching reviews:", error));

    // TÜRLER
    fetch("/api/favorite-genres/")
        .then(res => res.json())
        .then(data => {
            data.sort((a, b) => a.genre_name.localeCompare(b.genre_name));

            const container = document.getElementById("genresContainer");
            container.innerHTML = "";

            data.forEach(item => {
                const li = document.createElement("li");
                const link = document.createElement("a");
                link.href = `/tur/${encodeURIComponent(item.genre_name)}/`;
                link.textContent = item.genre_name;
                li.appendChild(link);
                container.appendChild(li);
            });
        });
});

// YILDIZ GÖSTEREN FONKSİYON
function getStars(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 >= 0.5 ? 1 : 0;
    const emptyStars = 5 - fullStars - halfStar;

    let stars = '';

    for (let i = 0; i < fullStars; i++) stars += '⭐';
    if (halfStar) stars += '⭐';
    for (let i = 0; i < emptyStars; i++) stars += '☆';

    return stars;
}
