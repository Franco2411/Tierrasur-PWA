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


let items = [];
// Agrego los items a la lista y los muestro en la pantalla
function addItem() {
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

    // Agregamos el item al array
    items.push({
        up: parseInt(up_name),
        lote: parseInt(lote_name),
        actividad: actividad_name,
        tipo: tablas_name,
        insumo: insumo_name,
        cant: parseFloat(quantity),
        precio: parseFloat(price)
    });

    renderItems();
   

    // Limpiar los campos de entrada después de agregar el ítem
    document.getElementById('cantidad').value = '';
    document.getElementById('precio').value = '';
    //document.getElementById('popupForm').style.display = 'none';
}

// Función para renderizar los items en la lista
function renderItems() {
    const itemList = document.getElementById('item-list');
    itemList.innerHTML = ''; // Limpiamos la lista

    items.forEach((item, index) => {
        const listItem = document.createElement('li');
        listItem.textContent = `UP: ${item.up} - Lote: ${item.lote} - Actividad: ${item.actividad} - Tipo: ${item.tipo} - Insumo/Labor: ${item.insumo} - Cantidad: ${item.cant} - Precio: ${item.precio}`;
        itemList.appendChild(listItem);
    });
}

// Funcion para enviar los datos al backend en un json
document.getElementById('submitForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Evitar que el formulario se envíe automáticamente
    enviarDatos(); // Llamar a la función enviarDatos
});

function enviarDatos() {
    console.log('Función enviarDatos llamada');
    if (items.length === 0) {
        //alert('No hay items para enviar');
        Swal.fire({
            icon: 'warning',
            title: 'No hay datos!',
            text: 'Debe cargar datos para poder enviarlos',
            confirmButtonText: 'Aceptar',
            //timer: 5000 // El mensaje se cierra automáticamente en 3 segundos
        });
        return;
    }

    const data = {
        order_id: document.getElementById('order-id') ? document.getElementById('order-id').value : null,
        items: items
    };

    console.log('Datos a enviar: ', data);

    fetch('/api/save_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            //alert('Datos guardados con éxito');
            Swal.fire({
                icon: 'success',
                title: 'Datos enviados!',
                text: 'Los datos se enviaron correctamente.',
                confirmButtonText: 'Aceptar',
                //timer: 5000 // El mensaje se cierra automáticamente en 3 segundos
            });
            
            
            itemList.innerHTML = ''; // Limpiamos la lista
            itemList = '';
        } else {
            console.log('Error al guardar la orden: ' + data.error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Ocurrió un problema al enviar los datos.',
                confirmButtonText: 'Intentar de nuevo'
            });
        }
    })
    .catch(error => console.error('Error: ', error));    
}



