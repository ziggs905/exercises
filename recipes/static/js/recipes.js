function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
}

const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function () {
    const favoriteBtn = document.getElementById('favorite-btn');
    if (favoriteBtn) {
        favoriteBtn.addEventListener('click', function () {
            const recipeId = favoriteBtn.dataset.recipeId;
            fetch(`/recipes/${recipeId}/favorite/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
            })
                .then(response => response.json())
                .then(data => {
                    favoriteBtn.textContent = data.is_favorite ? '★ Favorited' : '☆ Add to favorites';
                });
        });
    }

    const ratingWidget = document.getElementById('rating-widget');
    if (ratingWidget) {
        const recipeId = ratingWidget.dataset.recipeId;
        ratingWidget.querySelectorAll('.rating-star').forEach(function (star) {
            star.addEventListener('click', function () {
                const value = Number(star.dataset.value);
                fetch(`/recipes/${recipeId}/rate/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ rating: value }),
                })
                    .then(response => response.json())
                    .then(data => {
                        ratingWidget.querySelectorAll('.rating-star').forEach(function (s) {
                            s.textContent = Number(s.dataset.value) <= data.rating ? '★' : '☆';
                        });
                    });
            });
        });
    }
});
