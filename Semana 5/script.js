// Referencias a elementos del DOM
const imageURL = document.getElementById("imageURL");
const addImageBtn = document.getElementById("addImageBtn");
const deleteImageBtn = document.getElementById("deleteImageBtn");
const gallery = document.getElementById("gallery");

let selectedImage = null; // Guarda la imagen seleccionada

// --- Agregar nueva imagen ---
addImageBtn.addEventListener("click", () => {
  const url = imageURL.value.trim();

  if (url === "") {
    alert("Por favor, ingresa una URL válida de imagen.");
    return;
  }

  // Crear un nuevo elemento <img>
  const newImg = document.createElement("img");
  newImg.src = url;
  newImg.alt = "Imagen agregada por el usuario";

  // Añadir evento para poder seleccionarla
  newImg.addEventListener("click", selectImage);

  // Agregar la imagen a la galería
  gallery.appendChild(newImg);

  // Limpiar el campo
  imageURL.value = "";
});

// --- Seleccionar una imagen ---
function selectImage(event) {
  // Si hay una imagen seleccionada, se deselecciona
  if (selectedImage) {
    selectedImage.classList.remove("selected");
  }

  // Marcar la nueva imagen seleccionada
  selectedImage = event.target;
  selectedImage.classList.add("selected");
}

// --- Eliminar imagen seleccionada ---
deleteImageBtn.addEventListener("click", () => {
  if (!selectedImage) {
    alert("Selecciona una imagen antes de eliminarla.");
    return;
  }

  // Remover la imagen del DOM
  gallery.removeChild(selectedImage);
  selectedImage = null;
});

// --- Evento: seleccionar imágenes existentes ---
document.querySelectorAll(".gallery img").forEach(img => {
  img.addEventListener("click", selectImage);
});

// --- Evento extra: presionar tecla "Delete" para borrar ---
document.addEventListener("keydown", (e) => {
  if (e.key === "Delete" && selectedImage) {
    gallery.removeChild(selectedImage);
    selectedImage = null;
  }
});
