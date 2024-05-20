// Inicialización del carrusel Swiper con autoplay
var mySwiper = new Swiper('.mySwiper', {
    loop: true,
    autoplay: {
        delay: 2500,

        // Continúa después de la interacción del usuario
        disableOnInteraction: false  
    },
    pagination: {
        el: '.swiper-pagination'
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev'
    }
});

 //Modal términos y condiciones
document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('termsModal');
    var acceptButton = document.getElementById('acceptTerms');

    // Verificar si el usuario ya ha aceptado los términos
    if (localStorage.getItem('termsAccepted') !== 'true') {
        modal.style.display = 'block';
    } else {
        modal.style.display = 'none';
    }

    // Manejar clic en el botón de aceptar
    acceptButton.addEventListener('click', function() {
        modal.style.display = 'none';
        // Guardar en localStorage que los términos han sido aceptados
        localStorage.setItem('termsAccepted', 'true');
    });
});

 //Función para actualizar el gráfico según el departamento seleccionado
function updateChart() {
    const department = document.getElementById('department-select').value;
    document.getElementById('chart-image').src = `/chart?department=${department}`;
}


