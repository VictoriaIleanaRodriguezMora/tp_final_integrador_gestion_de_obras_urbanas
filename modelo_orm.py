"""
- Crear módulo `modelo_orm.py` que contenga:
  - Definición de clases y atributos necesarios, siguiendo el modelo *ORM de Pewee*, para poder persistir los datos importados del dataset en una base de datos relacional de tipo SQLite `obras_urbanas.db`
  - Aquí se debe incluir  además la clase `BaseModel` heredando de `peewee.Model`
"""

from peewee import *
from datetime import datetime, date

import os
from dotenv import load_dotenv

load_dotenv()


# Creacion de la bdd vacía
sqlite_db = SqliteDatabase(os.getenv("DB_NAME"))
db_name = os.getenv("DB_NAME")
print(db_name)


# Este es nuetro modelo normalizado. Basado en pewee. El modelo son las tablas que tendrá la bdd
class BaseModel(Model):
    class Meta:
        # database, es una variable de pewee, al asignarle nuestra bdd. El modelo entiende que va a ser una bdd
        database = sqlite_db


class Etapa(BaseModel):
    etapa = CharField(unique=True, null=False)

    class Meta:
        table_name = "Etapa"


class TipoObra(BaseModel):
    tipo_obra = CharField(unique=True, null=False)

    class Meta:
        table_name = "TipoObra"


class AreaResponsable(BaseModel):
    area_responsable = CharField(unique=True, null=False)

    class Meta:
        table_name = "AreaResponsable"


class Ubicacion(BaseModel):
    comuna = IntegerField()
    barrio = CharField()
    direccion = CharField()

    class Meta:
        table_name = "Ubicacion"
        constraints = [SQL("UNIQUE(comuna, barrio, direccion)")]


class Contratacion(BaseModel):
    contratacion_tipo = CharField()
    nro_contratacion = CharField()
    cuit_contratista = CharField()

    class Meta:
        table_name = "Contratacion"


