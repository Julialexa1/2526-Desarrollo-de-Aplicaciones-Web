from flask import Flask, render_template, request, redirect, url_for, flash
from models import Inventario
import json
import csv
import os
from conexion.conexion import obtener_conexion
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import obtener_usuario_por_email, obtener_usuario_por_id
from services.producto_service import *
from forms.producto_form import leer_formulario
from fpdf import FPDF
from services.producto_service import listar
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import send_file
import io
from flask import make_response
from flask_login import login_required

app = Flask(__name__)
app.secret_key = "rosita-2026"

# ===============================
# CONFIG LOGIN
# ===============================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return obtener_usuario_por_id(user_id)

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
# LOGIN
# ===============================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        usuario = obtener_usuario_por_email(email)

        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            flash("Bienvenido 👋", "success")
            return redirect(url_for("index"))
        else:
            flash("Correo o contraseña incorrectos", "danger")

    return render_template("login.html")

# ===============================
# REGISTRO
# ===============================
@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO usuarios(nombre,email,password) VALUES(%s,%s,%s)",
            (nombre, email, password)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

        flash("Usuario registrado correctamente", "success")
        return redirect(url_for("login"))

    return render_template("registro.html")

# ===============================
# LOGOUT
# ===============================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "success")
    return redirect(url_for("login"))

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
@login_required
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
@login_required
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
@login_required
def eliminar_producto(id):

    inv.eliminar(id)

    flash("Producto eliminado correctamente.", "success")

    return redirect(url_for('inventario'))


# =================================================
# GUARDAR DATOS EN TXT, JSON Y CSV
# =================================================
@app.route("/guardar_datos", methods=["POST"])
@login_required
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
@login_required
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
@login_required
def mysql_productos():

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("mysql_productos.html", productos=productos)


@app.route("/mysql/eliminar/<int:id>")
@login_required
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
# CRUD MYSQL NUEVO
# ===============================

@app.route("/crud")
@login_required
def crud():
    productos = listar()
    return render_template("crud/listar.html", productos=productos)


@app.route("/crud/crear", methods=["GET", "POST"])
@login_required
def crear():

    if request.method == "POST":
        datos = leer_formulario(request)
        insertar(datos["nombre"], datos["precio"], datos["stock"])
        flash("Producto creado", "success")
        return redirect(url_for("crud"))

    return render_template("crud/crear.html")


@app.route("/crud/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):

    if request.method == "POST":
        datos = leer_formulario(request)
        actualizar(id, datos["nombre"], datos["precio"], datos["stock"])
        flash("Actualizado", "success")
        return redirect(url_for("crud"))

    producto = obtener(id)
    return render_template("crud/editar.html", producto=producto)


@app.route("/crud/eliminar/<int:id>")
@login_required
def eliminar_crud(id):
    eliminar(id)
    flash("Eliminado", "success")
    return redirect(url_for("crud"))

# ===============================
# REPORTE PDF
# ===============================

@app.route("/pdf")
@login_required
def pdf():

    productos = listar()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="REPORTE PRODUCTOS", ln=True)

    for p in productos:
        pdf.cell(200, 10, txt=f"{p['nombre']} - ${p['precio']} - Stock: {p['stock']}", ln=True)

    pdf.output("reporte.pdf")

    return "PDF generado correctamente"


@app.route("/reporte/pdf")
@login_required
def generar_pdf():

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    pdf = FPDF()
    pdf.add_page()

    # ====== TÍTULO ======
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "REPORTE DE PRODUCTOS", ln=True, align="C")

    pdf.ln(5)

    # ====== SUBTÍTULO ======
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, "Cafetería Rosita", ln=True, align="C")

    pdf.ln(10)

    # ====== ENCABEZADO TABLA ======
    pdf.set_font("Arial", "B", 10)

    pdf.cell(20, 10, "ID", border=1, align="C")
    pdf.cell(60, 10, "Nombre", border=1, align="C")
    pdf.cell(30, 10, "Precio", border=1, align="C")
    pdf.cell(30, 10, "Stock", border=1, align="C")
    pdf.ln()

    # ====== FILAS ======
    pdf.set_font("Arial", "", 10)

    for p in productos:
        pdf.cell(20, 10, str(p["id_producto"]), border=1, align="C")
        pdf.cell(60, 10, p["nombre"], border=1)
        pdf.cell(30, 10, f"${p['precio']}", border=1, align="C")
        pdf.cell(30, 10, str(p["stock"]), border=1, align="C")
        pdf.ln()

    # ====== PIE DE PÁGINA ======
    pdf.ln(10)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, "Generado automáticamente - Cafetería Rosita", align="C")

    response = make_response(pdf.output(dest="S").encode("latin-1"))
    response.headers.set("Content-Type", "application/pdf")
    response.headers.set("Content-Disposition", "attachment", filename="reporte_productos.pdf")

    return response

# ===============================
# INICIAR APP
# ===============================
if __name__ == "__main__":
    app.run(debug=True)