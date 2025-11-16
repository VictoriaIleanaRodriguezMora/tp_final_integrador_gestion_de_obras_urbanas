"""
- Crear módulo `modelo_orm.py` que contenga:
  - Definición de clases y atributos necesarios, siguiendo el modelo *ORM de Pewee*, para poder persistir los datos importados del dataset en una base de datos relacional de tipo SQLite `obras_urbanas.db`
  - Aquí se debe incluir  además la clase `BaseModel` heredando de `peewee.Model`
"""

from peewee import *

# Creacion de la bdd
db = SqliteDatabase("obras_urbanas.db")


class BaseModel(Model):
    class Meta:
        database = db


class Etapa(BaseModel):
    etapa = CharField(unique=True)

    class Meta:
        db_table = "Etapa"


class TipoObra(BaseModel):
    tipo = CharField(unique=True)

    class Meta:
        db_table = "Tipo obra"


class AreaResponsable(BaseModel):
    area_responsable = CharField(unique=True)

    class Meta:
        db_table = "Area responsable"


class Ubicacion(BaseModel):
    comuna = IntegerField(unique=True)  # Bo sé si la comuna es la mejor opcion para ID
    barrio = CharField()
    nombre_calle = CharField()
    altura = CharField()

    class Meta:
        db_table = "Ubicacion"


# no estoy seguro si dejar este asi o hacerlo parte de la tabla obra
class Contratacion(BaseModel):
    nro_contratacion = CharField(
        unique=True
    )  # El tipo de contratacion es algo que se repite, no es único. En cambio el nro si es unico.
    tipo_contratacion = CharField()
    cuit_contratista = CharField()

    class Meta:
        db_table = "Contratacion"


class Obra(BaseModel):
    expediente_numero = CharField(unique=True)
    etapa = ForeignKeyField(Etapa, backref="etapa")  # FK
    ubicacion = ForeignKeyField(Ubicacion, backref="ubicacion")  # FK
    tipo = ForeignKeyField(TipoObra, backref="tipo")  # FK
    contratacion_tipo = ForeignKeyField(Contratacion, backref="contratacion")  # FK
    area_responsable = ForeignKeyField(
        AreaResponsable, backref="area_responsable"
    )  # FK
    entorno = CharField()
    nombre = CharField()
    descripcion = CharField()
    monto_contrato = IntegerField()
    fecha_inicio = DateField()
    fecha_fin_inicial = DateField()
    plazo_meses = IntegerField()
    porcentaje_avance = IntegerField()
    licitacion_oferta_empresa = CharField()
    licitacion_anio = DateField()
    mano_obra = IntegerField()
    destacada = CharField()
    financiamiento = CharField()  #

    class Meta:
        db_table = "Obra"

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

