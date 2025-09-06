from typing import List, Dict
from models import Producto, Categoria
from repository import ProductoRepository, CategoriaRepository

# Clase Inventario
class Inventario:
    def _init_(self):
        self.producto_repo = ProductoRepository()
        self.categoria_repo = CategoriaRepository()

    def agregar_producto(self, nombre: str, categoria_nombre: str, cantidad: int, precio: float) -> Producto:
        categoria = self.categoria_repo.obtener_por_nombre(categoria_nombre)
        if not categoria:
            categoria = Categoria(nombre=categoria_nombre)
            self.categoria_repo.agregar(categoria)

        producto = Producto(nombre=nombre, categoria=categoria, cantidad=cantidad, precio=precio)
        self.producto_repo.agregar(producto)
        return producto
    
    def eliminar_producto(self, producto_id: int) -> bool:
        return self.producto_repo.eliminar(producto_id)
    
    def actualizar_producto(self, producto_id: int, **kwargs) -> bool:
        return self.producto_repo.actualizar(producto_id, **kwargs)
    
    def listar_productos(self) -> List[Producto]:
        return self.producto_repo.listar_todos()
    
    def buscar_productos_por_categoria(self, categoria_nombre: str) -> List[Producto]:
        categoria = self.categoria_repo.obtener_por_nombre(categoria_nombre)
        if not categoria:
            return []
        return self.producto_repo.buscar_por_categoria(categoria.id)
    
    def obtener_inventario_total(self) -> Dict[str, float]:
        productos = self.producto_repo.listar_todos()
        total_valor = sum(p.cantidad * p.precio for p in productos)
        total_unidades = sum(p.cantidad for p in productos)
        return {
            "total_productos": total_unidades,
            "valor_total": total_valor
        }