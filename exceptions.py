class WarehouseException(Exception):
    pass


class ProductNotFoundException(WarehouseException):
    pass


class SupplierNotFoundException(WarehouseException):
    pass


class DuplicateSKUException(WarehouseException):
    pass


class NotEnoughStockException(WarehouseException):
    pass