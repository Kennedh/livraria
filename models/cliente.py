class Cliente:
    _contador_id = 0

    def __init__(self, nome: str, email: str = None):
        if not nome or not nome.strip():
            raise ValueError("Nome do cliente não pode ser vazio")
        
        Cliente._contador_id += 1
        self._id = Cliente._contador_id
        self._nome = nome.strip()
        self._email = email

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        self._email = valor

    def __str__(self):
        return f"ID: {self._id} | Nome: {self._nome}" + \
               (f" | Email: {self._email}" if self._email else "")