# =========================
# modelos/producto.py
# =========================

from database import conectar

class Producto:

    def __init__(self, nombre, categoria, precio, stock):

        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    # =========================
    # CREAR PRODUCTO
    # =========================

    def crear_producto(self):

        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO productos
        (nombre, categoria, precio, stock, disponible)
        VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            self.nombre,
            self.categoria,
            self.precio,
            self.stock,
            True
        )

        cursor.execute(sql, valores)

        conexion.commit()
        conexion.close()

    # =========================
    # LISTAR PRODUCTOS
    # =========================

    @staticmethod
    def listar_productos():

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM productos")

        productos = cursor.fetchall()

        conexion.close()

        return productos

    # =========================
    # OBTENER PRODUCTO
    # =========================

    @staticmethod
    def obtener_producto(id):

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM productos WHERE id = %s",
            (id,)
        )

        producto = cursor.fetchone()

        conexion.close()

        return producto

    # =========================
    # EDITAR PRODUCTO
    # =========================

    def editar_producto(self, id):

        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
        UPDATE productos
        SET nombre = %s,
            categoria = %s,
            precio = %s,
            stock = %s
        WHERE id = %s
        """

        valores = (
            self.nombre,
            self.categoria,
            self.precio,
            self.stock,
            id
        )

        cursor.execute(sql, valores)

        conexion.commit()
        conexion.close()

    # =========================
    # ELIMINAR PRODUCTO
    # =========================

    @staticmethod
    def eliminar_producto(id):

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM productos WHERE id = %s",
            (id,)
        )

        conexion.commit()
        conexion.close()