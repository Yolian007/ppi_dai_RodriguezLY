function toggleMenu() {
    document.getElementById("userDropdown").classList.toggle("show");
}

// Cierra el menú si el usuario hace clic fuera de él
window.onclick = function(event) {
    if (!event.target.matches('.user-icon img')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

function toggleMenu() {
    var dropdown = document.getElementById("userDropdown");
    if (dropdown.style.display === "none" || dropdown.style.display === "") {
        dropdown.style.display = "block";
    } else {
        dropdown.style.display = "none";
    }
}

// mi perfil.html
function openModal() {
    document.getElementById('createEventModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('createEventModal').style.display = 'none';
}

function openEventModal(name, date, department, municipality, address, type, participants, duration, description) {
    document.getElementById('event-title').innerText = name;
    document.getElementById('event-date').innerText = `Fecha: ${date}`;
    document.getElementById('event-location').innerText = `Ubicación: ${address}, ${municipality}, ${department}`;
    document.getElementById('event-type').innerText = `Tipo: ${type}`;
    document.getElementById('event-participants').innerText = `Participantes: ${participants}`;
    document.getElementById('event-duration').innerText = `Duración: ${duration} horas`;
    document.getElementById('event-description').innerText = `Descripción: ${description}`;

    
    // Rellenar el formulario de edición con los datos del evento
    document.getElementById('edit_event_name').value = name;
    document.getElementById('edit_event_date').value = date;
    document.getElementById('edit_department').value = department;
    document.getElementById('edit_municipality').value = municipality;
    document.getElementById('edit_address').value = address;
    document.getElementById('edit_event_type').value = type;
    document.getElementById('edit_num_participants').value = participants;
    document.getElementById('edit_event_duration').value = duration;
    document.getElementById('edit_event_description').value = description;

    document.getElementById('eventDetailsModal').style.display = 'block';
}

function closeEventModal() {
    document.getElementById('eventDetailsModal').style.display = 'none';
}
