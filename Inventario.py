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

    def buscar_producto(self, codigo):
        for producto in self.productos:
            if producto.codigo == codigo:
                return producto
        return None

    def ordenar_por_precio(self):
        return sorted(self.productos, key=lambda p: p.precio)

    def ordenar_por_nombre(self):
        return sorted(self.productos, key=lambda p: p.nombre.lower())

    def guardar_archivo(self, nombre_archivo):
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            for p in self.productos:
                archivo.write(f"{p.codigo};{p.nombre};{p.categoria};{p.talla};{p.precio};{p.cantidad}\n")

    def cargar_archivo(self, nombre_archivo):
        self.productos = []
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if linea := linea.strip():
                    datos = linea.split(";")
                    producto = Producto(int(datos[0]), datos[1], datos[2], datos[3], int(datos[4]), int(datos[5]))
                    self.productos.append(producto)
