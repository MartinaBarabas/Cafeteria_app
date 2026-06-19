from flask import Flask, render_template, request
import json
from modelos.producto import Producto
from modelos.venta import Venta
from modelos.reporte import Reporte   

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("Home.html")

# ---------------- INVENTARIO ----------------
@app.route("/crear", methods=["GET", "POST"])
def crear_producto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])

        nuevo_producto = Producto(
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock
        )
        nuevo_producto.crear_producto()
        return render_template("Inventario.html", productos=Producto.listar_productos())

    return render_template("crear_producto.html")

@app.route("/inventario")
def inventario():
    productos = Producto.listar_productos()
    return render_template("Inventario.html", productos=productos)

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])

        producto = Producto(
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock
        )
        producto.editar_producto(id)
        return render_template("Inventario.html", productos=Producto.listar_productos())

    producto = Producto.obtener_producto(id)
    return render_template("editar_producto.html", producto=producto)

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_producto(id):
    Producto.eliminar_producto(id)
    return render_template("Inventario.html", productos=Producto.listar_productos())

# ---------------- VENTAS ----------------
@app.route("/venta", methods=["GET", "POST"])
def venta():
    if request.method == "POST":
        productos_json = request.form.get("productos_json")
        productos_lista = json.loads(productos_json) if productos_json else []

        if not productos_lista:
            return render_template("venta.html", productos=Producto.listar_productos(), error="No se seleccionaron productos")

        venta = Venta()
        for item in productos_lista:
            producto_id = int(item["id"])
            cantidad = int(item["cantidad"])
            datos = Producto.obtener_producto(producto_id)

            if datos.stock < cantidad:
                return render_template("venta.html", productos=Producto.listar_productos(), error=f"Stock insuficiente para {datos.nombre}")

            producto = Producto(
                id_producto=datos.id,
                nombre=datos.nombre,
                categoria=datos.categoria,
                precio=datos.precio,
                stock=datos.stock - cantidad,
                disponible=datos.disponible
            )

            venta.agregar_producto(producto, cantidad)
            producto.editar_producto(producto_id)

        venta.guardar_venta()
        venta.productos = []

        return render_template("venta.html", productos=Producto.listar_productos(), success=True)

    productos = Producto.listar_productos()
    return render_template("venta.html", productos=productos)

# ---------------- REPORTES ----------------
@app.route("/reportes")
def reportes():
    return render_template("reportes.html")

@app.route("/reportes/productos")
def reporte_productos():
    productos = Reporte.productos_sin_stock()
    return render_template("reportes_productos.html", productos=productos)

@app.route("/reportes/ventas")
def reporte_ventas():
    detalle = Reporte.detalle_ventas_del_dia()
    return render_template("reportes_ventas.html", detalle=detalle)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=True)
