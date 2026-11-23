from Producto import Producto
from Inventario import Inventario
from Cliente import Cliente
from Venta import Venta

# Inicialización
inventario = Inventario()
clientes = []
ventas = []
contador_ventas = 1

# Cargar datos
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
        contador_ventas = max(v.numero_venta for v in ventas) + 1
except FileNotFoundError:
    pass

# Helpers
def separador():
    print("=" * 45)

def pausa():
    input("\nPresiona Enter para continuar...")

def buscar_cliente_por_id(identificacion):
    return next((c for c in clientes if c.identificacion == identificacion), None)

# SUBMENÚ: INVENTARIO
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
        print("  6. Agregar stock a producto existente")
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
                codigo = int(input("Código: "))
                nombre = input("Nombre: ").strip()
                categoria = input("Categoría (Superior/Inferior/Accesorio...): ").strip()
                talla = input("Talla: ").strip()
                precio = int(input("Precio: "))
                cantidad = int(input("Cantidad en stock: "))

                if inventario.buscar_producto(codigo):
                    print("   Ya existe un producto con ese código.")
                else:
                    inventario.agregar_producto(Producto(codigo, nombre, categoria, talla, precio, cantidad))
                    inventario.guardar_archivo("productos.txt")
                    print("  Producto agregado y guardado.")
            except ValueError:
                print("   Datos inválidos. Intenta de nuevo.")
            pausa()

        elif opcion == "3":
            separador()
            print("       BUSCAR PRODUCTO")
            separador()
            try:
                codigo = int(input("Código del producto: "))
                encontrado = inventario.buscar_producto(codigo)
                if encontrado:
                    print("\n  Producto encontrado:")
                    encontrado.mostrar_producto()
                else:
                    print("  Producto no encontrado.")
            except ValueError:
                print("   Código inválido.")
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

        elif opcion == "6":
            separador()
            print("       AGREGAR STOCK A PRODUCTO EXISTENTE")
            separador()
            try:
                codigo = int(input("Código del producto: "))
                producto = inventario.buscar_producto(codigo)
                
                if not producto:
                    print("   Producto no encontrado.")
                else:
                    print("\n  Producto encontrado:")
                    print("  ----------------")
                    producto.mostrar_producto()
                    print("  ----------------")
                    
                    cantidad_agregar = int(input("\nCantidad a agregar al stock: "))
                    
                    if cantidad_agregar <= 0:
                        print("   La cantidad debe ser mayor a 0.")
                    elif cantidad_agregar > 999999:
                        print("   La cantidad excede el máximo permitido (999,999).")
                    else:
                        stock_anterior = producto.cantidad
                        if producto.agregar_stock(cantidad_agregar):
                            inventario.guardar_archivo("productos.txt")
                            print(f"\n  Stock actualizado exitosamente")
                            print(f"  Stock anterior: {stock_anterior}")
                            print(f"  Stock agregado: {cantidad_agregar}")
                            print(f"  Stock nuevo: {producto.cantidad}")
                        else:
                            print("   Error al agregar stock.")
            except ValueError:
                print("   Datos inválidos. Intenta de nuevo.")
            pausa()

        elif opcion == "0":
            break
        else:
            print("   Opción no válida.")
            pausa()

# SUBMENÚ: PRODUCTOS
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
                encontrado = inventario.buscar_producto(codigo)
                if encontrado:
                    print("\n  Detalles del producto:")
                    encontrado.mostrar_producto()
                else:
                    print("   Producto no encontrado.")
            except ValueError:
                print("   Código inválido.")
            pausa()

        elif opcion == "0":
            break
        else:
            print("   Opción no válida.")
            pausa()

# SUBMENÚ: VENTAS
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
                id_cliente = int(input("Identificación del cliente: "))
                cliente = buscar_cliente_por_id(id_cliente)

                if not cliente:
                    nombre_cliente = input("Cliente nuevo. Ingresa el nombre: ").strip()
                    cliente = Cliente(id_cliente, nombre_cliente)
                    clientes.append(cliente)
                    Cliente.guardar_clientes(clientes, "clientes.txt")
                    print(f"   Cliente '{nombre_cliente}' registrado.")

                venta = Venta(contador_ventas, cliente)

                while True:
                    separador()
                    codigo_producto = int(input("Código del producto: "))
                    producto = inventario.buscar_producto(codigo_producto)

                    if not producto:
                        print("   Producto no encontrado en el inventario.")
                        if input("¿Desea intentar con otro producto? (s/n): ").strip().lower() != 's':
                            break
                        continue

                    print(f"  Producto: {producto.nombre} | Stock: {producto.cantidad} | Precio: ${producto.precio}")
                    cantidad = int(input("Cantidad a vender: "))

                    if cantidad <= 0:
                        print("   La cantidad debe ser mayor a 0.")
                        if input("¿Desea intentar de nuevo? (s/n): ").strip().lower() != 's':
                            break
                        continue

                    if venta.agregar_item(producto, cantidad):
                        print(f"   {producto.nombre} agregado a la venta.")
                    else:
                        print(f"   Stock insuficiente. Disponible: {producto.cantidad}")

                    if input("\n¿Agregar otro producto a esta venta? (s/n): ").strip().lower() != 's':
                        break

                if venta.items:
                    if venta.registrar_venta():
                        ventas.append(venta)
                        contador_ventas += 1
                        Venta.guardar_ventas(ventas, "ventas.txt")
                        inventario.guardar_archivo("productos.txt")
                        separador()
                        print("\n  VENTA REGISTRADA EXITOSAMENTE")
                        separador()
                        venta.mostrar_venta()
                    else:
                        print("   Error al registrar la venta.")
                else:
                    print("   No se agregaron productos a la venta.")

            except ValueError:
                print("   Datos inválidos. Intenta de nuevo.")
            pausa()

        elif opcion == "2":
            separador()
            print("       TODAS LAS VENTAS")
            separador()
            if not ventas:
                print("  No hay ventas registradas.")
            else:
                for v in ventas:
                    print("  ================")
                    v.mostrar_venta()
            pausa()

        elif opcion == "0":
            break
        else:
            print("   Opción no válida.")
            pausa()

# MENÚ PRINCIPAL
def menu_principal():
    while True:
        separador()
        print("       TIENDA DE ROPA - MENÚ PRINCIPAL")
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
            separador()
            print("       TODAS LAS VENTAS")
            separador()
            if not ventas:
                print("  No hay ventas registradas.")
            else:
                for v in ventas:
                    print("  ================")
                    v.mostrar_venta()
            pausa()
        elif opcion == "0":
            print("\n  Hasta luego ")
            break
        else:
            print("  Opción no válida. Intenta de nuevo.")
            pausa()

if __name__ == "__main__":
    menu_principal()
