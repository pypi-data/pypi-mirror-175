from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from typing import Literal, Union
from pydantic.fields import ModelField
from pyspedfiscal.exception import ValorCampoInvalido
from enum import Enum


class Campo(ABC):
    @classmethod
    @abstractmethod
    def __get_validators__(cls):
        pass

    @classmethod
    @abstractmethod
    def validate(cls, v, field: ModelField) -> Union[date, Literal['']]:
        pass


class CampoData(date, Campo):
    """ Representa uma data """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field: ModelField) -> Union[date, Literal['']]:

        campo = field.name

        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%d%m%Y').date()
            except ValueError:
                if v != '':
                    raise ValorCampoInvalido(campo, v)
                else:
                    return ''
        elif isinstance(v, date):
            return v
        elif isinstance(v, datetime):
            return v.date()
        else:
            raise ValorCampoInvalido(campo, v)


class CampoDecimal(Decimal, Campo):
    """ Representa um numero decimal """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field: ModelField) -> Union[Decimal, Literal['']]:

        campo = field.name

        if isinstance(v, (float, Decimal, int)):
            return Decimal(v)
        elif isinstance(v, str):
            try:
                return Decimal(v.replace(',', '.'))
            except InvalidOperation:
                if v != '':
                    raise ValorCampoInvalido(campo, v)
                else:
                    return ''
        else:
            raise ValorCampoInvalido(campo, v)


class CampoInteiro(int, Campo):
    """ Representa um numero decimal """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field: ModelField) -> Union[int, Literal['']]:

        campo = field.name

        if isinstance(v, int):
            return v

        elif isinstance(v, str):
            try:
                return int(v)
            except ValueError:
                if v == '':
                    return v
                else:
                    raise ValorCampoInvalido(campo, v)
        else:
            raise ValorCampoInvalido(campo, v)


class CampoAlphanumerico(str, Campo):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field: ModelField) -> Union[date, Literal['']]:
        campo = field.name

        if isinstance(v, str):
            return v

        else:
            raise ValorCampoInvalido(campo, v)


class CampoEnumerate(str, Enum):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field: ModelField) -> Union[str, Literal['']]:
        if v == '':
            return ''
        else:
            return cls(v)


class CampoSerie(CampoAlphanumerico):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        yield cls._converter

    @classmethod
    def _converter(cls, valor: str, field: ModelField):
        _valor = valor.strip()

        if _valor.isalnum():
            return _valor.zfill(3)

        return _valor


class CampoCNPJ(CampoInteiro):
    pass


class CampoCPF(CampoInteiro):
    pass


class CampoCNPJouCPF(CampoInteiro):
    pass


class CampoChaveAcesso(CampoAlphanumerico):
    pass


class OutroCampo(Campo):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        pass
