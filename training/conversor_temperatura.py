"""
Crie uma classe ConversorTemperatura com:
@staticmethod para converter Celsius ↔ Fahrenheit
@classmethod para criar um objeto a partir de um valor em Fahrenheit
"""


class Temperatura:
    def __init__(self, celsius):
        self.celsius = celsius

    def exibir(self):
        return f"{self.celsius}°C"

    @staticmethod
    def converter_fahrenheit_para_celsius(fahrenheit):
        return (fahrenheit - 32) * 5 / 9

    @classmethod
    def from_fahrenheit(cls, fahrenheit):
        celsius = cls.converter_fahrenheit_para_celsius(fahrenheit)
        return cls(celsius)

# Teste

temp1 = Temperatura(25)
print(temp1.exibir())

celsius = Temperatura.converter_fahrenheit_para_celsius(77)
print(celsius)

temp2 = Temperatura.from_fahrenheit(77)
print(temp2.exibir())