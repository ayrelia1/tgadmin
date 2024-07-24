document.addEventListener("DOMContentLoaded", () => {
    const createButton = document.getElementById("create-button");
    const selectOtdel = document.getElementById("select-otdel");
    const userCardsContainer = document.querySelector(".user-cards-container");
    const paginationContainer = document.querySelector(".pagination");

    const questionCreateModal = document.getElementById("question-create-modal");
    const questionEditModal = document.getElementById("question-edit-modal");
    const closeButton = document.querySelectorAll(".close-button");
    const questionCreateForm = document.getElementById("question-create-form");
    const questionEditForm = document.getElementById("question-edit-form");

    const questionTitleInput = document.getElementById("question-title");
    const questionTextInput = document.getElementById("question-text");
    const questionFileInput = document.getElementById("question-file");
    const questionOtdelIdDisplay = document.getElementById("question-otdel-id");

    const editQuestionIdInput = document.getElementById("edit-question-id");
    const editQuestionTitleInput = document.getElementById("edit-question-title");
    const editQuestionTextInput = document.getElementById("edit-question-text");
    const editQuestionFileInput = document.getElementById("edit-question-file");
    const editQuestionOtdelIdDisplay = document.getElementById("edit-question-otdel-id");

    let currentPage = new URLSearchParams(window.location.search).get('page') || 1;
    let selectedOtdelId = new URLSearchParams(window.location.search).get('otdel') || null;

    // Обновляем страницу при изменении отдела
    selectOtdel.addEventListener("change", (event) => {
        currentPage = 1;  // Сбрасываем страницу на 1
        selectedOtdelId = event.target.value;
        updateUrl();
    });

    // Обновляем URL при нажатии на кнопку пагинации
    paginationContainer.addEventListener("click", (event) => {
        if (event.target.classList.contains("pagination-button")) {
            const page = event.target.getAttribute("data-page");
            if (page) {
                currentPage = page;
                updateUrl();
            }
        }
    });

    // Обновляем URL с новыми параметрами
    function updateUrl() {
        const params = new URLSearchParams();
        params.set('page', currentPage); // Устанавливаем страницу первым
        if (selectedOtdelId) {
            params.set('otdel', selectedOtdelId); // Устанавливаем отдел вторым
        }
        window.history.replaceState({}, '', `${window.location.pathname}?${params}`);
        window.location.reload(); // Перезагрузить страницу с новыми параметрами
    }

    // Открытие модального окна для создания вопроса
    if (createButton) {
        createButton.addEventListener("click", () => {
            if (selectedOtdelId) {
                questionOtdelIdDisplay.textContent = `ID отдела: ${selectedOtdelId}`;
                questionCreateModal.classList.add("show"); // Показать модальное окно
            }
        });
    }

    // Открытие модального окна для редактирования вопроса
    function openEditModal(questionId, title, text, fileName, otdelId) {
        editQuestionIdInput.value = questionId;
        editQuestionTitleInput.value = title;
        editQuestionTextInput.value = text;
        editQuestionOtdelIdDisplay.textContent = `ID отдела: ${otdelId}`;
        editQuestionFileInput.value = ''; // Файловый input не поддерживает установки значения через JS
        questionEditModal.classList.add("show"); // Показать модальное окно
    }

    // Обработчик клика по кнопкам редактирования
    userCardsContainer.addEventListener("click", (event) => {
        if (event.target.classList.contains("edit-button")) {
            const questionId = event.target.getAttribute("data-question-id");
            const title = event.target.getAttribute("data-question-name");
            const text = event.target.getAttribute("data-question-text") || "";
            const fileName = event.target.getAttribute("data-question-file") || "";
            const otdelId = event.target.getAttribute("data-question-otdel-id");
            openEditModal(questionId, title, text, fileName, otdelId);
        } else if (event.target.classList.contains("delete-button")) {
            const questionId = event.target.getAttribute("data-question-id");
            if (confirm("Вы уверены, что хотите удалить этот вопрос?")) {
                deleteQuestion(questionId);
            }
        }
    });

    // Функция для удаления вопроса
    async function deleteQuestion(questionId) {
        const response = await fetch(`/delete-question/${questionId}`, {
            method: "DELETE"
        });

        if (response.ok) {
            updateUrl(); // Обновляем URL и перезагружаем страницу
        } else {
            console.error("Failed to delete question");
        }
    }

    // Обработчик закрытия модальных окон
    closeButton.forEach(button => {
        button.addEventListener("click", (event) => {
            const modalId = event.target.getAttribute("data-modal-id");
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.remove("show"); // Скрыть соответствующее модальное окно
            }
        });
    });

    window.addEventListener("click", (event) => {
        if (event.target === questionCreateModal || event.target === questionEditModal) {
            event.target.classList.remove("show"); // Скрыть модальное окно при клике вне его
        }
    });

    // Обработка отправки формы для создания вопроса
    if (questionCreateForm) {
        questionCreateForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const title = questionTitleInput.value;
            const text = questionTextInput.value || "";
            const file = questionFileInput.files[0] || null;

            if (!text && !file) {
                alert("Пожалуйста, заполните хотя бы одно поле: текст или файл.");
                return;
            }

            const formData = new FormData();
            formData.append("title", title);
            formData.append("text", text);
            if (file) {
                formData.append("file", file);
            }
            formData.append("otdel_id", selectedOtdelId);

            const response = await fetch(`/create-question`, {
                method: "POST",
                body: formData
            });

            if (response.ok) {
                updateUrl(); // Обновляем URL и перезагружаем страницу
                questionCreateModal.classList.remove("show"); // Скрыть модальное окно
            } else {
                console.error("Failed to create question");
            }
        });
    }

    // Обработка отправки формы для редактирования вопроса
    if (questionEditForm) {
        questionEditForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const questionId = editQuestionIdInput.value;
            const title = editQuestionTitleInput.value;
            const text = editQuestionTextInput.value || "";
            const file = editQuestionFileInput.files[0] || null;

            if (!text && !file) {
                alert("Пожалуйста, заполните хотя бы одно поле: текст или файл.");
                return;
            }

            const formData = new FormData();
            formData.append("id", questionId);
            formData.append("title", title);
            formData.append("text", text);
            if (file) {
                formData.append("file", file);
            }
            formData.append("otdel_id", editQuestionOtdelIdDisplay.textContent.split(': ')[1]);

            const response = await fetch(`/edit-question`, {
                method: "PUT",
                body: formData
            });

            if (response.ok) {
                updateUrl(); // Обновляем URL и перезагружаем страницу
                questionEditModal.classList.remove("show"); // Скрыть модальное окно
            } else {
                console.error("Failed to edit question");
            }
        });
    }

    // Инициализация на основе параметров URL
    if (selectedOtdelId) {
        selectOtdel.value = selectedOtdelId;
    }
});
