document.addEventListener("DOMContentLoaded", () => {
    const createButton = document.getElementById("create-button");
    const editModal = document.getElementById("edit-modal");
    const createModal = document.getElementById("create-modal");
    const closeButtons = document.querySelectorAll(".close-button");
    const editForm = document.getElementById("edit-form");
    const createForm = document.getElementById("create-form");
    const editNameInput = document.getElementById("edit-name");
    const editIdInput = document.getElementById("edit-id");
    const createNameInput = document.getElementById("create-name");
    const modalTitle = document.getElementById("modal-title");
    const createTitle = document.getElementById("create-title");

    // Делегирование событий для кнопок "Удалить" и "Изменить"
    document.querySelector(".user-cards-container").addEventListener("click", async (event) => {
        if (event.target.classList.contains("delete-button")) {
            const otdelId = event.target.getAttribute("data-otdel-id");

            const response = await fetch(`/delete-otdel/${otdelId}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                }
            });

            const result = await response.json();

            if (response.ok) {
                event.target.closest(".user-card").remove();
            } else {
                const errorMessage = result.message || "Произошла ошибка";
                alert(`Ошибка: ${errorMessage}`);
            }
        }

        if (event.target.classList.contains("edit-button")) {
            const otdelId = event.target.getAttribute("data-otdel-id");
            const otdelName = event.target.getAttribute("data-otdel-name");

            editIdInput.value = otdelId;
            editNameInput.value = otdelName;
            modalTitle.textContent = `Изменить отдел ${otdelName} (ID: ${otdelId})`;
            editModal.classList.add("show");
        }
    });

    // Обработчик для кнопки создания нового отдела
    if (createButton) {
        createButton.addEventListener("click", () => {
            createNameInput.value = "";
            createTitle.textContent = "Создать новый отдел";
            createModal.classList.add("show");
        });
    }

    // Обработчики для кнопок закрытия модальных окон
    closeButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            const modalId = event.target.getAttribute("data-modal-id");
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.remove("show");
            }
        });
    });

    function closeModal(event) {
        if (event.target === editModal || event.target === createModal) {
            event.target.classList.remove("show");
        }
    }

    window.addEventListener("click", closeModal);
    window.addEventListener("touchend", closeModal);

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
                editModal.classList.remove("show");
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

            const result = await response.json();

            if (response.ok) {
                const newOtdel = result.otdel;
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
                createModal.classList.remove("show");
            } else {
                const errorMessage = result.message || "Произошла ошибка";
                alert(`Ошибка: ${errorMessage}`);
            }
        });
    }
});
