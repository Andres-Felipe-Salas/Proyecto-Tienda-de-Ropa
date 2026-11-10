class Cliente:

    def __init__(self, identificacion, nombre):

        self.identificacion = identificacion
        self.nombre = nombre

    # GETTERS

    def get_identificacion(self):
        return self.identificacion

    def get_nombre(self):
        return self.nombre

    def actualizar_datos(self, nueva_identificacion, nuevo_nombre):

        self.identificacion = nueva_identificacion
        self.nombre = nuevo_nombre

    def mostrar_cliente(self):

        print("Identificacion:", self.identificacion)
        print("Nombre:", self.nombre)


        # GUARDAR CLIENTES

    @staticmethod
    def guardar_clientes(clientes, nombre_archivo):

        with open(nombre_archivo, "w", encoding="utf-8") as archivo:

            for cliente in clientes:

                linea = (
                    f"{cliente.get_identificacion()};"
                    f"{cliente.get_nombre()}\n"
                )

                archivo.write(linea)

#cargar clientes

    @staticmethod
    def cargar_clientes(nombre_archivo):

        clientes = []

        with open(nombre_archivo, "r", encoding="utf-8") as archivo:

            for linea in archivo:

                linea = linea.rstrip("\n")

                if linea.strip() != "":

                    datos = linea.split(";")

                    identificacion = int(datos[0])
                    nombre = datos[1]

                    cliente = Cliente(identificacion, nombre)

                    clientes.append(cliente)

        return clientes