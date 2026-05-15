const avatarInput = document.getElementById('avatar-input');
const avatarImg = document.getElementById('avatar-img');

if (avatarInput && avatarImg) {
    avatarInput.addEventListener('change', function(event) {
        const selectedFile = event.target.files[0];
        if (!selectedFile) return;

        avatarImg.src = URL.createObjectURL(selectedFile);

        const formData = new FormData();
        formData.append('avatar', selectedFile);

        // Находим CSRF-токен на странице
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

        const headers = {
            'X-Requested-With': 'XMLHttpRequest'
        };

        // Если токен найден, добавляем его в заголовки запроса
        if (csrfToken) {
            headers['X-CSRFToken'] = csrfToken;
        }

        fetch('/upload_avatar', {
            method: 'POST',
            body: formData,
            headers: headers
        })
        .then(response => {
            const contentType = response.headers.get("content-type");

            // Защита от падения парсера: если сервер вернул HTML вместо JSON
            if (contentType && contentType.indexOf("application/json") === -1) {
                throw new Error(`Сервер вернул HTML-страницу (Код ${response.status}). Проверьте консоль Python.`);
            }

            return response.json();
        })
        .then(data => {
            if (data.success) {
                console.log('Аватар успешно изменен.');
            } else {
                alert('Ошибка: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Критический сбой:', error);
            alert('Сбой загрузки: ' + error.message);
        });
    });
}
