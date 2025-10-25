class Producto:
    def __init__(self, nombre, categoria, cantidad, stock_minimo=0):
        self.__nombre = None
        self.__categoria = None
        self.__cantidad = None
        self.__stock_minimo = None
        self.set_nombre(nombre)
        self.set_categoria(categoria)
        self.set_cantidad(cantidad)
        self.set_stock_minimo(stock_minimo)

    def get_nombre(self):
        return self.__nombre

    def get_categoria(self):
        return self.__categoria

    def get_cantidad(self):
        return self.__cantidad

    def get_stock_minimo(self):
        return self.__stock_minimo

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_categoria(self, categoria):
        self.__categoria = categoria

    def set_cantidad(self, cantidad):
        self.__cantidad = cantidad

    def set_stock_minimo(self, stock_minimo):
        self.__stock_minimo = stock_minimo


class Usuarios:
    def __init__(self, nombre, contrasena):
        self.nombre = nombre
        self.contrasena = contrasena
