from flask import Flask, render_template

app = Flask(__name__)

# Ruta principal
@app.route('/')
def inicio():
    return render_template('index.html', titulo="Inicio | Cafetería Rosita")

# Ruta "Acerca de"
@app.route('/about')
def about():
    return render_template('about.html', titulo="Acerca de | Cafetería Rosita")

# Ruta de productos
@app.route('/productos')
def productos():
    lista_productos = [
        {"nombre": "Capuccino", "precio": 2.50},
        {"nombre": "Latte", "precio": 2.00},
        {"nombre": "Brownie", "precio": 1.50}
    ]
    return render_template('productos.html', titulo="Productos | Cafetería Rosita", productos=lista_productos)

if __name__ == '__main__':
    app.run(debug=True)