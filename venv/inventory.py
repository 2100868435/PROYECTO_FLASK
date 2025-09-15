# inventory.py
import os
import csv
import json
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "datos")
CSV_PATH = os.path.join(DATA_DIR, "datos.csv")
JSON_PATH = os.path.join(DATA_DIR, "datos.json")
TXT_PATH = os.path.join(DATA_DIR, "datos.txt")

@dataclass
class Product:
    id: int
    nombre: str
    descripcion: str = ""
    precio: float = 0.0
    cantidad: int = 0

class Inventory:
    def __init__(self, csv_path=CSV_PATH, json_path=JSON_PATH, txt_path=TXT_PATH):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.csv_path = csv_path
        self.json_path = json_path
        self.txt_path = txt_path
        self.products: List[Product] = []
        # Intentamos cargar los datos (prioridad: CSV -> JSON -> TXT)
        if os.path.exists(self.csv_path):
            self.load_from_csv()
        elif os.path.exists(self.json_path):
            self.load_from_json()
        elif os.path.exists(self.txt_path):
            self.load_from_txt()

    # --- CARGAR ---
    def load_from_csv(self):
        self.products = []
        with open(self.csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                try:
                    p = Product(
                        id=int(r.get("id", 0)),
                        nombre=r.get("nombre", ""),
                        descripcion=r.get("descripcion", ""),
                        precio=float(r.get("precio", 0) or 0),
                        cantidad=int(r.get("cantidad", 0) or 0),
                    )
                    self.products.append(p)
                except Exception:
                    continue

    def load_from_json(self):
        self.products = []
        with open(self.json_path, encoding='utf-8') as f:
            data = json.load(f)
            for r in data:
                p = Product(
                    id=int(r.get("id", 0)),
                    nombre=r.get("nombre", ""),
                    descripcion=r.get("descripcion", ""),
                    precio=float(r.get("precio", 0) or 0),
                    cantidad=int(r.get("cantidad", 0) or 0),
                )
                self.products.append(p)

    def load_from_txt(self, sep="|"):
        self.products = []
        with open(self.txt_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(sep)
                if len(parts) < 5:
                    continue
                try:
                    p = Product(
                        id=int(parts[0]),
                        nombre=parts[1],
                        descripcion=parts[2],
                        precio=float(parts[3]),
                        cantidad=int(parts[4]),
                    )
                    self.products.append(p)
                except Exception:
                    continue

    # --- GUARDAR ---
    def save_to_csv(self):
        with open(self.csv_path, "w", newline="", encoding='utf-8') as f:
            fieldnames = ["id", "nombre", "descripcion", "precio", "cantidad"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for p in self.products:
                writer.writerow(asdict(p))

    def save_to_json(self):
        with open(self.json_path, "w", encoding='utf-8') as f:
            json.dump([asdict(p) for p in self.products], f, indent=2, ensure_ascii=False)

    def save_to_txt(self, sep="|"):
        with open(self.txt_path, "w", encoding='utf-8') as f:
            for p in self.products:
                line = sep.join([str(p.id), p.nombre, p.descripcion, str(p.precio), str(p.cantidad)])
                f.write(line + "\n")

    def save_all(self):
        self.save_to_csv()
        self.save_to_json()
        self.save_to_txt()

    # --- UTILIDADES CRUD ---
    def _next_id(self) -> int:
        if not self.products:
            return 1
        return max(p.id for p in self.products) + 1

    def list_products(self) -> List[Product]:
        return list(self.products)

    def find_by_id(self, pid: int) -> Optional[Product]:
        for p in self.products:
            if p.id == pid:
                return p
        return None

    def add_product(self, nombre: str, descripcion: str = "", precio: float = 0.0, cantidad: int = 0, persist=True) -> Product:
        new_id = self._next_id()
        p = Product(id=new_id, nombre=nombre, descripcion=descripcion, precio=float(precio), cantidad=int(cantidad))
        self.products.append(p)
        if persist:
            self.save_all()
        return p

    def update_product(self, pid: int, **kwargs) -> bool:
        p = self.find_by_id(pid)
        if not p:
            return False
        if "nombre" in kwargs:
            p.nombre = kwargs["nombre"]
        if "descripcion" in kwargs:
            p.descripcion = kwargs["descripcion"]
        if "precio" in kwargs:
            p.precio = float(kwargs["precio"])
        if "cantidad" in kwargs:
            p.cantidad = int(kwargs["cantidad"])
        self.save_all()
        return True

    def delete_product(self, pid: int) -> bool:
        p = self.find_by_id(pid)
        if not p:
            return False
        self.products.remove(p)
        self.save_all()
        return True

    # Impresión simple
    def print_table(self):
        rows = self.list_products()
        if not rows:
            print("No hay productos.")
            return
        header = f"{'ID':>3}  {'NOMBRE':20}  {'PRECIO':>8}  {'CANT':>5}"
        print(header)
        print("-" * len(header))
        for p in rows:
            print(f"{p.id:>3}  {p.nombre:20.20}  {p.precio:8.2f}  {p.cantidad:5}")

# --- Interfaz simple para probar en consola ---
def main_menu():
    inv = Inventory()
    while True:
        print("\n--- INVENTARIO ---")
        print("1) Listar productos")
        print("2) Agregar producto")
        print("3) Editar producto")
        print("4) Eliminar producto")
        print("5) Guardar archivos (CSV/JSON/TXT)")
        print("0) Salir")
        choice = input("Elige una opción: ").strip()
        if choice == "1":
            inv.print_table()
        elif choice == "2":
            nombre = input("Nombre: ").strip()
            descripcion = input("Descripción: ").strip()
            precio = input("Precio: ").strip() or "0"
            cantidad = input("Cantidad: ").strip() or "0"
            try:
                p = inv.add_product(nombre, descripcion, float(precio), int(cantidad))
                print(f"Agregado id={p.id}")
            except Exception as e:
                print("Error al agregar:", e)
        elif choice == "3":
            pid = int(input("ID del producto a editar: ").strip())
            p = inv.find_by_id(pid)
            if not p:
                print("No encontrado.")
                continue
            print("Dejar vacío para mantener el valor actual.")
            nombre = input(f"Nombre [{p.nombre}]: ").strip() or p.nombre
            descripcion = input(f"Descripción [{p.descripcion}]: ").strip() or p.descripcion
            precio = input(f"Precio [{p.precio}]: ").strip() or p.precio
            cantidad = input(f"Cantidad [{p.cantidad}]: ").strip() or p.cantidad
            try:
                inv.update_product(pid, nombre=nombre, descripcion=descripcion, precio=float(precio), cantidad=int(cantidad))
                print("Actualizado.")
            except Exception as e:
                print("Error al actualizar:", e)
        elif choice == "4":
            pid = int(input("ID del producto a eliminar: ").strip())
            if inv.delete_product(pid):
                print("Eliminado.")
            else:
                print("No encontrado.")
        elif choice == "5":
            inv.save_all()
            print("Guardado en CSV/JSON/TXT.")
        elif choice == "0":
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main_menu()
