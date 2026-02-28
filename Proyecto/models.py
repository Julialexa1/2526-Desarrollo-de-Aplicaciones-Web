import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "data.db"

class Producto:
    def __init__(self, id, nombre, tipo, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.cantidad = cantidad
        self.precio = precio

    def __repr__(self):
        return f"<Producto {self.nombre} ({self.tipo}) - ${self.precio:.2f}>"

class Inventario:
    def __init__(self):
        self._crear_tabla()

    def _crear_tabla(self):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def añadir_producto(self, nombre, tipo, cantidad, precio):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("INSERT INTO productos (nombre, tipo, cantidad, precio) VALUES (?, ?, ?, ?)",
                  (nombre, tipo, cantidad, precio))
        conn.commit()
        conn.close()

    def listar_todos(self):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM productos")
        filas = c.fetchall()
        conn.close()
        return [Producto(*fila) for fila in filas]

    def obtener_por_id(self, id):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM productos WHERE id=?", (id,))
        fila = c.fetchone()
        conn.close()
        return Producto(*fila) if fila else None

    def actualizar(self, id, nombre, tipo, cantidad, precio):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            UPDATE productos
            SET nombre=?, tipo=?, cantidad=?, precio=?
            WHERE id=?
        """, (nombre, tipo, cantidad, precio, id))
        conn.commit()
        conn.close()

    def eliminar(self, id):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("DELETE FROM productos WHERE id=?", (id,))
        conn.commit()
        conn.close()