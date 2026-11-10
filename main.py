from Producto import Producto
from Inventario import Inventario
from Cliente import Cliente
from Venta import Venta

# ──────────────────────────────────────────────
#  Datos en memoria
# ──────────────────────────────────────────────
inventario = Inventario()
clientes = []
ventas = []
contador_ventas = 1  # para numerar ventas automáticamente

# ──────────────────────────────────────────────
#  Cargar datos persistidos (si existen)
# ──────────────────────────────────────────────
try:
    inventario.cargar_archivo("productos.txt")
except FileNotFoundError:
    pass

try:
    clientes = Cliente.cargar_clientes("clientes.txt")
except FileNotFoundError:
    pass

try:
    ventas = Venta.cargar_ventas("ventas.txt", clientes, inventario.productos)
    if ventas:
        contador_ventas = max(v.get_numero_venta() for v in ventas) + 1
except FileNotFoundError:
    pass


# ──────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────
def separador():
    print("=" * 45)

def pausa():
    input("\nPresiona Enter para continuar...")

def buscar_cliente_por_id(identificacion):
    for c in clientes:
        if c.get_identificacion() == identificacion:
            return c
    return None


# ──────────────────────────────────────────────
#  SUBMENÚ: INVENTARIO
# ──────────────────────────────────────────────
def menu_inventario():
    while True:
        separador()
        print("       GESTIÓN DE INVENTARIO")
        separador()
        print("  1. Ver inventario completo")
        print("  2. Agregar producto")
        print("  3. Buscar producto por código")
        print("  4. Ver productos ordenados por precio")
        print("  5. Ver productos ordenados por nombre")
        print("  0. Volver al menú principal")
        separador()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            separador()
            print("       INVENTARIO COMPLETO")
            separador()
            if not inventario.productos:
                print("  El inventario está vacío.")
            else:
                inventario.mostrar_inventario()
            pausa()

        elif opcion == "2":
            separador()
            print("       AGREGAR PRODUCTO")
            separador()
            try:
                codigo    = int(input("Código: "))
                nombre    = input("Nombre: ").strip()
                categoria = input("Categoría (Superior/Inferior/Accesorio...): ").strip()
                talla     = input("Talla: ").strip()
                precio    = int(input("Precio: "))
                cantidad  = int(input("Cantidad en stock: "))

                # Verificar que el código no esté repetido
                if inventario.buscar_producto_secuencial(codigo):
                    print("  ⚠ Ya existe un producto con ese código.")
                else:
                    nuevo = Producto(codigo, nombre, categoria, talla, precio, cantidad)
                    inventario.agregar_producto(nuevo)
                    inventario.guardar_archivo("productos.txt")
                    print("  ✓ Producto agregado y guardado.")
            except ValueError:
                print("  ✗ Datos inválidos. Intenta de nuevo.")
            pausa()

        elif opcion == "3":
            separador()
            print("       BUSCAR PRODUCTO")
            separador()
            try:
                codigo = int(input("Código del producto: "))
                encontrado = inventario.buscar_producto_secuencial(codigo)
                if encontrado:
                    print("\n  Producto encontrado:")
                    encontrado.mostrar_producto()
                else:
                    print("  ✗ Producto no encontrado.")
            except ValueError:
                print("  ✗ Código inválido.")
            pausa()

        elif opcion == "4":
            separador()
            print("  PRODUCTOS ORDENADOS POR PRECIO (menor → mayor)")
            separador()
            for p in inventario.ordenar_por_precio():
                print("  ----------------")
                p.mostrar_producto()
            pausa()

        elif opcion == "5":
            separador()
            print("  PRODUCTOS ORDENADOS POR NOMBRE (A → Z)")
            separador()
            for p in inventario.ordenar_por_nombre():
                print("  ----------------")
                p.mostrar_producto()
            pausa()

        elif opcion == "0":
            break
        else:
            print("  ✗ Opción no válida.")
            pausa()


# ──────────────────────────────────────────────
#  SUBMENÚ: PRODUCTOS (vista rápida)
# ──────────────────────────────────────────────
def menu_productos():
    while True:
        separador()
        print("       PRODUCTOS DE LA TIENDA")
        separador()
        print("  1. Listar todos los productos")
        print("  2. Buscar producto por código")
        print("  0. Volver al menú principal")
        separador()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            separador()
            if not inventario.productos:
                print("  No hay productos registrados.")
            else:
                for p in inventario.productos:
                    print("  ----------------")
                    p.mostrar_producto()
            pausa()

        elif opcion == "2":
            separador()
            try:
                codigo = int(input("Código del producto: "))
                encontrado = inventario.buscar_producto_secuencial(codigo)
                if encontrado:
                    print("\n  Detalles del producto:")
                    encontrado.mostrar_producto()
                else:
                    print("  ✗ Producto no encontrado.")
            except ValueError:
                print("  ✗ Código inválido.")
            pausa()

        elif opcion == "0":
            break
        else:
            print("  ✗ Opción no válida.")
            pausa()


