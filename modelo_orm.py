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


class Contratacion(BaseModel):
    contratacion_tipo = CharField()
    nro_contratacion = CharField()
    cuit_contratista = CharField()

    class Meta:
        db_table = "Contratacion"


class Obra(BaseModel):
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
    expediente_numero = CharField()
    financiamiento = CharField()  #

    class Meta:
        db_table = "Obra"

    # ❗ Son acciones de una obra ya existente
    # “Tengo una obra creada en la BD → aplico una acción → guardo cambios”.
    # métodos de instancia con el objetivo de definir las diferentes etapas de avance de obra
    # Los métodos de instancia necesitan una instancia de una clase y pueden acceder dicha instancia por medio de self

    # Debe modificar la Etapa de la obra
    def nuevo_proyecto(self, nueva_etapa: str):
        # self es el objeto Obra
        # self.etapa_fk - es el objeto Etapa vinculado por la FK
        # self.etapa_fk.etapa - es el valor del campo etapa dentro del modelo Etapa
        print("nuevo_proyecto")
        print("Obra completa:", self.__data__)

        try:
            # buscar o crear la etapa nueva_etapa
            etapa_pewee, created = Etapa.get_or_create(etapa=nueva_etapa)

            # created es un booleano que devuelve True o False
            if created:
                print(f"etapa {nueva_etapa} creada exitosamente en la DB.")
                # asignar la etapa a la obra
                self.etapa_fk = etapa_pewee
                self.save()  # guardar los cambios

            print("ID de etapa FK:", self.etapa_fk.id)
            print("Nombre etapa:", self.etapa_fk.etapa)

            # mostrar todos los atributos
            print("Obra completa después de los cambios:", self.__data__)
        except Exception as e:
            print(f"[ERROR] - al validar los registros': {e}")

    # Debe modificar el tipo de contratacion de la obra
    def iniciar_contratacion(self):
        try:
            iniciar_contratacion = input("Ingrese un tipo de contratación existente: ").strip()
            nuevo_tipo_contratacion = Contratacion.get_or_none(contratacion_tipo=iniciar_contratacion)
            if not nuevo_tipo_contratacion:
                raise ValueError("El tipo de contratación ingresado no existe en la base de datos")
        except Exception as e:
            print(f"[ERROR] - al buscar el Tipo de Contratación': {e}")

        try:
            nuevo_nro_contratacion = input("Ingrese un número de contratación: ").strip()
            if not nuevo_nro_contratacion:
                raise ValueError("El número de contratación no es válido")
        except Exception as e:
            print(f"[ERROR] - al ingresar un número de contratación': {e}")
        
        try:
            self.contratacion_tipo_fk.contratacion_tipo = nuevo_tipo_contratacion
            self.contratacion_tipo_fk.nro_contratacion = nuevo_nro_contratacion
            self.contratacion_tipo_fk.save()
            self.save()
            print("Obra completa después de los cambios:", self.__data__)
        except Exception as e:
            print(f"[ERROR] - al guardar el tipo y número de contratación': {e}")
            return False

    # Debe pedir: nombre, cuit de la empresa que ajudicará una obra. Y número de expediente
    def adjudicar_obra(self):
        try:
            nombre_empresa = input("Ingrese el nombre de la empresa adjudicataria: ").strip()
            cuit_empresa = input("Ingrese el CUIT de la empresa adjudicataria: ").strip()

            contratacion_existente = Contratacion.get_or_none(
            Contratacion.cuit_contratista == cuit_empresa
            )

            if not contratacion_existente:
                raise ValueError("No existe una contratación con ese CUIT en la base de datos.")

            nro_expediente = input("Ingrese número de expediente: ").strip()
        
            self.licitacion_oferta_empresa = nombre_empresa       
            self.expediente_numero = nro_expediente               
            self.save()

            print(f"[OK] La obra '{self.nombre}' fue adjudicada a {nombre_empresa} (CUIT {cuit_empresa}).")
        
        except Exception as e:
         print("[ERROR en adjudicar_obra]", e)

           
    # Debe pedir: nueva fecha de inicio, nueva fecha de fin inicial
    def iniciar_obra(self):
        try:
            self.destacada = input("¿Es destacada? (SI/NO): ").strip()

            fecha_ini = input("Fecha inicio (DD/MM/YYYY): ").strip()
            fecha_fin = input("Fecha fin inicial (DD/MM/YYYY): ").strip()

            self.fecha_inicio = fecha_ini
            self.fecha_fin_inicial = fecha_fin

            financiamiento = input("Fuente de financiamiento: ").strip()
            self.financiamiento = financiamiento

            self.mano_obra = int(input("Mano de obra inicial: "))

            self.save()
            print("[OK] Obra iniciada.")

        except Exception as e:
            print("[ERROR en iniciar_obra]", e)

    # Debe pedir: un número, el nuevo porcentaje a actualizar
    def actualizar_porcentaje_avance(self):
        try:
            nuevo = int(input("Nuevo porcentaje de avance (0-100): "))

            if not 0 <= nuevo <= 100:
                raise ValueError("Debe estar entre 0 y 100.")

            self.porcentaje_avance = nuevo
            self.save()

            print("[OK] Avance actualizado.")

        except Exception as e:
            print("[ERROR en actualizar_porcentaje_avance]", e)

    # Al invocar este método, el porcentaje de avance pasa a 100. Y la etapa = 'Finalizada'
    def finalizar_obra(self):
        try:
            etapa_fin = Etapa.get_or_none(etapa="Finalizada")
            self.etapa_fk = etapa_fin
            self.porcentaje_avance = 100
            self.save()
            print("[OK] Obra finalizada.")
        except Exception as e:
            print("[ERROR en finalizar_obra]", e)

    # Al invocar este método la etapa =  'Rescindida'
    def rescindir_obra(self):
        try:
            etapa_res = Etapa.get_or_none(etapa="Rescisión")
            self.etapa_fk = etapa_res
            self.save()
            print("[OK] Obra rescindida.")
        except Exception as e:
            print("[ERROR en rescindir_obra]", e)

    # Opcionales
    def incrementar_plazo(self):
        pass

    def incrementar_mano_obra(self):
        pass


# PASOS PARA PROBAR ESTOS MÉTODOS DE INSTANCIA
"""
1) Levantar la bdd
2) Obtener una Obra cualquiera por nombre o id, (O crear una de prueba)
3) Llamar a los métodos de instancia:
    obra.iniciar_obra()
    obra.actualizar_porcentaje_avance(80)
    obra.finalizar_obra()



GestionarObra.conectar_db()
obra = Obra.get_by_id(1)
obra.nuevo_proyecto()
obra.iniciar_contratacion()
obra.adjudicar_obra("Empresa SA", "30-12345678-9")
obra.iniciar_obra(date(2025,1,3), date(2025,12,20))
obra.actualizar_porcentaje_avance(40)
obra.incrementar_plazo(2)
obra.finalizar_obra()
"""
