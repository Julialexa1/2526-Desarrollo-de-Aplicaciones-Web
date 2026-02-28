from flask import Flask, render_template, request, redirect, url_for, flash
from models import Inventario

app = Flask(__name__)
app.secret_key = "rosita-2026"

inv = Inventario()

@app.route('/')
def index():
    descripcion = (
        "Cafetería Rosita ofrece deliciosas tortillas artesanales elaboradas con "
        "harina de trigo, maíz, verde y yuca. También servimos café, chocolate, "
        "colas y jugos naturales. Ven y disfruta el sabor tradicional de Caluma."
    )
    return render_template("index.html", titulo="Inicio | Cafetería Rosita", descripcion=descripcion)

@app.route('/productos')
def productos():
    productos = inv.listar_todos()
    return render_template("productos.html", productos=productos, titulo="Productos | Cafetería Rosita")

@app.route('/about')
def about():
    return render_template("about.html", titulo="Acerca de | Cafetería Rosita")

@app.route('/inventario', methods=['GET', 'POST'])
def inventario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo = request.form['tipo']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        inv.añadir_producto(nombre, tipo, cantidad, precio)
        flash(f"Producto '{nombre}' añadido correctamente.", "success")
        return redirect(url_for('inventario'))

    productos = inv.listar_todos()
    return render_template("inventario.html", titulo="Inventario | Cafetería Rosita", productos=productos)

@app.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = inv.obtener_por_id(id)
    if not producto:
        flash("Producto no encontrado", "danger")
        return redirect(url_for('inventario'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo = request.form['tipo']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        inv.actualizar(id, nombre, tipo, cantidad, precio)
        flash(f"Producto '{nombre}' actualizado correctamente.", "success")
        return redirect(url_for('inventario'))

    return render_template("editar_producto.html", producto=producto, titulo="Editar Producto | Cafetería Rosita")

@app.route('/producto/eliminar/<int:id>')
def eliminar_producto(id):
    inv.eliminar(id)
    flash("Producto eliminado correctamente.", "success")
    return redirect(url_for('inventario'))

if __name__ == "__main__":
    app.run(debug=True)