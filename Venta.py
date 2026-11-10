class Venta:

    def __init__(self, numero_venta, fecha, cliente, producto, cantidad):

        self.numero_venta = numero_venta
        self.fecha = fecha
        self.cliente = cliente
        self.producto = producto
        self.cantidad = cantidad
        self.total = 0

# GETTERS

    def get_numero_venta(self):
        return self.numero_venta

    def get_fecha(self):
        return self.fecha

    def get_cliente(self):
        return self.cliente

    def get_producto(self):
        return self.producto

    def get_cantidad(self):
        return self.cantidad

    def get_total(self):
        return self.total
        
# -------------------------------------
    def calcular_total(self):

        self.total = self.producto.precio * self.cantidad

        return self.total

    def registrar_venta(self):

        if self.producto.actualizar_stock(self.cantidad):

            self.calcular_total()
            return True

        else:
            return False

#guatrdar venta 
    @staticmethod
    def guardar_ventas(ventas, nombre_archivo):

        with open(nombre_archivo, "w", encoding="utf-8") as archivo:

            for venta in ventas:

                linea = (
                    f"{venta.get_numero_venta()};"
                    f"{venta.get_fecha()};"
                    f"{venta.get_cliente().get_identificacion()};"
                    f"{venta.get_producto().get_codigo()};"
                    f"{venta.get_cantidad()};"
                    f"{venta.get_total()}\n"
                )

                archivo.write(linea)  
#cargar ventas
    @staticmethod
    def cargar_ventas(nombre_archivo, clientes, productos):

        ventas = []

        with open(nombre_archivo, "r", encoding="utf-8") as archivo:

            for linea in archivo:

                linea = linea.rstrip("\n")

                if linea.strip() != "":

                    datos = linea.split(";")

                    numero_venta = int(datos[0])
                    fecha = datos[1]
                    identificacion = int(datos[2])
                    codigo = int(datos[3])
                    cantidad = int(datos[4])
                    total = int(datos[5])

                    cliente = None
                    producto = None

                    for c in clientes:
                        if c.get_identificacion() == identificacion:
                            cliente = c

                    for p in productos:
                        if p.get_codigo() == codigo:
                            producto = p

                    if cliente is not None and producto is not None:

                        venta = Venta(
                            numero_venta, fecha, cliente, producto, cantidad
                        )

                        venta.total = total

                        ventas.append(venta)

        return ventas      