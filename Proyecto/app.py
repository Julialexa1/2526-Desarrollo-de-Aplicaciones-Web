from flask import Flask, render_template, request, redirect, url_for, flash
from models import Inventario
import json
import csv
import os
from conexion.conexion import obtener_conexion

app = Flask(__name__)
app.secret_key = "rosita-2026"

inv = Inventario()

# RUTA DONDE SE GUARDARÁN LOS ARCHIVOS
DATA_PATH = "inventario/data"

TXT_FILE = os.path.join(DATA_PATH, "datos.txt")
JSON_FILE = os.path.join(DATA_PATH, "datos.json")
CSV_FILE = os.path.join(DATA_PATH, "datos.csv")


# ===============================
# PAGINA PRINCIPAL
# ===============================
@app.route('/')
def index():
    descripcion = (
        "Cafetería Rosita ofrece deliciosas tortillas artesanales elaboradas con "
        "harina de trigo, maíz, verde y yuca. También servimos café, chocolate, "
        "colas y jugos naturales. Ven y disfruta el sabor tradicional de Caluma."
    )
    return render_template("index.html", titulo="Inicio | Cafetería Rosita", descripcion=descripcion)


# ===============================
# PRODUCTOS
# ===============================
@app.route('/productos')
def productos():
    productos = inv.listar_todos()
    return render_template("productos.html", productos=productos, titulo="Productos | Cafetería Rosita")


# ===============================
# ABOUT
# ===============================
@app.route('/about')
def about():
    return render_template("about.html", titulo="Acerca de | Cafetería Rosita")


# ===============================
# INVENTARIO CRUD (SQLite)
# ===============================
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

    return render_template(
        "inventario.html",
        titulo="Inventario | Cafetería Rosita",
        productos=productos
    )


# ===============================
# EDITAR PRODUCTO
# ===============================
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

    return render_template(
        "editar_producto.html",
        producto=producto,
        titulo="Editar Producto | Cafetería Rosita"
    )


# ===============================
# ELIMINAR PRODUCTO
# ===============================
@app.route('/producto/eliminar/<int:id>')
def eliminar_producto(id):

    inv.eliminar(id)

    flash("Producto eliminado correctamente.", "success")

    return redirect(url_for('inventario'))


# =================================================
# GUARDAR DATOS EN TXT, JSON Y CSV
# =================================================
@app.route("/guardar_datos", methods=["POST"])
def guardar_datos():

    nombre = request.form["nombre"]
    precio = request.form["precio"]
    cantidad = request.form["cantidad"]

    os.makedirs(DATA_PATH, exist_ok=True)

    # -------- TXT --------
    with open(TXT_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(f"{nombre} - ${precio} - Cantidad: {cantidad}\n")

    # -------- JSON --------
    nuevo = {
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    }

    datos = []

    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except:
            datos = []

    datos.append(nuevo)

    with open(JSON_FILE, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)

    # -------- CSV --------
    archivo_existe = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as archivo:

        writer = csv.writer(archivo)

        if not archivo_existe:
            writer.writerow(["nombre", "precio", "cantidad"])

        writer.writerow([nombre, precio, cantidad])

    flash("Datos guardados en TXT, JSON y CSV correctamente", "success")

    return redirect(url_for("datos"))


# =================================================
# MOSTRAR DATOS GUARDADOS
# =================================================
@app.route("/datos")
def datos():

    txt_datos = []
    json_datos = []
    csv_datos = []

    # TXT
    if os.path.exists(TXT_FILE):
        with open(TXT_FILE, "r", encoding="utf-8") as archivo:
            txt_datos = archivo.readlines()

    # JSON
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as archivo:
            json_datos = json.load(archivo)

    # CSV
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            csv_datos = list(lector)

    return render_template(
        "datos.html",
        txt_datos=txt_datos,
        json_datos=json_datos,
        csv_datos=csv_datos
    )


# =================================================
# MYSQL
# =================================================
@app.route("/mysql/agregar_producto", methods=["POST"])
def mysql_agregar_producto():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    nombre = request.form["nombre"]
    tipo = request.form["tipo"]
    cantidad = request.form["cantidad"]
    precio = request.form["precio"]

    sql = """
    INSERT INTO productos(nombre,tipo,precio,stock)
    VALUES(%s,%s,%s,%s)
    """

    cursor.execute(sql, (nombre, tipo, precio, cantidad))

    conexion.commit()

    cursor.close()
    conexion.close()

    flash("Producto guardado en MySQL correctamente", "success")

    return redirect(url_for("mysql_productos"))


@app.route("/mysql/productos")
def mysql_productos():

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("mysql_productos.html", productos=productos)


@app.route("/mysql/eliminar/<int:id>")
def mysql_eliminar(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id_productos=%s", (id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    flash("Producto eliminado de MySQL", "success")

    return redirect(url_for("mysql_productos"))


# ===============================
# INICIAR APP
# ===============================
if __name__ == "__main__":
    app.run(debug=True)