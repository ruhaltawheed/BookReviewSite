document.addEventListener("DOMContentLoaded", function () {
    // slider kısmı
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

    // incelemeler
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
        });

    // türler
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
});
