from database import conectar

class Reporte:
    @staticmethod
    def productos_sin_stock():
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, nombre, categoria, precio, stock
            FROM productos
            WHERE stock <= 0 OR disponible = 0
        """)
        resultados = cursor.fetchall()

        conexion.close()
        return resultados

    @staticmethod
    def ventas_del_dia():
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, fecha, total
            FROM ventas
            WHERE DATE(fecha) = CURDATE()
        """)
        resultados = cursor.fetchall()

        conexion.close()
        return resultados

    @staticmethod
    def detalle_ventas_del_dia():
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT v.id AS venta_id, v.fecha, p.nombre, dv.cantidad, dv.subtotal
            FROM ventas v
            JOIN detalle_ventas dv ON v.id = dv.venta_id
            JOIN productos p ON dv.producto_id = p.id
            WHERE DATE(v.fecha) = CURDATE()
        """)
        resultados = cursor.fetchall()

        conexion.close()
        return resultados
