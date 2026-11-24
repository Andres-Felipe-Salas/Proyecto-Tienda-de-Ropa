class Venta:
    IVA_PORCENTAJE = 0.19

    def __init__(self, numero_venta, cliente):
        self.numero_venta = numero_venta
        self.cliente = cliente
        self.items = []
        self.subtotal_sin_iva = 0
        self.total_iva = 0
        self.total = 0

    def agregar_item(self, producto, talla, cantidad):
        if not producto.hay_disponibilidad(talla, cantidad):
            return False
        
        precio_base = producto.precio / (1 + self.IVA_PORCENTAJE)
        iva_unitario = producto.precio - precio_base
        
        item = {
            'producto': producto,
            'talla': talla.upper(),
            'cantidad': cantidad,
            'precio_base': round(precio_base, 2),
            'iva_unitario': round(iva_unitario, 2),
            'subtotal_base': round(precio_base * cantidad, 2),
            'subtotal_iva': round(iva_unitario * cantidad, 2),
            'subtotal': round(producto.precio * cantidad, 2)
        }
        self.items.append(item)
        return True

    def calcular_total(self):
        self.subtotal_sin_iva = sum(item['subtotal_base'] for item in self.items)
        self.total_iva = sum(item['subtotal_iva'] for item in self.items)
        self.total = sum(item['subtotal'] for item in self.items)
        return self.total

    def registrar_venta(self):
        if not self.items:
            return False
        
        for item in self.items:
            if not item['producto'].actualizar_stock(item['talla'], item['cantidad']):
                return False
        
        self.calcular_total()
        return True

    def mostrar_venta(self):
        print(f"N° Venta : {self.numero_venta}")
        print(f"Cliente  : {self.cliente.nombre} (ID: {self.cliente.identificacion})")
        print("\nItems:")
        print(f"{'Producto':<20} {'Talla':>6} {'Cant':>4} {'P.Base':>10} {'IVA':>10} {'Subtotal':>10}")
        print("-" * 70)
        for item in self.items:
            prod = item['producto']
            print(f"{prod.nombre:<20} {item['talla']:>6} {item['cantidad']:>4} ${item['subtotal_base']:>9.2f} ${item['subtotal_iva']:>9.2f} ${item['subtotal']:>9.2f}")
        print("-" * 70)
        print(f"{'SUBTOTAL (sin IVA):':<55} ${self.subtotal_sin_iva:>9.2f}")
        print(f"{'IVA (19%):':<55} ${self.total_iva:>9.2f}")
        print(f"{'TOTAL:':<55} ${self.total:>9.2f}")

    @staticmethod
    def guardar_ventas(ventas, nombre_archivo):
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            for venta in ventas:
                items_str = ",".join(
                    f"{item['producto'].codigo}:{item['talla']}:{item['cantidad']}:{item['subtotal_base']}:{item['subtotal_iva']}:{item['subtotal']}"
                    for item in venta.items
                )
                archivo.write(f"{venta.numero_venta};{venta.cliente.identificacion};{items_str};{venta.subtotal_sin_iva};{venta.total_iva};{venta.total}\n")

    @staticmethod
    def cargar_ventas(nombre_archivo, clientes, productos):
        ventas = []
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if not (linea := linea.strip()):
                    continue

                datos = linea.split(";")
                numero_venta = int(datos[0])
                identificacion = int(datos[1])

                cliente = next((c for c in clientes if c.identificacion == identificacion), None)
                if not cliente:
                    continue

                venta = Venta(numero_venta, cliente)
                items_str = datos[2]
                venta.subtotal_sin_iva = float(datos[3])
                venta.total_iva = float(datos[4])
                venta.total = float(datos[5])

                if items_str:
                    for item_data in items_str.split(","):
                        partes = item_data.split(":")
                        codigo = int(partes[0])
                        talla = partes[1]
                        cantidad = int(partes[2])
                        producto = next((p for p in productos if p.codigo == codigo), None)

                        if producto:
                            item = {
                                'producto': producto,
                                'talla': talla,
                                'cantidad': cantidad,
                                'precio_base': float(partes[3]) / cantidad,
                                'iva_unitario': float(partes[4]) / cantidad,
                                'subtotal_base': float(partes[3]),
                                'subtotal_iva': float(partes[4]),
                                'subtotal': float(partes[5])
                            }
                            venta.items.append(item)

                ventas.append(venta)
        return ventas
