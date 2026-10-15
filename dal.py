import sqlite3
from contextlib import contextmanager
from models import Product, Supplier, Operation


class Database:
    """Единая точка работы с SQLite."""

    def __init__(self, path: str = "warehouse.db"):
        self.path = path
        self._init_schema()

    @contextmanager
    def conn(self):
        c = sqlite3.connect(self.path)
        c.row_factory = sqlite3.Row
        try:
            yield c
            c.commit()
        finally:
            c.close()

    def _init_schema(self):
        with self.conn() as c:
            c.executescript("""
                CREATE TABLE IF NOT EXISTS products(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    sku TEXT UNIQUE NOT NULL,
                    quantity INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS suppliers(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    contact_person TEXT NOT NULL,
                    phone TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS operations(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    supplier_id INTEGER NOT NULL,
                    kind TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    FOREIGN KEY(product_id) REFERENCES products(id),
                    FOREIGN KEY(supplier_id) REFERENCES suppliers(id)
                );
            """)


class ProductRepository:
    def __init__(self, db: Database):
        self.db = db

    def get_all(self) -> list[Product]:
        with self.db.conn() as c:
            rows = c.execute("SELECT * FROM products").fetchall()
        return [Product(r["id"], r["name"], r["category"], r["sku"], r["quantity"]) for r in rows]

    def get_by_id(self, pid: int) -> Product | None:
        with self.db.conn() as c:
            r = c.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
        return Product(r["id"], r["name"], r["category"], r["sku"], r["quantity"]) if r else None

    def search(self, query: str) -> list[Product]:
        with self.db.conn() as c:
            rows = c.execute(
                "SELECT * FROM products WHERE name LIKE ? OR sku LIKE ? OR category LIKE ?",
                (f"%{query}%", f"%{query}%", f"%{query}%")
            ).fetchall()
        return [Product(r["id"], r["name"], r["category"], r["sku"], r["quantity"]) for r in rows]

    def add(self, product: Product) -> int:
        with self.db.conn() as c:
            cur = c.execute(
                "INSERT INTO products(name, category, sku, quantity) VALUES(?,?,?,?)",
                (product.name, product.category, product.sku, product.quantity)
            )
            return cur.lastrowid

    def set_quantity(self, product_id: int, quantity: int):
        with self.db.conn() as c:
            c.execute("UPDATE products SET quantity=? WHERE id=?", (quantity, product_id))


class SupplierRepository:
    def __init__(self, db: Database):
        self.db = db

    def get_all(self) -> list[Supplier]:
        with self.db.conn() as c:
            rows = c.execute("SELECT * FROM suppliers").fetchall()
        return [Supplier(r["id"], r["name"], r["contact_person"], r["phone"]) for r in rows]

    def get_by_id(self, sid: int) -> Supplier | None:
        with self.db.conn() as c:
            r = c.execute("SELECT * FROM suppliers WHERE id=?", (sid,)).fetchone()
        return Supplier(r["id"], r["name"], r["contact_person"], r["phone"]) if r else None

    def add(self, supplier: Supplier) -> int:
        with self.db.conn() as c:
            cur = c.execute(
                "INSERT INTO suppliers(name, contact_person, phone) VALUES(?,?,?)",
                (supplier.name, supplier.contact_person, supplier.phone)
            )
            return cur.lastrowid


class OperationRepository:
    def __init__(self, db: Database):
        self.db = db

    def add(self, op: Operation) -> int:
        with self.db.conn() as c:
            cur = c.execute(
                "INSERT INTO operations(product_id, supplier_id, kind, amount) VALUES(?,?,?,?)",
                (op.product_id, op.supplier_id, op.kind, op.amount)
            )
            return cur.lastrowid