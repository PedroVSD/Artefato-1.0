function updateSalas() {
    const bloco = document.getElementById('bloco').value;
    const dia_semana = document.getElementById('dia_semana').value;

    if(bloco != 'Escolha um Bloco' && dia_semana != 'Escolha um Dia da Semana') {
        fetch('/get_salas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ bloco: bloco })
        })
        .then(response => response.json())
        .then(data => {
            const salaSelect = document.getElementById('sala');
            salaSelect.innerHTML = '<option selected>Escolha uma Sala</option>'; // Reset options
            data.forEach(dado => {
                dado.hora.forEach((hora, index) => {
                    if (hora === 'Livre' && dado.dia == dia_semana) {
                        const option = document.createElement('option');
                        option.value = `${dado.sala} ${dado.n_hora[index]}`;
                        option.text = `${dado.sala} - ${dado.semana} - ${dado.n_hora[index]}`;
                        salaSelect.appendChild(option);
                    }
                });
            });
            checkSala();
        });
    }
    else{
        const salaSelect = document.getElementById('sala');
        salaSelect.innerHTML = '<option selected>Escolha uma Sala</option>'; // Reset options
    }
}

function checkSala() {
    const salaSelect = document.getElementById('sala');
    const submitButton = document.getElementById('submitButton');
    if (salaSelect.value !== 'Escolha uma Sala' && salaSelect.value !== '') {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}

var backLink = document.getElementById('backLink');
if (backLink) {
    backLink.addEventListener('click', function (event) {
    event.preventDefault(); // Prevent the default link behavior
    var confirmation = confirm('Você tem certeza que deseja sair?');
    if (confirmation) {
        window.location.href = '/Profile'; // Redirect to the logout URL
    }
    });
}

var logoutLink = document.getElementById('logoutLink');

if (logoutLink){
    logoutLink.addEventListener('click', function (event) {
    event.preventDefault(); // Prevent the default link behavior
    var confirmation = confirm('Você tem certeza que deseja sair?');
    if (confirmation) {
        window.location.href = '/logout'; // Redirect to the logout URL
    }
    });
}