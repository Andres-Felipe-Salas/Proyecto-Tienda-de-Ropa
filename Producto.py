class Producto:

    def __init__(self, codigo, nombre, categoria, talla, precio, cantidad):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.talla = talla
        self.precio = precio
        self.cantidad = cantidad

    def get_codigo(self):
        return self.codigo

    def get_nombre(self):
        return self.nombre

    def get_categoria(self):
        return self.categoria

    def get_talla(self):
        return self.talla

    def get_precio(self):
        return self.precio

    def get_cantidad(self):
        return self.cantidad

    def hay_disponibilidad(self, cantidad_solicitada):
        return self.cantidad >= cantidad_solicitada

    def actualizar_stock(self, cantidad_vendida):
        if self.hay_disponibilidad(cantidad_vendida):
            self.cantidad -= cantidad_vendida
            return True
        return False

    def mostrar_producto(self):
        print("Codigo:", self.codigo)
        print("Nombre:", self.nombre)
        print("Categoria:", self.categoria)
        print("Talla:", self.talla)
        print("Precio:", self.precio)
        print("Cantidad:", self.cantidad)
