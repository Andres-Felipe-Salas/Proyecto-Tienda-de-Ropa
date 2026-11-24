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
                tallas_str = ",".join([f"{talla}:{cantidad}" for talla, cantidad in p.tallas.items()])
                archivo.write(f"{p.codigo};{p.nombre};{p.categoria};{p.precio};{tallas_str}\n")

    def cargar_archivo(self, nombre_archivo):
        self.productos = []
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if linea := linea.strip():
                    datos = linea.split(";")
                    codigo = int(datos[0])
                    nombre = datos[1]
                    categoria = datos[2]
                    precio = int(datos[3])
                    
                    # Parsear tallas
                    tallas = {}
                    if len(datos) > 4 and datos[4]:
                        for talla_info in datos[4].split(","):
                            if ":" in talla_info:
                                talla, cantidad = talla_info.split(":")
                                tallas[talla.upper()] = int(cantidad)
                    
                    producto = Producto(codigo, nombre, categoria, precio, tallas)
                    self.productos.append(producto)

