

document.addEventListener("DOMContentLoaded", function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.classList.add('show');
        setTimeout(() => {
            alert.classList.remove('show');
        }, 5000); // Display alerts for 5 seconds
    });

    // Handle logout button
    const logoutButton = document.querySelector('.logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(event) {
            event.preventDefault();
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = logoutButton.href;

            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = '_method';
            input.value = 'POST';
            form.appendChild(input);

            document.body.appendChild(form);
            form.submit();
        });
    }
});




