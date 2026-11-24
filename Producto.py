class Producto:
    def __init__(self, codigo, nombre, categoria, precio, tallas=None):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        # tallas es un diccionario: {'S': 10, 'M': 15, 'L': 20, 'XL': 5}
        self.tallas = tallas if tallas else {}

    def agregar_talla(self, talla, cantidad):
        """Agrega una nueva talla o aumenta el stock de una existente"""
        talla = talla.upper()
        if talla in self.tallas:
            self.tallas[talla] += cantidad
        else:
            self.tallas[talla] = cantidad
        return True

    def hay_disponibilidad(self, talla, cantidad_solicitada):
        """Verifica si hay stock disponible para una talla específica"""
        talla = talla.upper()
        return talla in self.tallas and self.tallas[talla] >= cantidad_solicitada

    def actualizar_stock(self, talla, cantidad_vendida):
        """Reduce el stock de una talla específica"""
        talla = talla.upper()
        if self.hay_disponibilidad(talla, cantidad_vendida):
            self.tallas[talla] -= cantidad_vendida
            return True
        return False

    def agregar_stock(self, talla, cantidad_agregar):
        """Agrega stock a una talla específica"""
        if cantidad_agregar > 0:
            return self.agregar_talla(talla, cantidad_agregar)
        return False

    def get_stock_total(self):
        """Retorna el stock total de todas las tallas"""
        return sum(self.tallas.values())

    def get_tallas_disponibles(self):
        """Retorna una lista de tallas que tienen stock"""
        return [talla for talla, cantidad in self.tallas.items() if cantidad > 0]

    def mostrar_producto(self):
        print(f"Codigo: {self.codigo}")
        print(f"Nombre: {self.nombre}")
        print(f"Categoria: {self.categoria}")
        print(f"Precio: ${self.precio}")
        if self.tallas:
            print(f"Tallas y Stock:")
            for talla, cantidad in sorted(self.tallas.items()):
                print(f"  - {talla}: {cantidad} unidades")
            print(f"Stock total: {self.get_stock_total()}")
        else:
            print("Sin tallas registradas")
