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