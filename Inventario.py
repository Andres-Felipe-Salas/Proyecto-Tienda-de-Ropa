from Producto import Producto

class Inventario:

    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def mostrar_inventario(self):

        for producto in self.productos:
            print("----------------")
            producto.mostrar_producto()

    def buscar_producto_secuencial(self, codigo):

        for producto in self.productos:
            if producto.codigo == codigo:
                return producto

        return None

    def buscar_producto_binaria(self, codigo):

        inicio = 0
        fin = len(self.productos) - 1

        while inicio <= fin:

            medio = (inicio + fin) // 2

            if self.productos[medio].codigo == codigo:
                return self.productos[medio]

            elif self.productos[medio].codigo < codigo:
                inicio = medio + 1

            else:
                fin = medio - 1

        return None

    def ordenar_por_precio(self):

        productos_ordenados = []

        for producto in self.productos:
            productos_ordenados.append(producto)

        cantidad = len(productos_ordenados)

        for i in range(cantidad - 1):

            for j in range(cantidad - 1 - i):

                if productos_ordenados[j].precio > productos_ordenados[j + 1].precio:

                    temporal = productos_ordenados[j]
                    productos_ordenados[j] = productos_ordenados[j + 1]
                    productos_ordenados[j + 1] = temporal

        return productos_ordenados

    def ordenar_por_nombre(self):

        productos_ordenados = []

        for producto in self.productos:
            productos_ordenados.append(producto)

        cantidad = len(productos_ordenados)

        for i in range(cantidad - 1):

            for j in range(cantidad - 1 - i):

                if productos_ordenados[j].nombre.lower() > productos_ordenados[j + 1].nombre.lower():

                    temporal = productos_ordenados[j]
                    productos_ordenados[j] = productos_ordenados[j + 1]
                    productos_ordenados[j + 1] = temporal

        return productos_ordenados

    def guardar_archivo(self, nombre_archivo):

        with open(nombre_archivo, "w", encoding="utf-8") as archivo:

            for producto in self.productos:

                linea = (
                    f"{producto.get_codigo()};"
                    f"{producto.get_nombre()};"
                    f"{producto.get_categoria()};"
                    f"{producto.get_talla()};"
                    f"{producto.get_precio()};"
                    f"{producto.get_cantidad()}"
                    "\n"
                )

                archivo.write(linea)

    # cargar arch

    def cargar_archivo(self, nombre_archivo):

        self.productos = []

        with open(nombre_archivo, "r", encoding="utf-8") as archivo:

            for linea in archivo:

                linea = linea.rstrip("\n")

                if linea.strip() != "":

                    datos = linea.split(";")

                codigo = int(datos[0])
                nombre = datos[1]
                categoria = datos[2]
                talla = datos[3]
                precio = int(datos[4])
                cantidad = int(datos[5])


                producto = Producto(
                    codigo, nombre, categoria,
                    talla, precio, cantidad)

                self.productos.append(producto)