import logging
from dal import Database, ProductRepository, SupplierRepository, OperationRepository
from bll import ProductService, SupplierService, OperationService
from ui import WarehouseApp


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("debug.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )


def build_container():
    db = Database("warehouse.db")
    product_repo = ProductRepository(db)
    supplier_repo = SupplierRepository(db)
    op_repo = OperationRepository(db)
    return {
        "products": ProductService(product_repo),
        "suppliers": SupplierService(supplier_repo),
        "ops": OperationService(product_repo, supplier_repo, op_repo),
    }


def main():
    setup_logging()
    container = build_container()
    app = WarehouseApp(container)
    app.mainloop()


if __name__ == "__main__":
    main()