document.addEventListener('DOMContentLoaded', function () {
    const ratingElements = document.querySelectorAll('.result-info li:last-child');

    ratingElements.forEach(function (ratingElement) {
        const ratingTextElement = ratingElement.querySelector('.average-rating-value');

        if (ratingTextElement) {
            const ratingValue = parseFloat(ratingTextElement.textContent);
            let stars = '';
            const fullStars = Math.floor(ratingValue);
            const fraction = ratingValue - fullStars;

            // Add full stars
            for (let i = 0; i < fullStars; i++) {
                stars += '<span class="star full">★</span>';
            }

            // Add half star if needed
            if (fraction >= 0.25 && fraction < 0.75) {
                stars += '<span class="star half">★</span>';
            } else if (fraction >= 0.75) {
                stars += '<span class="star full">★</span>';
            }

            // Fill the rest with empty stars
            const totalStars = fullStars + (fraction >= 0.25 ? 1 : 0);
            for (let i = totalStars; i < 5; i++) {
                stars += '<span class="star empty">☆</span>';
            }

            ratingTextElement.insertAdjacentHTML('afterend', ' <span class="result-stars">' + stars + '</span>');
        }
    });
});