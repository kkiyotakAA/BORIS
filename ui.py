import tkinter as tk
from tkinter import ttk, messagebox
from exceptions import WarehouseException


class WarehouseApp(tk.Tk):
    """Главное окно складской системы."""

    def __init__(self, container: dict):
        super().__init__()
        self.container = container
        self.title("Склад — информационная система")
        self.geometry("960x620")
        self.minsize(820, 520)

        style = ttk.Style(self)
        style.configure("Treeview", rowheight=24, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("TButton", padding=6)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.tab_products = ttk.Frame(notebook)
        self.tab_suppliers = ttk.Frame(notebook)
        self.tab_ops = ttk.Frame(notebook)

        notebook.add(self.tab_products, text="Товары")
        notebook.add(self.tab_suppliers, text="Поставщики")
        notebook.add(self.tab_ops, text="Приёмка / отгрузка")

        self._build_products_tab()
        self._build_suppliers_tab()
        self._build_ops_tab()

        self.refresh_products()
        self.refresh_suppliers()
        self.refresh_hint()

    # ================== ВКЛАДКА "ТОВАРЫ" ==================
    def _build_products_tab(self):
        form = ttk.LabelFrame(self.tab_products, text="Добавить товар")
        form.pack(fill="x", padx=8, pady=8)

        ttk.Label(form, text="Название:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.e_name = ttk.Entry(form, width=25)
        self.e_name.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(form, text="Категория:").grid(row=0, column=2, sticky="w", padx=6, pady=4)
        self.e_category = ttk.Entry(form, width=18)
        self.e_category.grid(row=0, column=3, padx=6, pady=4)

        ttk.Label(form, text="Артикул (SKU):").grid(row=0, column=4, sticky="w", padx=6, pady=4)
        self.e_sku = ttk.Entry(form, width=14)
        self.e_sku.grid(row=0, column=5, padx=6, pady=4)

        ttk.Label(form, text="Кол-во:").grid(row=0, column=6, sticky="w", padx=6, pady=4)
        self.e_qty = ttk.Entry(form, width=8)
        self.e_qty.insert(0, "0")
        self.e_qty.grid(row=0, column=7, padx=6, pady=4)

        ttk.Button(form, text="Добавить", command=self.on_add_product).grid(
            row=0, column=8, padx=8, pady=4
        )

        search_frame = ttk.LabelFrame(self.tab_products, text="Поиск")
        search_frame.pack(fill="x", padx=8, pady=(0, 8))

        ttk.Label(search_frame, text="Запрос:").pack(side="left", padx=6, pady=6)
        self.e_search = ttk.Entry(search_frame, width=40)
        self.e_search.pack(side="left", padx=6, pady=6)
        self.e_search.bind("<Return>", lambda e: self.on_search())

        ttk.Button(search_frame, text="Найти", command=self.on_search).pack(side="left", padx=4)
        ttk.Button(search_frame, text="Сбросить", command=self.refresh_products).pack(side="left", padx=4)

        cols = ("id", "name", "category", "sku", "qty")
        self.tree_products = ttk.Treeview(self.tab_products, columns=cols, show="headings")
        for c, h, w in [
            ("id", "ID", 50),
            ("name", "Название", 240),
            ("category", "Категория", 160),
            ("sku", "Артикул", 140),
            ("qty", "На складе", 100),
        ]:
            self.tree_products.heading(c, text=h)
            self.tree_products.column(c, width=w, anchor="w")

        vsb = ttk.Scrollbar(self.tab_products, orient="vertical", command=self.tree_products.yview)
        self.tree_products.configure(yscrollcommand=vsb.set)
        self.tree_products.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        vsb.pack(side="left", fill="y", pady=8)

    # ================== ВКЛАДКА "ПОСТАВЩИКИ" ==================
    def _build_suppliers_tab(self):
        form = ttk.LabelFrame(self.tab_suppliers, text="Добавить поставщика")
        form.pack(fill="x", padx=8, pady=8)

        ttk.Label(form, text="Название:").grid(row=0, column=0, sticky="w", padx=6, pady=4)
        self.e_sup_name = ttk.Entry(form, width=28)
        self.e_sup_name.grid(row=0, column=1, padx=6, pady=4)

        ttk.Label(form, text="Контактное лицо:").grid(row=0, column=2, sticky="w", padx=6, pady=4)
        self.e_sup_contact = ttk.Entry(form, width=24)
        self.e_sup_contact.grid(row=0, column=3, padx=6, pady=4)

        ttk.Label(form, text="Телефон:").grid(row=0, column=4, sticky="w", padx=6, pady=4)
        self.e_sup_phone = ttk.Entry(form, width=16)
        self.e_sup_phone.grid(row=0, column=5, padx=6, pady=4)

        ttk.Button(form, text="Добавить", command=self.on_add_supplier).grid(
            row=0, column=6, padx=8, pady=4
        )

        cols = ("id", "name", "contact", "phone")
        self.tree_suppliers = ttk.Treeview(self.tab_suppliers, columns=cols, show="headings")
        for c, h, w in [
            ("id", "ID", 60),
            ("name", "Название", 280),
            ("contact", "Контактное лицо", 240),
            ("phone", "Телефон", 180),
        ]:
            self.tree_suppliers.heading(c, text=h)
            self.tree_suppliers.column(c, width=w, anchor="w")

        vsb = ttk.Scrollbar(self.tab_suppliers, orient="vertical", command=self.tree_suppliers.yview)
        self.tree_suppliers.configure(yscrollcommand=vsb.set)
        self.tree_suppliers.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        vsb.pack(side="left", fill="y", pady=8)

    # ================== ВКЛАДКА "ПРИЁМКА / ОТГРУЗКА" ==================
    def _build_ops_tab(self):
        # Приёмка
        f1 = ttk.LabelFrame(self.tab_ops, text="Приёмка товара (увеличивает остаток)")
        f1.pack(fill="x", padx=8, pady=8)

        ttk.Label(f1, text="ID товара:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.e_in_product = ttk.Entry(f1, width=10)
        self.e_in_product.grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(f1, text="ID поставщика:").grid(row=0, column=2, sticky="w", padx=6, pady=6)
        self.e_in_supplier = ttk.Entry(f1, width=10)
        self.e_in_supplier.grid(row=0, column=3, padx=6, pady=6)

        ttk.Label(f1, text="Кол-во:").grid(row=0, column=4, sticky="w", padx=6, pady=6)
        self.e_in_amount = ttk.Entry(f1, width=10)
        self.e_in_amount.grid(row=0, column=5, padx=6, pady=6)

        ttk.Button(f1, text="Принять", command=self.on_receive).grid(
            row=0, column=6, padx=8, pady=6
        )

        # Отгрузка
        f2 = ttk.LabelFrame(self.tab_ops, text="Отгрузка товара (уменьшает остаток)")
        f2.pack(fill="x", padx=8, pady=8)

        ttk.Label(f2, text="ID товара:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.e_out_product = ttk.Entry(f2, width=10)
        self.e_out_product.grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(f2, text="ID поставщика:").grid(row=0, column=2, sticky="w", padx=6, pady=6)
        self.e_out_supplier = ttk.Entry(f2, width=10)
        self.e_out_supplier.grid(row=0, column=3, padx=6, pady=6)

        ttk.Label(f2, text="Кол-во:").grid(row=0, column=4, sticky="w", padx=6, pady=6)
        self.e_out_amount = ttk.Entry(f2, width=10)
        self.e_out_amount.grid(row=0, column=5, padx=6, pady=6)

        ttk.Button(f2, text="Отгрузить", command=self.on_ship).grid(
            row=0, column=6, padx=8, pady=6
        )

        # Подсказка
        info = ttk.LabelFrame(self.tab_ops, text="Подсказка: список товаров и поставщиков")
        info.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.txt_hint = tk.Text(info, height=12, wrap="none", font=("Consolas", 10))
        self.txt_hint.pack(side="left", fill="both", expand=True, padx=(6, 0), pady=6)
        vsb = ttk.Scrollbar(info, orient="vertical", command=self.txt_hint.yview)
        self.txt_hint.configure(yscrollcommand=vsb.set)
        vsb.pack(side="left", fill="y", pady=6)

    # ================== ОБРАБОТЧИКИ ==================
    def on_add_product(self):
        name = self.e_name.get().strip()
        category = self.e_category.get().strip()
        sku = self.e_sku.get().strip()
        try:
            qty = int(self.e_qty.get().strip() or "0")
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть числом")
            return
        try:
            self.container["products"].add_product(name, category, sku, qty)
            for e in (self.e_name, self.e_category, self.e_sku):
                e.delete(0, "end")
            self.e_qty.delete(0, "end")
            self.e_qty.insert(0, "0")
            self.refresh_products()
            self.refresh_hint()
        except (WarehouseException, ValueError) as ex:
            messagebox.showerror("Ошибка", str(ex))

    def on_add_supplier(self):
        name = self.e_sup_name.get().strip()
        contact = self.e_sup_contact.get().strip()
        phone = self.e_sup_phone.get().strip()
        try:
            self.container["suppliers"].add_supplier(name, contact, phone)
            for e in (self.e_sup_name, self.e_sup_contact, self.e_sup_phone):
                e.delete(0, "end")
            self.refresh_suppliers()
            self.refresh_hint()
        except (WarehouseException, ValueError) as ex:
            messagebox.showerror("Ошибка", str(ex))

    def on_search(self):
        q = self.e_search.get().strip()
        products = self.container["products"].search(q)
        self._fill_products(products)

    def on_receive(self):
        try:
            pid = int(self.e_in_product.get().strip())
            sid = int(self.e_in_supplier.get().strip())
            amount = int(self.e_in_amount.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка", "ID и количество должны быть числами")
            return
        try:
            self.container["ops"].receive(pid, sid, amount)
            self.refresh_products()
            self.refresh_hint()
            messagebox.showinfo("Готово", f"Принято {amount} ед. товара {pid}")
        except WarehouseException as ex:
            messagebox.showerror("Ошибка", str(ex))

    def on_ship(self):
        try:
            pid = int(self.e_out_product.get().strip())
            sid = int(self.e_out_supplier.get().strip())
            amount = int(self.e_out_amount.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка", "ID и количество должны быть числами")
            return
        try:
            self.container["ops"].ship(pid, sid, amount)
            self.refresh_products()
            self.refresh_hint()
            messagebox.showinfo("Готово", f"Отгружено {amount} ед. товара {pid}")
        except WarehouseException as ex:
            messagebox.showerror("Ошибка", str(ex))

    # ================== ОБНОВЛЕНИЕ ==================
    def refresh_products(self):
        products = self.container["products"].list_products()
        self._fill_products(products)

    def _fill_products(self, products):
        self.tree_products.delete(*self.tree_products.get_children())
        for p in products:
            self.tree_products.insert(
                "", "end", values=(p.id, p.name, p.category, p.sku, p.quantity)
            )

    def refresh_suppliers(self):
        self.tree_suppliers.delete(*self.tree_suppliers.get_children())
        for s in self.container["suppliers"].list_suppliers():
            self.tree_suppliers.insert(
                "", "end", values=(s.id, s.name, s.contact_person, s.phone)
            )

    def refresh_hint(self):
        self.txt_hint.delete("1.0", "end")
        self.txt_hint.insert("end", "=== ТОВАРЫ ===\n")
        for p in self.container["products"].list_products():
            self.txt_hint.insert(
                "end",
                f"  [{p.id}] {p.name} ({p.category}, SKU={p.sku}) — на складе: {p.quantity}\n"
            )
        self.txt_hint.insert("end", "\n=== ПОСТАВЩИКИ ===\n")
        for s in self.container["suppliers"].list_suppliers():
            self.txt_hint.insert(
                "end",
                f"  [{s.id}] {s.name} — {s.contact_person}, {s.phone}\n"
            )