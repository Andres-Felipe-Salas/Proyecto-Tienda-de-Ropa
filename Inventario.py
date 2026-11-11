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
        inicio, fin = 0, len(self.productos) - 1
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
        productos_ordenados = self.productos.copy()
        n = len(productos_ordenados)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                if productos_ordenados[j].precio > productos_ordenados[j + 1].precio:
                    productos_ordenados[j], productos_ordenados[j + 1] = productos_ordenados[j + 1], productos_ordenados[j]
        return productos_ordenados

    def ordenar_por_nombre(self):
        productos_ordenados = self.productos.copy()
        n = len(productos_ordenados)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                if productos_ordenados[j].nombre.lower() > productos_ordenados[j + 1].nombre.lower():
                    productos_ordenados[j], productos_ordenados[j + 1] = productos_ordenados[j + 1], productos_ordenados[j]
        return productos_ordenados

    def guardar_archivo(self, nombre_archivo):
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            for p in self.productos:
                archivo.write(f"{p.codigo};{p.nombre};{p.categoria};{p.talla};{p.precio};{p.cantidad}\n")

    def cargar_archivo(self, nombre_archivo):
        self.productos = []
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    datos = linea.split(";")
                    producto = Producto(int(datos[0]), datos[1], datos[2], datos[3], int(datos[4]), int(datos[5]))
                    self.productos.append(producto)
