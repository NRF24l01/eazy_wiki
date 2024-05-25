var markdown = "";

function send_markdown() {
    const data = markdown;
    fetch("/send_markdown", {
        method: 'POST',
        headers: {
            'Content-Type': 'text/plain'
        },
        body: data
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка HTTP: ' + response.status);
            }
            return response.text();
        })
        .then(data => {
            if (data === 'true') {
                console.log('Получен ответ true');
            } else if (data === 'false') {
                console.log('Получен ответ false');
            } else {
                console.log('Некорректный ответ');
            }
        })
        .catch(error => console.error('Ошибка:', error));
}