# ──────────────────────────────────────────────
#  SUBMENÚ: VENTAS
# ──────────────────────────────────────────────
def menu_ventas():
    global contador_ventas

    while True:
        separador()
        print("       GESTIÓN DE VENTAS")
        separador()
        print("  1. Realizar una venta")
        print("  2. Ver todas las ventas")
        print("  0. Volver al menú principal")
        separador()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            separador()
            print("       NUEVA VENTA")
            separador()
            try:
                # Cliente
                id_cliente = int(input("Identificación del cliente: "))
                cliente = buscar_cliente_por_id(id_cliente)

                if not cliente:
                    nombre_cliente = input("Cliente nuevo. Ingresa el nombre: ").strip()
                    cliente = Cliente(id_cliente, nombre_cliente)
                    clientes.append(cliente)
                    Cliente.guardar_clientes(clientes, "clientes.txt")
                    print(f"  ✓ Cliente '{nombre_cliente}' registrado.")

                # Producto
                codigo_producto = int(input("Código del producto: "))
                producto = inventario.buscar_producto_secuencial(codigo_producto)

                if not producto:
                    print("  ✗ Producto no encontrado en el inventario.")
                    pausa()
                    continue

                print(f"  Producto: {producto.get_nombre()} | Stock: {producto.get_cantidad()} | Precio: ${producto.get_precio()}")
                cantidad = int(input("Cantidad a vender: "))

                if cantidad <= 0:
                    print("  ✗ La cantidad debe ser mayor a 0.")
                    pausa()
                    continue

                fecha = input("Fecha (DD/MM/AAAA): ").strip()

                venta = Venta(contador_ventas, fecha, cliente, producto, cantidad)
                if venta.registrar_venta():
                    ventas.append(venta)
                    contador_ventas += 1
                    Venta.guardar_ventas(ventas, "ventas.txt")
                    inventario.guardar_archivo("productos.txt")
                    print(f"\n  ✓ Venta #{venta.get_numero_venta()} registrada.")
                    print(f"  Total: ${venta.get_total()}")
                    print(f"  Stock restante de '{producto.get_nombre()}': {producto.get_cantidad()}")
                else:
                    print(f"  ✗ Stock insuficiente. Disponible: {producto.get_cantidad()}")

            except ValueError:
                print("  ✗ Datos inválidos. Intenta de nuevo.")
            pausa()

        elif opcion == "2":
            separador()
            print("       TODAS LAS VENTAS")
            separador()
            if not ventas:
                print("  No hay ventas registradas.")
            else:
                for v in ventas:
                    print("  ----------------")
                    print(f"  N° Venta : {v.get_numero_venta()}")
                    print(f"  Fecha    : {v.get_fecha()}")
                    print(f"  Cliente  : {v.get_cliente().get_nombre()}")
                    print(f"  Producto : {v.get_producto().get_nombre()}")
                    print(f"  Cantidad : {v.get_cantidad()}")
                    print(f"  Total    : ${v.get_total()}")
            pausa()

        elif opcion == "0":
            break
        else:
            print("  ✗ Opción no válida.")
            pausa()


# ──────────────────────────────────────────────
#  MENÚ PRINCIPAL
# ──────────────────────────────────────────────
def menu_principal():
    while True:
        separador()
        print("     🛍  TIENDA DE ROPA - MENÚ PRINCIPAL")
        separador()
        print("  1. Inventario")
        print("  2. Realizar una venta")
        print("  3. Ver productos")
        print("  4. Ver todas las ventas")
        print("  0. Salir")
        separador()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            menu_inventario()
        elif opcion == "2":
            menu_ventas()
        elif opcion == "3":
            menu_productos()
        elif opcion == "4":
            # Atajo directo a ver ventas
            separador()
            print("       TODAS LAS VENTAS")
            separador()
            if not ventas:
                print("  No hay ventas registradas.")
            else:
                for v in ventas:
                    print("  ----------------")
                    print(f"  N° Venta : {v.get_numero_venta()}")
                    print(f"  Fecha    : {v.get_fecha()}")
                    print(f"  Cliente  : {v.get_cliente().get_nombre()}")
                    print(f"  Producto : {v.get_producto().get_nombre()}")
                    print(f"  Cantidad : {v.get_cantidad()}")
                    print(f"  Total    : ${v.get_total()}")
            pausa()
        elif opcion == "0":
            print("\n  Hasta luego 👋")
            break
        else:
            print("  ✗ Opción no válida. Intenta de nuevo.")
            pausa()


# ──────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ──────────────────────────────────────────────
if __name__ == "__main__":
    menu_principal()
