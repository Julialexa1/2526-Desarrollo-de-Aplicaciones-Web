def leer_formulario(request):
    return {
        "nombre": request.form["nombre"],
        "precio": request.form["precio"],
        "stock": request.form["stock"]
    }