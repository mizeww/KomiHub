document.addEventListener('DOMContentLoaded', function() {
    const avatarInput = document.getElementById('avatar-input');
    const avatarImg = document.getElementById('avatar-img');
    const uploadProgress = document.getElementById('upload-progress');
    const progressBar = uploadProgress.querySelector('.progress-bar');

    avatarInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;

        if (!file.type.startsWith('image/')) {
            showNotification('Пожалуйста, выберите изображение', 'error');
            return;
        }

        if (file.size > 5 * 1024 * 1024) {
            showNotification('Файл слишком большой. Максимальный размер: 5MB', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            avatarImg.src = e.target.result;
        }
        reader.readAsDataURL(file);

        uploadAvatar(file);
    });

    function uploadAvatar(file) {
        const formData = new FormData();
        formData.append('avatar', file);

        uploadProgress.style.display = 'block';
        progressBar.style.width = '0%';

        fetch('/upload_avatar', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                avatarImg.src = data.avatar_url + '?t=' + new Date().getTime();
                progressBar.style.width = '100%';
                showNotification('Аватар успешно обновлен!', 'success');

                setTimeout(() => {
                    uploadProgress.style.display = 'none';
                }, 1000);
            } else {
                showNotification(data.error || 'Ошибка при загрузке', 'error');
                uploadProgress.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Ошибка при загрузке аватара', 'error');
            uploadProgress.style.display = 'none';
        });
    }

    function showNotification(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
        alertDiv.style.zIndex = '9999';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alertDiv);

        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }
});