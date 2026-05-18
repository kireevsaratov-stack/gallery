document.addEventListener('DOMContentLoaded', function() {
    // Находим все поля загрузки файлов в инлайнах
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach(function(input) {
        // Заменяем single на multiple
        input.setAttribute('multiple', '');

        // При выборе нескольких файлов — создаём новые поля
        input.addEventListener('change', function(e) {
            const files = Array.from(e.target.files);

            if (files.length > 1) {
                e.preventDefault();

                // Берём первый файл для текущего поля
                const firstFile = files.shift();
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(firstFile);
                input.files = dataTransfer.files;

                // Для остальных файлов ищем пустые поля
                files.forEach(function(file, index) {
                    setTimeout(function() {
                        const allInputs = document.querySelectorAll('input[type="file"]');
                        for (let inp of allInputs) {
                            if (!inp.files || inp.files.length === 0) {
                                const dt = new DataTransfer();
                                dt.items.add(file);
                                inp.files = dt.files;
                                inp.dispatchEvent(new Event('change', { bubbles: true }));
                                break;
                            }
                        }
                    }, index * 100);
                });
            }
        });
    });
});