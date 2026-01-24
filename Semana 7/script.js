// ===============================
// Lista Dinámica de Productos
// ===============================

// Arreglo inicial de productos
const productos = [
  { nombre: "Laptop HP", precio: 750, descripcion: "Portátil ideal para trabajo y estudio." },
  { nombre: "Smartphone Samsung", precio: 620, descripcion: "Pantalla AMOLED y excelente cámara." },
  { nombre: "Auriculares Bluetooth", precio: 80, descripcion: "Sonido envolvente y batería de larga duración." }
];

// Referencias al DOM
const lista = document.getElementById("productList");
const btnAgregar = document.getElementById("addProductBtn");

// --- Función para renderizar productos ---
function renderizarProductos() {
  lista.innerHTML = ""; // Limpiar contenido

  productos.forEach((producto, index) => {
    const item = document.createElement("li");

    item.innerHTML = `
      <strong>${index + 1}. ${producto.nombre}</strong><br>
      <span>💲 <b>${producto.precio}</b></span><br>
      <em>${producto.descripcion}</em>
    `;

    lista.appendChild(item);
  });
}

// --- Evento: agregar nuevo producto ---
btnAgregar.addEventListener("click", () => {
  const nuevoProducto = {
    nombre: `Producto ${productos.length + 1}`,
    precio: (Math.random() * 100 + 50).toFixed(2),
    descripcion: "Nuevo producto agregado dinámicamente al final de la lista."
  };

  productos.push(nuevoProducto);
  renderizarProductos();
});

// --- Render inicial ---
renderizarProductos();