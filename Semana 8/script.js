// ===========================
// Interactividad con JavaScript
// ===========================

// Botón de alerta personalizada
const alertBtn = document.getElementById("alertBtn");
alertBtn.addEventListener("click", () => {
  alert("🚀 ¡Bienvenido a TechWorld! Explora nuestros productos innovadores.");
});

// Validación del formulario
const form = document.getElementById("contactForm");
const nombre = document.getElementById("nombre");
const correo = document.getElementById("correo");
const mensaje = document.getElementById("mensaje");
const errores = document.querySelectorAll(".error");

form.addEventListener("submit", (e) => {
  e.preventDefault(); // Evita envío inmediato
  let valido = true;

  // Limpiar errores previos
  errores.forEach(err => err.textContent = "");

  // Validar nombre
  if (nombre.value.trim().length < 3) {
    errores[0].textContent = "El nombre debe tener al menos 3 caracteres.";
    valido = false;
  }

  // Validar correo
  const regexCorreo = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
  if (!regexCorreo.test(correo.value.trim())) {
    errores[1].textContent = "Por favor, ingresa un correo válido.";
    valido = false;
  }

  // Validar mensaje
  if (mensaje.value.trim().length < 10) {
    errores[2].textContent = "El mensaje debe tener al menos 10 caracteres.";
    valido = false;
  }

  // Si todo es válido, mostrar confirmación
  if (valido) {
    alert("✅ ¡Formulario enviado con éxito!");
    form.reset();
  }
});
