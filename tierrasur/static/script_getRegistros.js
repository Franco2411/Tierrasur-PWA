// Funcion de abrir y cerrar el sidebar
document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const menuBtn = document.getElementById("menu-toggle");

    // Mostrar/Ocultar el menú al hacer clic en el botón
    menuBtn.addEventListener("click", () => {
        sidebar.classList.toggle("active");
    });

    // Cerrar el menú al hacer clic fuera de él
    document.addEventListener("click", (event) => {
        const isClickInsideSidebar = sidebar.contains(event.target);
        const isClickOnMenuButton = menuBtn.contains(event.target);

        if (!isClickInsideSidebar && !isClickOnMenuButton) {
            sidebar.classList.remove("active");
        }
    });
});

// Hago la peticion en la Pantalla de Mis Registros
document.addEventListener('DOMContentLoaded', function() {
    
    const [fecha1, fecha2] = obtener_dia()

    const requestFecha = new URLSearchParams(
        {
            fecha1: fecha1,
            fecha2: fecha2
        }
    );

    fetch(`/api/get_registers?${requestFecha.toString()}`)
        .then(response => response.json()) // Parsear la respuesta como JSON
        .then(data => {
            if (data.success) {
                if (Object.keys(data.data).length === 0 && data.constructor === Object) {
                    imagenNoDatos()
                } else {
                    contenedorRegistros(data.data)
                }                
                console.log('Entre al if del fetch')
            } else {
                console.log('Entre al else del fetch')
            }
            
        })
        .catch(error => console.error('Error:', error));
});

// Funcion para obtener el dia de la fecha
function obtener_dia() {
    const hoy = new Date();

    // Obtener el año, mes y día
    const year = hoy.getFullYear();
    const month = (hoy.getMonth() + 1).toString().padStart(2, '0'); // Los meses empiezan en 0, por eso sumamos 1
    const day = hoy.getDate().toString().padStart(2, '0'); // El día del mes

    const fecha1 = `${day}/${month}/${year}`;

    const year2 = hoy.getFullYear();
    const month2 = (hoy.getMonth() + 1).toString().padStart(2, '0'); // Los meses empiezan en 0, por eso sumamos 1
    const day2 = (hoy.getDate() + 1).toString().padStart(2, '0');

    const fecha2 = `${day2}/${month2}/${year2}`;

    return [fecha1, fecha2];
    
};

// Funcion para crear las vistas de los registros
function crearContenedorRegistros(data) {
    // Formateo la fecha que devuelve el backend
    const fec = formatearFecha(data.fecha)
    
    // Creo el contenedor principal
    const contenedor = document.createElement('div');
    contenedor.classList.add('carta');

    // Creo los elementos que van dentro
    const tituloPrincipal = document.createElement('h4');
    tituloPrincipal.classList.add('carta-header');
    tituloPrincipal.innerHTML = `Campaña ${data.campania} <span>${data.nro_c}</span>`;

    // Unidad productiva
    const uniProd = document.createElement('p');
    uniProd.innerHTML = `<b>UP:</b> ${data.up}`;
    
    // Lote
    const lote = document.createElement('p');
    lote.innerHTML = `<b>Lote:</b> ${data.lote}`;

    // Actividad
    const actividad = document.createElement('p');
    actividad.innerHTML = `<b>Actividad:</b> ${data.actividad}`;

    // Codigo
    const codigo = document.createElement('p');
    codigo.innerHTML = `<b>Tipo:</b> ${data.codigo}`;

    // Detalle
    const detalle = document.createElement('p');
    detalle.innerHTML = `<b>Insumo:</b> ${data.detalle}`;

    // Fecha
    const fecha = document.createElement('p');
    fecha.innerHTML = `<b>Fecha:</b> ${fec}`;

    // Fecha
    const cant = document.createElement('p');
    cant.innerHTML = `<b>Cantidad:</b> ${data.cantidad}`;

    // Agrego los elementos al contenedor principal
    contenedor.appendChild(tituloPrincipal);
    contenedor.appendChild(uniProd);
    contenedor.appendChild(lote);
    contenedor.appendChild(actividad);
    contenedor.appendChild(codigo);
    contenedor.appendChild(detalle);
    contenedor.appendChild(cant);
    contenedor.appendChild(fecha);

    // Inserto el contenido en el DOM
    document.getElementById('conteinerRegisters').appendChild(contenedor);
}

// Funcion para manejar registros múltiples
function contenedorRegistros(registros) {
    const contenedor = document.getElementById('conteinerRegisters');
    contenedor.innerHTML = '';

    // Recorro el array de registros
    registros.forEach(registro => {
        crearContenedorRegistros(registro);
    });
}

function imagenNoDatos() {
    const contenedor = document.getElementById('conteinerRegisters');
    
    const div_img = document.createElement('div');
    div_img.classList.add('div-img');

    const img = document.createElement('img');
    img.src = '/static/images/no_data.png';
    img.alt = 'No se encontraron datos.';
    
    div_img.appendChild(img);
    contenedor.appendChild(div_img);
}

// Funcion para formatear la fecha
function formatearFecha(fechaString) {
    // Creo un objeto Date con el string recibido
    const fecha = new Date(fechaString);
  
    // Obtengo el día, mes y año
    const dia = fecha.getDate().toString().padStart(2, '0'); // Asegurar dos dígitos
    const mes = (fecha.getMonth() + 1).toString().padStart(2, '0'); // Los meses van de 0 a 11, por eso sumamos 1
    const año = fecha.getFullYear();
  
    // Formateo la fecha como dd/mm/yyyy
    return `${dia}/${mes}/${año}`;
  }