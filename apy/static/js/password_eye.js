/**
 * Lógica para mostrar/ocultar contraseñas
 * Busca elementos con la clase .toggle-password y cambia el type del input hermano
 */
document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.toggle-password');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Esto busca el input dentro del mismo contenedor 'position-relative'
            const container = this.closest('.position-relative');
            const input = container.querySelector('input');
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.replace('fa-eye', 'fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.replace('fa-eye-slash', 'fa-eye');
            }
        });
    });
});