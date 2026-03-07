from flask import Flask, render_template, request, redirect, url_for, flash
from models import Inventario
import json
import csv
import os

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

@app.route("/guardar_txt", methods=["POST"])
def guardar_txt():

    ruta = "inventario/data/datos.txt"

    nombre = request.form["nombre"]
    precio = request.form["precio"]
    cantidad = request.form["cantidad"]

    linea = f"{nombre} - ${precio} - Cantidad: {cantidad}\n"

    with open(ruta, "a", encoding="utf-8") as archivo:
        archivo.write(linea)

    flash("Datos guardados en TXT correctamente", "success")

    return redirect(url_for("ver_datos"))

@app.route("/guardar_json", methods=["POST"])
def guardar_json():

    ruta = "inventario/data/datos.json"

    nombre = request.form["nombre"]
    precio = request.form["precio"]
    cantidad = request.form["cantidad"]

    nuevo = {
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    }

    datos = []

    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as archivo:
            try:
                datos = json.load(archivo)
            except:
                datos = []

    datos.append(nuevo)

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)

    flash("Datos guardados en JSON correctamente", "success")

    return redirect(url_for("ver_datos"))

@app.route("/guardar_csv", methods=["POST"])
def guardar_csv():

    ruta = "inventario/data/datos.csv"

    nombre = request.form["nombre"]
    precio = request.form["precio"]
    cantidad = request.form["cantidad"]

    archivo_existe = os.path.exists(ruta)

    with open(ruta, "a", newline="", encoding="utf-8") as archivo:

        campos = ["nombre", "precio", "cantidad"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)

        if not archivo_existe:
            escritor.writeheader()

        escritor.writerow({
            "nombre": nombre,
            "precio": precio,
            "cantidad": cantidad
        })

    flash("Datos guardados en CSV correctamente", "success")

    return redirect(url_for("ver_datos"))

@app.route("/datos")
def ver_datos():

    ruta = "inventario/data"

    txt_datos = []
    json_datos = []
    csv_datos = []

    # leer txt
    try:
        with open(f"{ruta}/datos.txt", "r", encoding="utf-8") as archivo:
            txt_datos = archivo.readlines()
    except:
        txt_datos = ["No hay datos TXT"]

    # leer json
    try:
        with open(f"{ruta}/datos.json", "r", encoding="utf-8") as archivo:
            json_datos = json.load(archivo)
    except:
        json_datos = []

    # leer csv
    try:
        with open(f"{ruta}/datos.csv", "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            csv_datos = list(lector)
    except:
        csv_datos = []

    return render_template(
        "datos.html",
        txt_datos=txt_datos,
        json_datos=json_datos,
        csv_datos=csv_datos
    )

if __name__ == "__main__":
    app.run(debug=True)