"""
- Crear módulo `modelo_orm.py` que contenga:
  - Definición de clases y atributos necesarios, siguiendo el modelo *ORM de Pewee*, para poder persistir los datos importados del dataset en una base de datos relacional de tipo SQLite `obras_urbanas.db`
  - Aquí se debe incluir  además la clase `BaseModel` heredando de `peewee.Model`
"""

# ❗ Todas las clases de este archivo, pueden (o deben) tener métodos dentro.

from peewee import *
import sqlite3

import os
from dotenv import load_dotenv

load_dotenv()

# Creacion de la bdd
sqlite_db = SqliteDatabase(os.getenv("DB_NAME"))
print(os.getenv("DB_NAME"))


# Este es nuetro modelo normalizado. Basado en pewee
class BaseModel(Model):
    class Meta:
        database = sqlite_db


class Etapa(BaseModel):
    etapa = CharField(unique=True, null=False)

    class Meta:
        db_table = "Etapa"


class TipoObra(BaseModel):
    tipo_obra = CharField(unique=True, null=False)

    class Meta:
        db_table = (
            "TipoObra"  # Si no defino un nombre, toma por defecto el nombre de la clase
        )


class AreaResponsable(BaseModel):
    area_responsable = CharField(unique=True, null=False)

    class Meta:
        db_table = "AreaResponsable"


class Ubicacion(BaseModel):
    comuna = IntegerField()  # No sé si la comuna es la mejor opcion para ID
    barrio = CharField()
    # nombre_calle = CharField()
    # altura = CharField()
    direccion = CharField()

    class Meta:
        db_table = "Ubicacion"


# no estoy seguro si dejar este asi o hacerlo parte de la tabla obra
class Contratacion(BaseModel):
    nro_contratacion = CharField()
    contratacion_tipo = CharField()
    cuit_contratista = CharField()

    class Meta:
        db_table = "Contratacion"


class Obra(BaseModel):
    expediente_numero = CharField(unique=True)
    etapa_fk = ForeignKeyField(Etapa)  # FK
    ubicacion_fk = ForeignKeyField(Ubicacion)  # FK
    tipo_obra_fk = ForeignKeyField(TipoObra)  # FK
    contratacion_tipo_fk = ForeignKeyField(Contratacion)  # FK
    area_responsable_fk = ForeignKeyField(AreaResponsable)  # FK
    entorno = CharField()
    nombre = CharField()
    descripcion = CharField()
    monto_contrato = IntegerField()
    fecha_inicio = DateField(null=True)  # Permite valores nulos
    fecha_fin_inicial = DateField(null=True)
    plazo_meses = IntegerField()
    porcentaje_avance = IntegerField()
    licitacion_oferta_empresa = CharField()
    licitacion_anio = CharField(null=True)
    mano_obra = IntegerField()
    destacada = CharField()
    financiamiento = CharField()  #

    class Meta:
        db_table = "Obra"

    # métodos de instancia con el objetivo de definir las diferentes etapas de avance de obra
    # Los métodos de instancia necesitan una instancia de una clase y pueden acceder dicha instancia por medio de self

    def nuevo_proyecto():
        pass

    def iniciar_contratacion():
        pass

    def adjudicar_obra():
        pass

    def iniciar_obra():
        pass

    def actualizar_porcentaje_avance():
        pass

    def finalizar_obra():
        pass

    def rescindir_obra():
        pass

    def incrementar_plazo():
        pass

    def incrementar_mano_obra():
        pass

    # dejo afuera las columnas que no considero relevantes
    """
    lat = CharField()
    lng = CharField()
    imagen_1 = CharField()
    imagen_2 = CharField()
    imagen_3 = CharField()
    imagen_4 = CharField()
    beneficiarios = CharField()
    compromiso = CharField()
    ba_elige = CharField()
    link_interno = CharField()
    pliego_descarga = CharField()
    estudio_ambiental_descarga = CharField()
    """
