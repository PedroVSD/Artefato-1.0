   //função para mostrar o conteúdo do textarea
   function showAlert(textarea) {
    alert(textarea.textContent);
}

//Previne a seleção de texto ao clicar em um textarea
document.querySelectorAll('textarea.no-select').forEach(textarea => {
    textarea.addEventListener('mousedown', function(event) {
        event.preventDefault();
    });
});

//Pega todos os elementos <td>
const tdElements = document.querySelectorAll('td');

//Muda a cor do texto para verde se o conteúdo for "Livre"
tdElements.forEach(td => {
    if (td.textContent == 'Livre') {
        td.style.color = 'lightgreen';
    }});

//Função para preselecionar o bloco
function preselectBloco() {
    const url = window.location.pathname;
    const match = url.match(/\/Blocos\/bloco:([A-Z])\//);
    if (match) {
        const bloco = match[1];
        const filterBloco = document.getElementById('filterBloco');
        filterBloco.value = bloco;
        const selectedInput = document.activeElement;

    }
}
function chargeUrl() {
    const selectedBloco = document.getElementById('filterBloco').value;
    const filterSala =  document.getElementById('filterSala').value;
    const filterAndar = document.getElementById('filterAndar').value;
    const filterDia = document.getElementById('filterDia').value;
    const queryString = `?bloco=${selectedBloco}&?sala=${filterSala}&andar=${filterAndar}&dia=${filterDia}`;
    const newUrl = `/Blocos/${queryString}`;
    history.pushState(null, '', newUrl);
}

//Função para recarregar a página com os filtros selecionados
function reloadPage() {
    const selectedBloco = document.getElementById('filterBloco').value;
    const filterSala = document.getElementById('filterSala').value;
    const filterAndar = document.getElementById('filterAndar').value;
    const filterDia = document.getElementById('filterDia').value;
    const queryString = `?bloco=${selectedBloco}&?sala=${filterSala}&andar=${filterAndar}&dia=${filterDia}`;
    window.location.href = `/Blocos/${queryString}`;
}

//É chamada quando a página é carregada
window.onload = function() {
    //preselectBloco();

    // Get the query parameters from the URL
    const urlParams = new URLSearchParams(window.location.search);
    
    // Get the values from the query parameters
    const bloco = urlParams.get('bloco');
    const sala = urlParams.get('sala');  
    const andar = urlParams.get('andar');
    const dia = urlParams.get('dia');

    // Set the values in the filters
    if (bloco != null && bloco != "") {
        document.getElementById('filterBloco').value = bloco;
    }
    else{
        document.getElementById('filterBloco').value = "";
        document.getElementById('salasTable').innerHTML = "<h1 class='text-light'>Selecione um bloco para visualizar as salas</h1>";
    }
    if (sala != null) {
        document.getElementById('filterSala').value = sala;
        if(document.getElementById('filterSala').value == '' && sala != "")
            reloadPage();
    }
    if (andar != null) {
        document.getElementById('filterAndar').value = andar;
        if((andar > 3 || andar < 1) && andar != ""){
            alert("Andar inválido, voltando para todos os andares");
            document.getElementById('filterAndar').value = "";
            const selectedBloco = document.getElementById('filterBloco').value;
            const filterSala = document.getElementById('filterSala').value;
            const filterAndar = document.getElementById('filterAndar').value;
            const filterDia = document.getElementById('filterDia').value;
            const queryString = `?sala=${filterSala}&andar=${filterAndar}&dia=${filterDia}`;
            window.location.href = `/Blocos/bloco:${selectedBloco}/${queryString}`;
        }
    }
    if (dia != null ) {
        document.getElementById('filterDia').value = dia;
        if(dia > 4 || dia < 0){
            alert("Dia inválido, voltando para segunda-feira");
            document.getElementById('filterDia').value = 0;
            const selectedBloco = document.getElementById('filterBloco').value;
            const filterSala = document.getElementById('filterSala').value;
            const filterAndar = document.getElementById('filterAndar').value;
            const filterDia = document.getElementById('filterDia').value;
            const queryString = `?sala=${filterSala}&andar=${filterAndar}&dia=${filterDia}`;
            window.location.href = `/Blocos/bloco:${selectedBloco}/${queryString}`;
        }
    } else{
        const currentDay = "{{ dia }}";
        document.getElementById('filterDia').value = currentDay;
    }
    filterTable();

    //Recarrega a cada meia hora
    setInterval(function() {
        location.reload();
    },  60000);

    //1 minuto = 60000
    //30 minutos = 1800000
}

// Filter function
function filterTable() {
    const filterSala = document.getElementById('filterSala').value.toLowerCase();
    const filterAndar = document.getElementById('filterAndar').value;
    
    const table = document.getElementById('salasTable');
    const trs = table.getElementsByTagName('tr');

    for (let i = 1; i < trs.length; i++) {
        const tds = trs[i].getElementsByTagName('td');
        const sala = tds[1].textContent.toLowerCase();
        const andar = sala.charAt(0);
        
        if ((filterSala === '' || sala.startsWith(filterSala)) &&
            (filterAndar === '' || andar === filterAndar)
            ) {
            trs[i].style.display = '';
        } else {
            trs[i].style.display = 'none';
        }
    }
}

// Attach filterTable function to input events
document.getElementById('filterSala').addEventListener('input', filterTable);
document.getElementById('filterAndar').addEventListener('change', filterTable);
