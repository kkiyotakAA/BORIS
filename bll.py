import logging
from models import Product, Supplier, Operation
from exceptions import (
    ProductNotFoundException, SupplierNotFoundException,
    DuplicateSKUException, NotEnoughStockException
)

logger = logging.getLogger("warehouse.bll")


class ProductService:
    def __init__(self, product_repo):
        self.repo = product_repo

    def add_product(self, name: str, category: str, sku: str, quantity: int = 0) -> int:
        if not name or not category or not sku:
            raise ValueError("Все поля товара обязательны")
        if quantity < 0:
            raise ValueError("Количество не может быть отрицательным")
        for p in self.repo.get_all():
            if p.sku == sku:
                raise DuplicateSKUException(f"Артикул {sku} уже существует")
        new_id = self.repo.add(Product(None, name, category, sku, quantity))
        logger.info("Добавлен товар id=%s '%s' (SKU=%s)", new_id, name, sku)
        return new_id

    def list_products(self) -> list[Product]:
        return self.repo.get_all()

    def search(self, q: str) -> list[Product]:
        return self.repo.get_all() if not q else self.repo.search(q)


class SupplierService:
    def __init__(self, supplier_repo):
        self.repo = supplier_repo

    def add_supplier(self, name: str, contact: str, phone: str) -> int:
        if not name or not contact or not phone:
            raise ValueError("Все поля поставщика обязательны")
        new_id = self.repo.add(Supplier(None, name, contact, phone))
        logger.info("Добавлен поставщик id=%s '%s'", new_id, name)
        return new_id

    def list_suppliers(self) -> list[Supplier]:
        return self.repo.get_all()


class OperationService:
    """Приёмка и отгрузка товара."""

    def __init__(self, product_repo, supplier_repo, op_repo):
        self.products = product_repo
        self.suppliers = supplier_repo
        self.ops = op_repo

    def receive(self, product_id: int, supplier_id: int, amount: int) -> int:
        """Приёмка товара: увеличивает остаток."""
        if amount <= 0:
            raise ValueError("Количество должно быть положительным")
        product = self.products.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(f"Товар id={product_id} не найден")
        if not self.suppliers.get_by_id(supplier_id):
            raise SupplierNotFoundException(f"Поставщик id={supplier_id} не найден")

        op_id = self.ops.add(Operation(None, product_id, supplier_id, "in", amount))
        self.products.set_quantity(product_id, product.quantity + amount)
        logger.info("Приёмка: товар=%s +%s (поставщик=%s)", product_id, amount, supplier_id)
        return op_id

    def ship(self, product_id: int, supplier_id: int, amount: int) -> int:
        """Отгрузка товара: уменьшает остаток, проверяет наличие."""
        if amount <= 0:
            raise ValueError("Количество должно быть положительным")
        product = self.products.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(f"Товар id={product_id} не найден")
        if product.quantity < amount:
            raise NotEnoughStockException(
                f"На складе только {product.quantity} ед., нельзя отгрузить {amount}"
            )
        if not self.suppliers.get_by_id(supplier_id):
            raise SupplierNotFoundException(f"Поставщик id={supplier_id} не найден")

        op_id = self.ops.add(Operation(None, product_id, supplier_id, "out", amount))
        self.products.set_quantity(product_id, product.quantity - amount)
        logger.info("Отгрузка: товар=%s -%s (поставщик=%s)", product_id, amount, supplier_id)
        return op_id