"""
- Crear módulo `modelo_orm.py` que contenga:
  - Definición de clases y atributos necesarios, siguiendo el modelo *ORM de Pewee*, para poder persistir los datos importados del dataset en una base de datos relacional de tipo SQLite `obras_urbanas.db`
  - Aquí se debe incluir  además la clase `BaseModel` heredando de `peewee.Model`
"""

# ❗ Todas las clases de este archivo, pueden (o deben) tener métodos dentro.

from peewee import *
import sqlite3

# Creacion de la bdd
sqlite_db = SqliteDatabase("obras_urbanas.db")


# Este es nuetro modelo normalizado. Basado en pewee
class BaseModel(Model):
    class Meta:
        database = sqlite_db


class Etapa(BaseModel):
    etapa = CharField()

    class Meta:
        db_table = "Etapa"


class TipoObra(BaseModel):
    tipo_obra = CharField()

    class Meta:
        db_table = (
            "TipoObra"  # Si no defino un nombre, toma por defecto el nombre de la clase
        )


class AreaResponsable(BaseModel):
    area_responsable = CharField()

    class Meta:
        db_table = "AreaResponsable"


class Ubicacion(BaseModel):
    comuna = IntegerField()  # No sé si la comuna es la mejor opcion para ID
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
    etapa_fk = ForeignKeyField(Etapa, backref="etapa")  # FK
    ubicacion_fk = ForeignKeyField(Ubicacion, backref="ubicacion")  # FK
    tipo_obra_fk = ForeignKeyField(TipoObra, backref="tipo_obra")  # FK
    contratacion_tipo_fk = ForeignKeyField(Contratacion, backref="contratacion")  # FK
    area_responsable_fk = ForeignKeyField(
        AreaResponsable, backref="area_responsable"
    )  # FK
    entorno = CharField()
    nombre = CharField()
    descripcion = CharField()
    monto_contrato = IntegerField()
    fecha_inicio = DateField(null=True)  # Permite valores nulos
    fecha_fin_inicial = DateField(null=True)
    plazo_meses = IntegerField()
    porcentaje_avance = IntegerField()
    licitacion_oferta_empresa = CharField()
    licitacion_anio = DateField(null=True)
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


try:
    sqlite_db.connect()
    print("🔓 Conexión a la BDD abierta")
    # 🔽Crea el archivo obras_urbanas.db, sin registros
    sqlite_db.create_tables(
        [Etapa, TipoObra, AreaResponsable, Ubicacion, Contratacion, Obra]
    )
    print("✍🏼 Estructura de las tablas creada")
except OperationalError as e:
    print("Error al conectarse a la BD ", e)
    sqlite_db.close()
    exit()
finally:
    sqlite_db.close()
    print("🔒 Conexión a la BDD cerrada")
