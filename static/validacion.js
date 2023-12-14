
    function validarRespuestas() {
        const preguntas = document.querySelectorAll('.pregunta');
        let sinRespuesta = false;
    
        preguntas.forEach(pregunta => {
            const radios = pregunta.querySelectorAll('input[type="radio"]:checked');
    
            if (radios.length === 0) {
                sinRespuesta = true;
                marcarPreguntaSinRespuesta(pregunta);
            } else {
                eliminarMensajeValidacion(pregunta);
            }
        });
    
        mostrarOcultarMensajeValidacion(sinRespuesta);
    
        return !sinRespuesta;
    }
    
    function marcarPreguntaSinRespuesta(pregunta) {
        if (!pregunta.classList.contains('pregunta-sin-respuesta')) {
            pregunta.classList.add('pregunta-sin-respuesta');
    
            const mensaje = document.createElement('span');
            mensaje.textContent = ' (Falta responder esta pregunta)';
            mensaje.classList.add('validation-message');
    
            pregunta.querySelector('td').appendChild(mensaje);
        }
    }
    
    function eliminarMensajeValidacion(pregunta) {
        if (pregunta.classList.contains('pregunta-sin-respuesta')) {
            pregunta.classList.remove('pregunta-sin-respuesta');
            const mensaje = pregunta.querySelector('.validation-message');
            if (mensaje) {
                mensaje.remove();
            }
        }
    }
    
    function mostrarOcultarMensajeValidacion(sinRespuesta) {
        const mensaje = document.getElementById('validation-summary');
        mensaje.textContent = 'Por favor, responde todas las preguntas antes de continuar.';
        mensaje.style.display = sinRespuesta ? 'block' : 'none';
    }
