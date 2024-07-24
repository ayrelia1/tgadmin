document.addEventListener('DOMContentLoaded', function() {
    const newsletterTitle = document.getElementById("newsletter-title");
    const newsletterForm = document.getElementById("newsletter-form");
    const newsletterMessageInput = document.getElementById("newsletter-message");
    const newsletterButton = document.getElementById("newsletter-button");
    const newsletterModal = document.getElementById("newsletter-modal");
    const closeButton = document.querySelectorAll(".close-button");

    // Проверка существования элементов перед добавлением обработчиков
    if (newsletterButton) {
        newsletterButton.addEventListener("click", () => {
            if (newsletterTitle && newsletterMessageInput && newsletterModal) {
                newsletterMessageInput.value = ""; // Очистить поле ввода
                newsletterTitle.textContent = "Рассылка";
                newsletterModal.classList.add("show"); // Показать модальное окно
            }
        });
    }

    if (newsletterForm) {
        newsletterForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const message = newsletterMessageInput.value;
    
            try {
                const response = await fetch(`/send-newsletter`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ message: message })
                });
    
                // Парсим JSON-ответ
                const result = await response.json();
    
                if (response.ok) {
                    alert("Рассылка отправлена успешно!");
                    if (newsletterModal) {
                        newsletterModal.classList.remove("show"); // Скрыть модальное окно
                    }
                } else {
                    // Показать сообщение об ошибке, если оно есть
                    const errorMessage = result.message || "Произошла ошибка, рассылка не была начата";
                    alert(`Ошибка: ${errorMessage}`);
                    if (newsletterModal) {
                        newsletterModal.classList.remove("show"); // Скрыть модальное окно
                    }
                }
            } catch (error) {
                console.error("Error:", error);
                alert("Произошла ошибка при отправке запроса.");
            }
        });
    }

    if (closeButton.length > 0) {
        closeButton.forEach(button => {
            button.addEventListener("click", (event) => {
                const modalId = event.target.getAttribute("data-modal-id");
                const modal = document.getElementById(modalId);
                if (modal) {
                    modal.classList.remove("show"); // Скрыть соответствующее модальное окно
                }
            });
        });
    }

    function closeModal(event) {
        if (newsletterModal && event.target === newsletterModal) {
            newsletterModal.classList.remove("show"); // Скрыть модальное окно при клике вне его
        }
    }

    window.addEventListener("click", closeModal);
    window.addEventListener("touchend", closeModal); // Обработка касания на мобильных устройствах

    const statusToggles = document.querySelectorAll('.status-toggle');

    statusToggles.forEach(toggle => {
        toggle.addEventListener('change', async function() {
            const userId = this.getAttribute('data-user-id');
            const status = this.checked ? 'enabled' : 'disabled';

            try {
                const response = await fetch(`/update_status/${userId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') // Получение CSRF токена
                    },
                    body: JSON.stringify({ status: status })
                });

                if (response.ok) {
                    const statusLabel = this.closest('.user-status').querySelector('.status-label');
                    if (statusLabel) {
                        statusLabel.textContent = this.checked ? 'Доступ открыт' : 'Доступ закрыт';
                    }
                    console.log('Status updated successfully');
                } else {
                    console.error('Failed to update status');
                }
            } catch (error) {
                console.error('Error:', error);
            }
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