class Obra(BaseModel):
    etapa_fk = ForeignKeyField(Etapa)  # FK
    ubicacion_fk = ForeignKeyField(Ubicacion)  # FK
    tipo_obra_fk = ForeignKeyField(TipoObra)  # FK
    contratacion_tipo_fk = ForeignKeyField(Contratacion)  # FK
    area_responsable_fk = ForeignKeyField(AreaResponsable)  # FK
    entorno = CharField()
    nombre = CharField()
    descripcion = CharField()
    monto_contrato = CharField()
    fecha_inicio = DateField(null=True)  # Permite valores nulos
    fecha_fin_inicial = DateField(null=True)
    plazo_meses = IntegerField()
    porcentaje_avance = IntegerField()
    licitacion_oferta_empresa = CharField()
    licitacion_anio = CharField(null=True)
    mano_obra = IntegerField()
    destacada = CharField()
    expediente_numero = CharField()
    financiamiento = CharField()

    id_obra = None  # No se guarda en la bdd

    class Meta:
        table_name = "Obra"

    # ❗ Son acciones de una obra ya existente
    # “Tengo una obra creada en la BD → aplico una acción → guardo cambios”.
    # métodos de instancia con el objetivo de definir las diferentes etapas de avance de obra
    # Los métodos de instancia necesitan una instancia de una clase y pueden acceder dicha instancia por medio de self

    # Debe modificar la Etapa de la obra a "Proyecto"
    def nuevo_proyecto(self):
        print("\n[ETAPA] nuevo_proyecto iniciado.")
        try:
            # Cambia etapa a "Proyecto"
            etapa_proyecto, _ = Etapa.get_or_create(etapa="Proyecto")
            self.etapa_fk = etapa_proyecto

            self.save()
            print("[OPERACIÓN - SAVE] ✅ Proyecto iniciado correctamente. :)")
            return True

        except Exception as e:
            print(
                f"[ERROR] nuevo_proyecto - no se pudo asignar la etapa Proyecto.': {e}"
            )

    # Debe modificar el tipo de contratacion de la obra
    def iniciar_contratacion(self):
        print("\n[ETAPA] iniciar_contratacion")

        try:
            # Pedir tipo de contratación ya existente en la BD
            user_tipo = (
                input("Ingrese un tipo de contratación existente: ").strip().title()
            )
            tipo_obj = Contratacion.get_or_none(
                Contratacion.contratacion_tipo == user_tipo
            )

            while tipo_obj == None:
                print("[ERROR] Ese tipo de contratación no existe en la bdd.")
                user_tipo = (
                    input("🔄️ Porfavor, ingrese un tipo de contratación existente: ")
                    .strip()
                    .title()
                )
                print(f"Usd ingresó: {user_tipo}")
                tipo_obj = Contratacion.get_or_none(
                    Contratacion.contratacion_tipo == user_tipo
                )

            # Modificar la fila actual
            self.contratacion_tipo_fk.contratacion_tipo = user_tipo
            self.contratacion_tipo_fk.save()

            print("[OPERACIÓN - SAVE] ✅ Contratación actualizada correctamente.")

        except Exception as e:
            print(
                f"[ERROR] iniciar_contratacion - no se pudo asignar la etapa Proyecto.': {e}"
            )

    # Debe pedir: nombre, cuit, número de expediente de la empresa que ajudicará una obra.
    def adjudicar_obra(self):
        expediente_original = self.expediente_numero
        print("\n[ETAPA] Adjudicar obra")
        try:
            # Pedir expediente
            user_expediente = input(
                "Por seguridad, ingrese el número de expediente adjudicado: "
            ).strip()

            # Inicio campo expediente
            # Validar campo EXPEDIENTE vacío
            if not user_expediente:
                print("[ERROR] El expediente no puede quedar vacío.")
                return False
            print(
                f"user_expediente {user_expediente}, expediente_original {expediente_original}"
            )

            while user_expediente != expediente_original:
                print(
                    "[ERROR] El número de expediente ingresado no coincide con el registrado."
                )
                user_expediente = input(
                    "🔄️ Porfavor, ingrese el número de expediente adjudicado: "
                ).strip()

            print(
                "[OPERACIÓN - EVALUACIÓN] ✅ Número de expediente coincide correctamente."
            )
            # Fin campo expediente

            # Inicio nombre empresa adjudicataria
            cambiar_empresa = input(
                "¿Desea cambiar la empresa adjudicataria? (S) Sí, (N) No "
            ).upper()

            if cambiar_empresa == "S":
                user_empresa = input(
                    "Ingrese el nombre de la empresa adjudicataria: "
                ).strip()
                if not user_empresa:
                    print("[CAMPO INVÁLIDO] La empresa no puede quedar vacía.")

                # Validar campo vacío
                while not user_empresa:
                    user_empresa = input("🔄️ Porfavor ingrese un valor válido ").strip()
                # Si sale del bucle es porque ingresó un valor válido
                self.licitacion_oferta_empresa = user_empresa
                self.save()

            if cambiar_empresa == "N":
                print("No se modifica el nombre de la empresa")

            print(
                f"[OPERACIÓN - SAVE] ✅ Empresa adjudicada correctamente."
            )
            # Fin nombre empresa adjudicataria
        except Exception as e:
            print(f"[ERROR] - no se pudo adjudicar la empresa': {e}")

    # Debe pedir: nueva fecha de inicio, nueva fecha de fin inicial
    def iniciar_obra(self):
        print("\n[ETAPA] Iniciar obra")
        try:
            user_inicio = input("Fecha de inicio (DD/MM/YYYY): ").strip()
            fin = input("Fecha fin inicial (DD/MM/YYYY): ").strip()

            # Convertimos a datetime.date
            fecha_inicio = datetime.strptime(user_inicio, "%d/%m/%Y").date()
            while not fecha_inicio:
                print("[CAMPO INVÁLIDO] Formato de fecha inválido")
                user_inicio = input("Porfavor, ingrese una fecha válida (DD/MM/YYYY)")
                fecha_inicio = datetime.strptime(user_inicio, "%d/%m/%Y").date()

            fecha_fin = datetime.strptime(fin, "%d/%m/%Y").date()

            self.fecha_inicio = fecha_inicio
            self.fecha_fin_inicial = fecha_fin
            self.save()

            print("✔ Fechas actualizadas correctamente.")
            return True

        except ValueError as e:
            print("[ERROR] Formato de fecha inválido.", e)
            return False

    # Debe pedir: un número, el nuevo porcentaje a actualizar
    def actualizar_porcentaje_avance(self):
        print("\n[ETAPA] Actualizar porcentaje de avance")

        try:
            nuevo = int(input("Ingrese nuevo porcentaje (0 a 100): ").strip())
            if not 0 <= nuevo <= 100:
                raise ValueError()

            self.porcentaje_avance = nuevo
            self.save()

            print("✔ Porcentaje actualizado.")
            return True

        except ValueError:
            print("[ERROR] Debe ingresar un número entre 0 y 100.")
            return False

    # Al invocar este método, el porcentaje de avance pasa a 100. Y la etapa = 'Finalizada'
    def finalizar_obra(self):
        print("\n[ETAPA] Finalizar obra")

        self.porcentaje_avance = 100

        # Cambia etapa a "Finalizada"
        etapa_fin, _ = Etapa.get_or_create(etapa="Finalizada")
        self.etapa_fk = etapa_fin

        self.save()
        print("✔ Obra finalizada correctamente.")
        return True

    # Al invocar este método la etapa =  'Rescindida'
    def rescindir_obra(self):
        print("\n[ETAPA] Rescindir obra")

        etapa_res, _ = Etapa.get_or_create(etapa="Rescindida")
        self.etapa_fk = etapa_res
        self.save()

        print("✔ Obra rescindida correctamente.")
        return True

    # Opcionales
    def incrementar_plazo(self):
        print("\n[ETAPA] Incrementar plazo")

        try:
            extra = int(input("¿Cuántos meses desea agregar?: ").strip())
            if extra < 0:
                raise ValueError()

            self.plazo_meses += extra
            self.save()

            print("✔ Plazo incrementado correctamente.")
            return True

        except ValueError:
            print("[ERROR] Ingrese un número válido.")
            return False

    def incrementar_mano_obra(self):
        print("\n[ETAPA] Incrementar mano de obra")

        try:
            extra = int(input("¿Cuántas personas agregar a mano de obra?: ").strip())
            if extra < 0:
                raise ValueError()

            self.mano_obra += extra
            self.save()

            print("✔ Mano de obra actualizada.")
            return True

        except ValueError:
            print("[ERROR] Ingrese un número válido.")
            return False


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
