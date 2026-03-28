from conexion.conexion import obtener_conexion

def listar():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()
    conexion.close()
    return datos


def insertar(nombre, precio, stock):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO productos(nombre,precio,stock) VALUES(%s,%s,%s)",
        (nombre, precio, stock)
    )

    conexion.commit()
    conexion.close()


def obtener(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos WHERE id_producto=%s", (id,))
    dato = cursor.fetchone()

    conexion.close()
    return dato


def actualizar(id, nombre, precio, stock):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "UPDATE productos SET nombre=%s, precio=%s, stock=%s WHERE id_producto=%s",
        (nombre, precio, stock, id)
    )

    conexion.commit()
    conexion.close()


def eliminar(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE id_producto=%s", (id,))
    conexion.commit()
    conexion.close()