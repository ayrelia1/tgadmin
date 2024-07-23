document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll(".delete-button");
    const editButtons = document.querySelectorAll(".edit-button");
    const createButton = document.getElementById("create-button");
    
    const editModal = document.getElementById("edit-modal");
    const createModal = document.getElementById("create-modal");
    const closeButton = document.querySelectorAll(".close-button");
    const editForm = document.getElementById("edit-form");
    const createForm = document.getElementById("create-form");
    
    const editNameInput = document.getElementById("edit-name");
    const editIdInput = document.getElementById("edit-id");
    const createNameInput = document.getElementById("create-name");
    
    const modalTitle = document.getElementById("modal-title");
    const createTitle = document.getElementById("create-title");

    // Добавляем обработчики для кнопок удаления
    if (deleteButtons.length > 0) {
        deleteButtons.forEach(button => {
            button.addEventListener("click", async () => {
                const otdelId = button.getAttribute("data-otdel-id");

                const response = await fetch(`/delete-otdel/${otdelId}`, {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });

                if (response.ok) {
                    button.closest(".user-card").remove();
                } else {
                    console.error("Failed to delete otdel");
                }
            });
        });
    }

    // Добавляем обработчики для кнопок редактирования
    if (editButtons.length > 0) {
        editButtons.forEach(button => {
            button.addEventListener("click", () => {
                const otdelId = button.getAttribute("data-otdel-id");
                const otdelName = button.getAttribute("data-otdel-name");

                editIdInput.value = otdelId;
                editNameInput.value = otdelName;
                modalTitle.textContent = `Изменить отдел ${otdelName} (ID: ${otdelId})`;
                editModal.classList.add("show"); // Показать модальное окно
            });
        });
    }

    // Обработчик для кнопки создания нового отдела
    if (createButton) {
        createButton.addEventListener("click", () => {
            createNameInput.value = ""; // Очистить поле ввода
            createTitle.textContent = "Создать новый отдел";
            createModal.classList.add("show"); // Показать модальное окно
        });
    }

    // Добавляем обработчики для кнопок закрытия модальных окон
    if (closeButton.length > 0) {
        closeButton.forEach(button => {
            button.addEventListener("click", (event) => {
                const modalId = event.target.getAttribute("data-modal-id");
                const modal = document.getElementById(modalId);
                if (modal) {
                    modal.classList.remove("show"); // Скрыть модальное окно
                }
            });
        });
    }

    function closeModal(event) {
        if (event.target === editModal) {
            editModal.classList.remove("show"); // Скрыть модальное окно при клике вне его
        }
        if (event.target === createModal) {
            createModal.classList.remove("show"); // Скрыть модальное окно при клике вне его
        }
    }

    window.addEventListener("click", closeModal);
    window.addEventListener("touchend", closeModal); // Обработка касания на мобильных устройствах

    // Обработчик отправки формы редактирования
    if (editForm) {
        editForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const otdelId = editIdInput.value;
            const newName = editNameInput.value;

            const response = await fetch(`/edit-otdel/${otdelId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name: newName })
            });

            if (response.ok) {
                const card = document.querySelector(`[data-otdel-id='${otdelId}']`).closest(".user-card");
                if (card) {
                    card.querySelector(".user-username").textContent = newName;
                }
                editModal.classList.remove("show"); // Скрыть модальное окно
            } else {
                console.error("Failed to edit otdel");
            }
        });
    }

    // Обработчик отправки формы создания нового отдела
    if (createForm) {
        createForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const newName = createNameInput.value;

            const response = await fetch(`/create-otdel`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name: newName })
            });

            if (response.ok) {
                const newOtdel = await response.json();
                const newCard = document.createElement("div");
                newCard.classList.add("user-card");
                newCard.innerHTML = `
                    <div class="user-card-header">
                        <h3 class="user-id">ID: ${newOtdel.id}</h3>
                        <h2 class="user-username">${newOtdel.name}</h2>
                    </div>
                    <div class="user-actions">
                        <button class="edit-button" data-otdel-id="${newOtdel.id}" data-otdel-name="${newOtdel.name}">Изменить</button>
                        <button class="delete-button" data-otdel-id="${newOtdel.id}">Удалить</button>
                    </div>
                `;
                document.querySelector(".user-cards-container").appendChild(newCard);
                createModal.classList.remove("show"); // Скрыть модальное окно
            } else {
                console.error("Failed to create otdel");
            }
        });
    }
});
