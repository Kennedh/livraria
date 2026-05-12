class Autor:
    def __init__(self, nome: str):
        if not nome or not nome.strip():
            raise ValueError("Nome do autor não pode ser vazio")
        self._nome = nome.strip()

    @property
    def nome(self):
        return self._nome

    def __str__(self):
        return self._nome

    def __eq__(self, other):
        if isinstance(other, Autor):
            return self._nome.lower() == other._nome.lower()
        return False

    def __hash__(self):
        return hash(self._nome.lower())