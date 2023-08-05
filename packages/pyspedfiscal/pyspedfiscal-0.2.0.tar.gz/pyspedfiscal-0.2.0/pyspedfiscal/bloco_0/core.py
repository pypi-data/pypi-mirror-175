from typing import List
from ..models import Bloco
from .registro_0000 import Registro0000
from .registro_0001 import Registro0001
from .registro_0200 import Registro0200
from .registro_0460 import Registro0460


class Bloco0(Bloco):
    def __init__(self):
        self.registro_0000: Registro0000 = None
        self.registro_0001: Registro0001 = None

    @classmethod
    def ler_registros(cls, registros: List[str]) -> 'Bloco0':
        bloco = cls()

        for registro in registros:
            tipo_registro = registro[1:5].upper()

            # Nivel 0 - Abertura do Arquivo Digital
            if tipo_registro == '0000':
                bloco.registro_0000 = Registro0000.ler_registro(registro)

            # Nivel 1 - Registro Pai
            if tipo_registro == '0001':
                bloco.registro_0001 = Registro0001.ler_registro(registro)

            # Nivel 2 - Filho de 0001
            if tipo_registro == '0200':
                bloco.registro_0001.registros_0200.append(
                    Registro0200.ler_registro(registro)
                )

            # Nivel 2 - Filho de 0001
            if tipo_registro == '0460':
                bloco.registro_0001.registros_0460.append(
                    Registro0460.ler_registro(registro)
                )

        return bloco
