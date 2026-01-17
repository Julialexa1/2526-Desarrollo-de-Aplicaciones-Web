// Referencias al DOM
const form = document.getElementById('registroForm');
const nombre = document.getElementById('nombre');
const email = document.getElementById('email');
const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirmPassword');
const edad = document.getElementById('edad');
const btnEnviar = document.getElementById('btnEnviar');
const errorElements = document.querySelectorAll('.error');

// Validación individual de cada campo
function validarNombre() {
  if (nombre.value.trim().length < 3) {
    mostrarError(nombre, "El nombre debe tener al menos 3 caracteres");
    return false;
  }
  limpiarError(nombre);
  return true;
}

function validarEmail() {
  const regexEmail = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
  if (!regexEmail.test(email.value.trim())) {
    mostrarError(email, "Ingresa un correo electrónico válido");
    return false;
  }
  limpiarError(email);
  return true;
}

function validarPassword() {
  const regexPass = /^(?=.*[0-9])(?=.*[!@#$%^&*.-_]).{8,}$/;
  if (!regexPass.test(password.value.trim())) {
    mostrarError(password, "La contraseña debe tener al menos 8 caracteres, un número y un símbolo");
    return false;
  }
  limpiarError(password);
  return true;
}

function validarConfirmPassword() {
  if (confirmPassword.value.trim() !== password.value.trim()) {
    mostrarError(confirmPassword, "Las contraseñas no coinciden");
    return false;
  }
  limpiarError(confirmPassword);
  return true;
}

function validarEdad() {
  const edadValor = parseInt(edad.value);
  if (isNaN(edadValor) || edadValor < 18) {
    mostrarError(edad, "Debes tener al menos 18 años");
    return false;
  }
  limpiarError(edad);
  return true;
}

// Mostrar y limpiar errores
function mostrarError(input, mensaje) {
  const errorElement = input.nextElementSibling;
  errorElement.textContent = mensaje;
  input.style.borderColor = "#dc3545";
}

function limpiarError(input) {
  const errorElement = input.nextElementSibling;
  errorElement.textContent = "";
  input.style.borderColor = "#28a745";
}

// Función para validar todo el formulario
function validarFormulario() {
  const valido =
    validarNombre() &&
    validarEmail() &&
    validarPassword() &&
    validarConfirmPassword() &&
    validarEdad();

  btnEnviar.disabled = !valido;
}

// --- Eventos dinámicos ---
form.addEventListener("input", validarFormulario);

form.addEventListener("submit", (e) => {
  e.preventDefault();
  if (!btnEnviar.disabled) {
    alert("✅ Formulario enviado correctamente. ¡Registro exitoso!");
    form.reset();
    btnEnviar.disabled = true;
    errorElements.forEach(err => err.textContent = "");
  }
});

form.addEventListener("reset", () => {
  errorElements.forEach(err => err.textContent = "");
  btnEnviar.disabled = true;
});
