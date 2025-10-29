"""
Crie uma classe Funcionario com:
Atributo de classe empresa = "TechCorp"
Atributos de instância nome e salario
Método exibir_dados() que mostra tudo formatado
Instancie 3 funcionários e altere o nome da empresa. Observe o que muda.

"""

class Funcionario:
    empresa = "TechCorp"
    _lista   = []
    def __init__(self, nome, salario):
        self.nome    = nome
        self.salario = salario
        Funcionario._lista.append(self)

    def exibir_dados(self):
        for func in Funcionario._lista:
            print(f"----------------{Funcionario.empresa}--------------------")
            print(f"Nome: {func.nome} | Salário: {func.salario} ")



# Teste

Funcionario.empresa = "Kennedh Inc."

func1 = Funcionario("Sérgio", 2800)
func2 = Funcionario("Ana", 3200)
func3 = Funcionario("Paulo", 1900)

func1.exibir_dados()
