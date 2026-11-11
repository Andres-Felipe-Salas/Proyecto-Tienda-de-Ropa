class Venta:
    IVA_PORCENTAJE = 0.19

    def __init__(self, numero_venta, fecha, cliente):
        self.numero_venta = numero_venta
        self.fecha = fecha
        self.cliente = cliente
        self.items = []
        self.subtotal_sin_iva = 0
        self.total_iva = 0
        self.total = 0

    def get_numero_venta(self):
        return self.numero_venta

    def get_fecha(self):
        return self.fecha

    def get_cliente(self):
        return self.cliente

    def get_items(self):
        return self.items

    def get_subtotal_sin_iva(self):
        return self.subtotal_sin_iva

    def get_total_iva(self):
        return self.total_iva

    def get_total(self):
        return self.total

    def agregar_item(self, producto, cantidad):
        if not producto.hay_disponibilidad(cantidad):
            return False
        
        precio_base = producto.precio / (1 + self.IVA_PORCENTAJE)
        iva_unitario = producto.precio - precio_base
        
        item = {
            'producto': producto,
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
            if not item['producto'].actualizar_stock(item['cantidad']):
                return False
        
        self.calcular_total()
        return True

    def mostrar_venta(self):
        print(f"N° Venta : {self.numero_venta}")
        print(f"Fecha    : {self.fecha}")
        print(f"Cliente  : {self.cliente.get_nombre()} (ID: {self.cliente.get_identificacion()})")
        print("\nItems:")
        print(f"{'Producto':<20} {'Cant':>4} {'P.Base':>10} {'IVA':>10} {'Subtotal':>10}")
        print("-" * 60)
        for item in self.items:
            prod = item['producto']
            print(f"{prod.get_nombre():<20} {item['cantidad']:>4} ${item['subtotal_base']:>9.2f} ${item['subtotal_iva']:>9.2f} ${item['subtotal']:>9.2f}")
        print("-" * 60)
        print(f"{'SUBTOTAL (sin IVA):':<45} ${self.subtotal_sin_iva:>9.2f}")
        print(f"{'IVA (19%):':<45} ${self.total_iva:>9.2f}")
        print(f"{'TOTAL:':<45} ${self.total:>9.2f}")

    @staticmethod
    def guardar_ventas(ventas, nombre_archivo):
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            for venta in ventas:
                items_str = ",".join(
                    f"{item['producto'].get_codigo()}:{item['cantidad']}:{item['subtotal_base']}:{item['subtotal_iva']}:{item['subtotal']}"
                    for item in venta.items
                )
                archivo.write(f"{venta.numero_venta};{venta.fecha};{venta.cliente.get_identificacion()};{items_str};{venta.subtotal_sin_iva};{venta.total_iva};{venta.total}\n")

    @staticmethod
    def cargar_ventas(nombre_archivo, clientes, productos):
        ventas = []
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                
                datos = linea.split(";")
                numero_venta = int(datos[0])
                fecha = datos[1]
                identificacion = int(datos[2])
                
                cliente = next((c for c in clientes if c.get_identificacion() == identificacion), None)
                if not cliente:
                    continue
                
                venta = Venta(numero_venta, fecha, cliente)
                
                # Formato antiguo (6 campos)
                if len(datos) == 6:
                    codigo = int(datos[3])
                    cantidad = int(datos[4])
                    producto = next((p for p in productos if p.get_codigo() == codigo), None)
                    
                    if producto:
                        precio_base = producto.precio / (1 + Venta.IVA_PORCENTAJE)
                        iva_unitario = producto.precio - precio_base
                        item = {
                            'producto': producto,
                            'cantidad': cantidad,
                            'precio_base': round(precio_base, 2),
                            'iva_unitario': round(iva_unitario, 2),
                            'subtotal_base': round(precio_base * cantidad, 2),
                            'subtotal_iva': round(iva_unitario * cantidad, 2),
                            'subtotal': round(producto.precio * cantidad, 2)
                        }
                        venta.items.append(item)
                        venta.subtotal_sin_iva = item['subtotal_base']
                        venta.total_iva = item['subtotal_iva']
                        venta.total = item['subtotal']
                
                # Formato nuevo (7 campos)
                elif len(datos) == 7:
                    items_str = datos[3]
                    venta.subtotal_sin_iva = float(datos[4])
                    venta.total_iva = float(datos[5])
                    venta.total = float(datos[6])
                    
                    if items_str:
                        for item_data in items_str.split(","):
                            partes = item_data.split(":")
                            codigo = int(partes[0])
                            cantidad = int(partes[1])
                            producto = next((p for p in productos if p.get_codigo() == codigo), None)
                            
                            if producto:
                                item = {
                                    'producto': producto,
                                    'cantidad': cantidad,
                                    'precio_base': float(partes[2]) / cantidad,
                                    'iva_unitario': float(partes[3]) / cantidad,
                                    'subtotal_base': float(partes[2]),
                                    'subtotal_iva': float(partes[3]),
                                    'subtotal': float(partes[4])
                                }
                                venta.items.append(item)
                
                ventas.append(venta)
        
        return ventas
