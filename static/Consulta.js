document.addEventListener('DOMContentLoaded', function() {
    var logoutLink = document.getElementById('logoutLink');
    
    // Função para obter valores únicos de uma coluna
    function getUniqueValuesFromColumn(columnClass) {
        var values = [];
        document.querySelectorAll('.' + columnClass).forEach(function(cell) {
            var text = cell.textContent.trim();
            if (!values.includes(text)) {
                values.push(text);
            }
        });
        return values;
    }

    // Preencher os selects com valores únicos
    function populateSelect(selectId, values) {
        var select = document.getElementById(selectId);
        values.forEach(function(value) {
            var option = document.createElement('option');
            option.value = value;
            option.text = value;
            select.appendChild(option);
        });
    }

    var locais = getUniqueValuesFromColumn('local');
    var dias = getUniqueValuesFromColumn('dia');
    var respostas = getUniqueValuesFromColumn('resposta');
    var horas = getUniqueValuesFromColumn('hora');

    populateSelect('filterLocal', locais);
    populateSelect('filterDia', dias);
    populateSelect('filterResposta', respostas);
    populateSelect('filterHora', horas);

    // Filtrar a tabela
    function filterTable() {
        var filterLocal = document.getElementById('filterLocal').value.toLowerCase();
        var filterDia = document.getElementById('filterDia').value.toLowerCase();
        var filterResposta = document.getElementById('filterResposta').value.toLowerCase();
        var filterHora = document.getElementById('filterHora').value.toLowerCase();

        document.querySelectorAll('#agendamentosTable tbody tr').forEach(function(row) {
            var local = row.querySelector('.local').textContent.toLowerCase();
            var dia = row.querySelector('.dia').textContent.toLowerCase();
            var resposta = row.querySelector('.resposta').textContent.toLowerCase().trim();
            var hora = row.querySelector('.hora').textContent.toLowerCase();

            var showRow = (!filterLocal || local.includes(filterLocal)) &&
                          (!filterDia || dia.includes(filterDia)) && 
                          (!filterHora || hora.includes(filterHora)) &&
                          (!filterResposta || resposta.startsWith(filterResposta));

            row.style.display = showRow ? '' : 'none';
        });
    }

    // Adicionar evento de mudança nos selects
    document.getElementById('filterLocal').addEventListener('change', filterTable);
    document.getElementById('filterDia').addEventListener('change', filterTable);
    document.getElementById('filterResposta').addEventListener('change', filterTable);
    document.getElementById('filterHora').addEventListener('change', filterTable);
});