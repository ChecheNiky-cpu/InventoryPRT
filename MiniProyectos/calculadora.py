class Calculadora:
    def sumar(self, a, b):
        return a + b

    def restar(self, a, b):
        return a - b

    def multiplicar(self, a, b):
        return a * b

    def dividir(self, a, b):
        if b != 0:
            return a / b
        else:
            return "Error: División por cero no permitida."


calc = Calculadora()


def main():
    print("Calculadora Simple")
    print("1. Sumar")
    print("2. Restar")
    print("3. Multiplicar")
    print("4. Dividir")

    opcion = input("Seleccione una operación (1/2/3/4): ")

    if opcion in ['1', '2', '3', '4']:
        num1 = float(input("Ingrese el primer número: "))
        num2 = float(input("Ingrese el segundo número: "))

        if opcion == '1':
            print(f"{num1} + {num2} = {calc.sumar(num1, num2)}")
        elif opcion == '2':
            print(f"{num1} - {num2} = {calc.restar(num1, num2)}")
        elif opcion == '3':
            print(f"{num1} * {num2} = {calc.multiplicar(num1, num2)}")
        elif opcion == '4':
            print(f"{num1} / {num2} = {calc.dividir(num1, num2)}")
    else:
        print("Opción inválida.")
