// users.js

document.addEventListener('DOMContentLoaded', function() {
    // Найти все переключатели статуса
    const statusToggles = document.querySelectorAll('.status-toggle');

    statusToggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            // Получить ID пользователя
            const userId = this.getAttribute('data-user-id');
            const status = this.checked ? 'enabled' : 'disabled';

            // Отправить запрос на сервер
            fetch(`/update-status/${userId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Получение CSRF токена
                },
                body: JSON.stringify({ status: status })
            })
            .then(response => {
                if (response.ok) {
                    console.log('Status updated successfully');
                } else {
                    console.error('Failed to update status');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});

// Функция для получения CSRF токена из cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}