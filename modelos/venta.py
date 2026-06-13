from database import conectar

class Venta:

    def __init__(self):
        self.productos = []  # lista de tuplas (producto, cantidad)

    def agregar_producto(self, producto, cantidad):
        self.productos.append((producto, cantidad))

    def calcular_total(self):
        total = 0
        for producto, cantidad in self.productos:
            total += producto.precio * cantidad
        return total

    def guardar_venta(self):
        conexion = conectar()
        cursor = conexion.cursor()

        # Insertar cabecera de la venta
        total = self.calcular_total()
        sql_venta = "INSERT INTO ventas (total) VALUES (%s)"
        cursor.execute(sql_venta, (total,))
        venta_id = cursor.lastrowid

        # Insertar detalle de cada producto
        for producto, cantidad in self.productos:
            subtotal = producto.precio * cantidad
            sql_detalle = """
                INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (venta_id, producto.id, cantidad, producto.precio, subtotal)
            cursor.execute(sql_detalle, valores)

        conexion.commit()
        conexion.close()
