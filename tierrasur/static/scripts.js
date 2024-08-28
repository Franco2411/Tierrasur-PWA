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


// Funcion de adición de items a la lista de la orden
document.getElementById('openFormButton').addEventListener('click', function() {
    document.getElementById('popupForm').style.display = 'flex';
});

document.getElementById('closeFormButton').addEventListener('click', function() {
    document.getElementById('popupForm').style.display = 'none';
});


function addItem() {
    const itemList = document.getElementById('item-list');
    // UP
    const upSelect = document.getElementById('campos_list');
    const up_name = upSelect.options[upSelect.selectedIndex].text;

    // Lote
    const loteSelect = document.getElementById('segunda-lista');
    const lote_name = loteSelect.options[loteSelect.selectedIndex].text;

    // Actividad
    const actividadSelect = document.getElementById('actividad_list');
    const actividad_name = actividadSelect.options[actividadSelect.selectedIndex].text;

    // Tablas
    const tablasSelect = document.getElementById('tablas');
    const tablas_name = tablasSelect.options[tablasSelect.selectedIndex].text;

    // Insumos
    const insumoSelect = document.getElementById('insumo_labor');
    const insumo_name = insumoSelect.options[insumoSelect.selectedIndex].text;
    
    const quantity = document.getElementById('cantidad').value;
    const price = document.getElementById('precio').value;

    if (!quantity) {
        alert("Debe de colocar la cantidad");
        return;
    }

    // Crear un nuevo ítem en la lista
    const item = document.createElement('li');
    item.textContent = `UP: ${up_name} - Lote: ${lote_name} - Actividad: ${actividad_name} - Tipo: ${tablas_name} - Insumo/Labor: ${insumo_name} - Cantidad: ${quantity} - Precio: ${price}`;
    
    // Crear un input oculto para enviar los datos del ítem
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'items[]';
    input.value = `${up_name},${lote_name},${actividad_name},${tablas_name},${insumo_name},${quantity},${price}`;
    
    // Añadir el input y el ítem a la lista
    item.appendChild(input);
    itemList.appendChild(item);

    // Limpiar los campos de entrada después de agregar el ítem
    document.getElementById('cantidad').value = '';
    document.getElementById('precio').value = '';
    //document.getElementById('popupForm').style.display = 'none';
}

