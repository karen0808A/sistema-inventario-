import json
from producto import Producto


class Inventario:
    def __init__(self, archivo="inventario.json"):
        self.productos = {}  # diccionario {id: Producto}
        self.archivo = archivo
        self.cargar_desde_archivo()

    def agregar_producto(self, producto):
        if producto.get_id() in self.productos:
            print("❌ El producto ya existe.")
        else:
            self.productos[producto.get_id()] = producto
            print("✅ Producto agregado.")

    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]
            print("🗑️ Producto eliminado.")
        else:
            print("❌ Producto no encontrado.")

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        producto = self.productos.get(id_producto)
        if producto:
            if cantidad is not None:
                producto.set_cantidad(cantidad)
            if precio is not None:
                producto.set_precio(precio)
            print("🔄 Producto actualizado.")
        else:
            print("❌ Producto no encontrado.")

    def buscar_por_nombre(self, nombre):
        encontrados = [
            p for p in self.productos.values()
            if nombre.lower() in p.get_nombre().lower()
        ]

        if encontrados:
            for p in encontrados:
                self.mostrar_producto(p)
        else:
            print("❌ No se encontraron productos.")

    def mostrar_producto(self, producto):
        print(
            f"ID: {producto.get_id()} | "
            f"Nombre: {producto.get_nombre()} | "
            f"Cantidad: {producto.get_cantidad()} | "
            f"Precio: ${producto.get_precio():.2f}"
        )

    def mostrar_todos(self):
        if not self.productos:
            print("📭 Inventario vacío.")
        else:
            for producto in self.productos.values():
                self.mostrar_producto(producto)

    def guardar_en_archivo(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(
                {id_p: p.to_dict() for id_p, p in self.productos.items()},
                f,
                indent=4
            )

    def cargar_desde_archivo(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.productos = {
                    id_p: Producto.from_dict(p_data)
                    for id_p, p_data in data.items()
                }
        except FileNotFoundError:
            self.productos = {}