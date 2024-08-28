document.getElementById('campos_list').addEventListener('change', function() {
    let campos_id = this.value;
    
    // Limpiar la segunda lista antes de llenarla
    let segundaLista = document.getElementById('segunda-lista');
    segundaLista.innerHTML = '<option value="">Seleccione una opción</option>';
    
    if (campos_id) {
        fetch(`/combo_lotes?campos_id=${campos_id}`)
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                let option = document.createElement('option');
                option.value = item['numlot'];
                option.textContent = item['numlot'];
                segundaLista.appendChild(option);
            });
        });
    }
});

document.getElementById('tablas').addEventListener('change', function() {
    let tabla_id = this.value;
    
    // Limpiar la segunda lista antes de llenarla
    let insumoList = document.getElementById('insumo_labor');
    insumoList.innerHTML = '<option value="">Seleccione una opción</option>';
    
    if (tabla_id) {
        fetch(`/combo_insumo_labor?tabla_id=${tabla_id}`)
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                let option = document.createElement('option');
                option.value = item['id1'];
                option.textContent = item['nombre'];
                insumoList.appendChild(option);
            });
        });
    }
});
