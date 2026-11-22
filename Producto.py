class Producto:
    def __init__(self, codigo, nombre, categoria, talla, precio, cantidad):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.talla = talla
        self.precio = precio
        self.cantidad = cantidad

    def hay_disponibilidad(self, cantidad_solicitada):
        return self.cantidad >= cantidad_solicitada

    def actualizar_stock(self, cantidad_vendida):
        if self.hay_disponibilidad(cantidad_vendida):
            self.cantidad -= cantidad_vendida
            return True
        return False

    def agregar_stock(self, cantidad_agregar):
        if cantidad_agregar > 0:
            self.cantidad += cantidad_agregar
            return True
        return False

    def mostrar_producto(self):
        print(f"Codigo: {self.codigo}")
        print(f"Nombre: {self.nombre}")
        print(f"Categoria: {self.categoria}")
        print(f"Talla: {self.talla}")
        print(f"Precio: {self.precio}")
        print(f"Cantidad: {self.cantidad}")
