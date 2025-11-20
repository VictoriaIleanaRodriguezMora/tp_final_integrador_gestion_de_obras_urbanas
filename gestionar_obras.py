from abc import ABC
import pandas as pd
from peewee import *
from modelo_orm import *
import sqlite3
from modelo_orm import sqlite_db
from datetime import datetime, date

import os
from dotenv import load_dotenv

load_dotenv()
CVS_PATH = os.getenv("CVS_PATH")

from datetime import *

from utilities.utility_nueva_obra import (
    utility_nueva_obra,
    utility_nueva_obra_multi,
    pedir_str,
    pedir_int,
    pedir_fecha,
    generar_nro_contratacion,
    obtener_o_crear_ubicacion,
)


class GestionarObra(ABC):
    df_limpio = []
    modelo = 0
    columna = 0

    # sentencias necesarias para manipular el dataset a través de un objeto Dataframe del módulo “pandas”.
    @classmethod
    def extraer_datos(cls):
        try:
            df = pd.read_csv(CVS_PATH, sep=";", encoding="latin1")
            return df

        except FileNotFoundError as e:
            print("No se ha encontrado el archivo csv", e)

    # sentencias necesarias para realizar la conexión a la base de datos “obras_urbanas.db”.
    @classmethod
    def conectar_db(cls, fn):
        try:
            if sqlite_db.is_closed():
                sqlite_db.connect()
                print(f"🔌 Bdd conectada en {fn}")
        except FileNotFoundError as e:
            print("No se ha podido conectar con la base de datos", e)

    # sentencias necesarias para realizar la desconexión a la base de datos “obras_urbanas.db”.
    @classmethod
    def desconectar_db(cls, fn):
        try:
            if not sqlite_db.is_closed():
                sqlite_db.close()
                print(f"🔌 Bdd desconectada de {fn}")
        except FileNotFoundError:
            print(
                "No se ha podido cerrar  la base de datos"
            )  # 🟡 Agregar info del error

    # sentencias necesarias para realizar la creación de la estructura de la base de datos (tablas y relaciones) utilizando el método de instancia “create_tables(list)” del módulo “peewee”.
    @classmethod
    def mapear_orm(cls):
        print("[MÉTODO] mapear_orm")
        try:
            GestionarObra.conectar_db("mapear_orm")
            sqlite_db.create_tables(
                [Etapa, TipoObra, AreaResponsable, Ubicacion, Contratacion, Obra]
            )

            print("✅ Datos mapeados")
            print("✨ Los datos se mapearon correctamente")
        except Exception as e:
            print("[ERROR] mapear_orm - Error al mapear_orm", e)
        finally:
            GestionarObra.desconectar_db("mapear_orm")

    # sentencias necesarias para persistir los datos de las obras (ya transformados y “limpios”) que contiene el objeto Dataframe en la base de  datos relacional SQLite. Para ello se debe utilizar el método de clase Model create() en  cada una de las clase del modelo ORM definido.

    @classmethod
    def limpiar_datos(cls):
        print("[MÉTODO] limpiar_datos")
        try:
            df = cls.extraer_datos()

            # 🟢 Normalizar nombres de columnas
            df.columns = (
                df.columns.str.strip()
                .str.lower()
                .str.replace("-", "_")
                .str.replace(" ", "_")
            )

            # 🟢 Crear df_limpio (recién ACÁ lo creamos)
            cls.df_limpio = (
                df.drop(
                    columns=[
                        "lat",
                        "lng",
                        "imagen_1",
                        "imagen_2",
                        "imagen_3",
                        "imagen_4",
                        "beneficiarios",
                        "compromiso",
                        "ba_elige",
                        "link_interno",
                        "pliego_descarga",
                        "estudio_ambiental_descarga",
                    ]
                )
                .drop_duplicates()
                .assign(monto_contrato=df["monto_contrato"].str.strip())
                .fillna(
                    {
                        "expediente_numero": 0,
                        "destacada": "NO",
                        "contratacion_tipo": "Desconocida",
                        "tipo": "Desconocido",
                        "descripcion": "Sin descripcion",
                        "barrio": "Desconocido",
                        "direccion": "Desconocido",
                        "licitacion_oferta_empresa": "Desconocido",
                        "nro_contratacion": "Desconocido",
                        "cuit_contratista": "Desconocido",
                        "comuna": 0,
                        "monto_contrato": 0,
                        "fecha_inicio": 0,
                        "fecha_fin_inicial": 0,
                        "plazo_meses": 0,
                        "licitacion_anio": 0,
                        "mano_obra": 0,
                        "financiamiento": "Desconocido",
                        "etapa": "Desconocida",
                        "porcentaje_avance": 0,
                        "nombre": "Sin nombre",
                        "tipo_obra": "Desconocido",
                        "area_responsable": "Desconocida",
                    }
                )
            )

            # 🟢 Reemplazar ACENTOS en TODAS las columnas string
            cols = cls.df_limpio.select_dtypes(include=["object"]).columns

            for c in cols:
                cls.df_limpio[c] = (
                    cls.df_limpio[c]
                    .astype(str)
                    .str.replace("á", "a")
                    .str.replace("é", "e")
                    .str.replace("í", "i")
                    .str.replace("ó", "o")
                    .str.replace("ú", "u")
                    .str.replace("Á", "A")
                    .str.replace("É", "E")
                    .str.replace("Í", "I")
                    .str.replace("Ó", "O")
                    .str.replace("Ú", "U")
                )

            # 🟢 Normalizar otras columnas
            cls.df_limpio["etapa"] = (
                cls.df_limpio["etapa"]
                .str.capitalize()
                .str.strip()
                .replace("", "Desconocida")
                .fillna("Desconocida")
            )

            cls.df_limpio["tipo"] = (
                cls.df_limpio["tipo"]
                .astype(str)
                .str.strip()
                .str.title()
                .replace("", "Desconocido")
                .fillna("Desconocido")
            )

            cls.df_limpio["direccion"] = cls.df_limpio["direccion"].str.upper()

            cls.df_limpio["barrio"] = cls.df_limpio["barrio"].str.lower().str.strip()

            cls.df_limpio = cls.df_limpio.drop_duplicates()

            cls.df_limpio.to_csv("datos_limpios.csv", index=False)

            print("✅ Datos limpiados")
            return cls.df_limpio

        except Exception as e:
            print("[ERROR] limpiar_datos - Error al limpiar datos: ", e)

    # sentencias necesarias para persistir los datos de las obras (ya transformados y “limpios”)
    @classmethod
    def cargar_datos(cls, df_limpio):
        GestionarObra.conectar_db("cargar_datos")
        try:
            print("[MÉTODO] cargar_datos")
            for index, row in df_limpio.iterrows():
                ubicacion_obj, booleano = Ubicacion.get_or_create(
                    comuna=row["comuna"],
                    barrio=row["barrio"],
                    direccion=row["direccion"],
                )

                nro_contratacion_utils = generar_nro_contratacion()

                contratacion_obj, booleano = Contratacion.get_or_create(
                    contratacion_tipo=row["contratacion_tipo"],
                    nro_contratacion=nro_contratacion_utils,
                    cuit_contratista=row["cuit_contratista"],
                )

                etapa_obj, booleano = Etapa.get_or_create(etapa=row["etapa"])

                tipo_obj, booleano = TipoObra.get_or_create(tipo_obra=row["tipo"])

                area_obj, booleano = AreaResponsable.get_or_create(
                    area_responsable=row["area_responsable"]
                )

                Obra.create(
                    expediente_numero=row["expediente_numero"],
                    etapa_fk=etapa_obj,
                    ubicacion_fk=ubicacion_obj,
                    tipo_obra_fk=tipo_obj,
                    contratacion_tipo_fk=contratacion_obj,
                    area_responsable_fk=area_obj,
                    entorno=row["entorno"],
                    nombre=row["nombre"],
                    descripcion=row["descripcion"],
                    monto_contrato=row["monto_contrato"],
                    fecha_inicio=row["fecha_inicio"],
                    fecha_fin_inicial=row["fecha_fin_inicial"],
                    plazo_meses=row["plazo_meses"],
                    porcentaje_avance=row["porcentaje_avance"],
                    licitacion_oferta_empresa=row["licitacion_oferta_empresa"],
                    licitacion_anio=row["licitacion_anio"],
                    mano_obra=row["mano_obra"],
                    destacada=row["destacada"],
                    financiamiento=row["financiamiento"],
                )

            print("✅ Datos cargados.")
            print("✨ Se realizó la carga de datos")
        except Exception as e:
            print("[ERROR] cargar_datos - Error al cargar_datos", e)
        finally:
            GestionarObra.desconectar_db("cargar_datos")

    # las sentencias necesarias para crear nuevas instancias de Obra.
    @classmethod
    def nueva_obra(cls):
        try:
            print("[MÉTODO] nueva_obra")
            # Area responsable
            nueva_area_responsable = utility_nueva_obra(
                AreaResponsable, "area_responsable", "el área responsable"
            )

            # Contratación
            nueva_contratacion = utility_nueva_obra_multi(
                Contratacion,
                {
                    # "nro_contratacion": "el número de contratación",
                    "contratacion_tipo": "el tipo de contratación",
                    "cuit_contratista": "el cuit del contratista",
                },
            )

            # Etapa
            nva_etapa = utility_nueva_obra(Etapa, "etapa", "el estado de la etapa")

            # Tipo de obra
            nvo_tipo = utility_nueva_obra(TipoObra, "tipo_obra", "el tipo de obra")

            nueva_ubicacion = obtener_o_crear_ubicacion()

            # Nueva obra.
            nombre = pedir_str("Ingrese el nombre de la obra: ")
            descripcion = pedir_str("Ingrese la descripción de la obra: ")
            expediente_numero = pedir_str("Ingrese número de expediente: ")
            entorno = pedir_str("Ingrese el entorno: ")

            monto_contrato = pedir_int("Ingrese el monto del contrato: ")
            fecha_inicio = pedir_fecha("Ingrese la fecha de inicio (DD/MM/YYYY): ")
            fecha_fin_inicial = pedir_fecha(
                "Ingrese la fecha de finalización (DD/MM/YYYY): "
            )

            plazo_meses = pedir_int("Ingrese el plazo en meses: ")
            porcentaje_avance = pedir_int("Ingrese el porcentaje de avance: ")

            licitacion_oferta_empresa = pedir_str("Ingrese la empresa: ")
            licitacion_anio = pedir_int("Ingrese el año: ")

            mano_obra = pedir_int("Ingrese la mano de obra: ")
            destacada = pedir_str("Ingrese si es una obra destacada (SI/NO): ")
            financiamiento = pedir_str("Ingrese el financiamiento: ")

            nueva_obra = Obra(
                area_responsable_fk=nueva_area_responsable,
                contratacion_tipo_fk=nueva_contratacion,
                etapa_fk=nva_etapa,
                tipo_obra_fk=nvo_tipo,
                ubicacion_fk=nueva_ubicacion,
                nombre=nombre,
                descripcion=descripcion,
                expediente_numero=expediente_numero,
                entorno=entorno,
                monto_contrato=monto_contrato,
                fecha_inicio=fecha_inicio,
                fecha_fin_inicial=fecha_fin_inicial,
                plazo_meses=plazo_meses,
                porcentaje_avance=porcentaje_avance,
                licitacion_oferta_empresa=licitacion_oferta_empresa,
                licitacion_anio=licitacion_anio,
                mano_obra=mano_obra,
                destacada=destacada,
                financiamiento=financiamiento,
            )

            obj_sin_ids = {
                "nombre": nombre,
                "descripcion": descripcion,
                "expediente_numero": expediente_numero,
                "entorno": entorno,
                "monto_contrato": monto_contrato,
                "fecha_inicio": fecha_inicio,
                "fecha_fin_inicial": fecha_fin_inicial,
                "plazo_meses": plazo_meses,
                "porcentaje_avance": porcentaje_avance,
                "licitacion_oferta_empresa": licitacion_oferta_empresa,
                "licitacion_anio": licitacion_anio,
                "mano_obra": mano_obra,
                "destacada": destacada,
                "financiamiento": financiamiento,
                # Mostramos las FK sin ids, para que sea más amigable
                "area_responsable": nueva_area_responsable.area_responsable,
                "contratacion": {
                    "tipo": nueva_contratacion.contratacion_tipo,
                    "nro": nueva_contratacion.nro_contratacion,
                    "cuit": nueva_contratacion.cuit_contratista,
                },
                "etapa": nva_etapa.etapa,
                "tipo_obra": nvo_tipo.tipo_obra,
                "ubicacion": {
                    "comuna": nueva_ubicacion.comuna,
                    "barrio": nueva_ubicacion.barrio,
                    "direccion": nueva_ubicacion.direccion,
                },
            }

            nueva_obra.save()
            print(f"[GUARDADO] - Obra '{nueva_obra.nombre}' creada exitosamente.")
            print(f"[GUARDADO] - {obj_sin_ids}")
            return nueva_obra

        except Exception as e:
            print(f"[ERROR] nueva_obra - No se pudo crear la nueva Obra: {e}")
            return None

    @classmethod
    def obtener_indicadores(cls):
        try:
            cls.conectar_db("obtener_indicadores")

            indicadores = {}

            # a. Listado de todas las áreas responsables
            indicadores["areas_responsables"] = [
                a.area_responsable for a in AreaResponsable.select()
            ]

            # b. Listado de todos los tipos de obra
            indicadores["tipos_obra"] = [t.tipo_obra for t in TipoObra.select()]

            # c. Cantidad de obras por etapa
            indicadores["obras_por_etapa"] = list(
                Obra.select(
                    Etapa.etapa.alias("etapa"), fn.COUNT(Obra.id).alias("cantidad")
                )
                .join(Etapa)
                .group_by(Etapa.etapa)
                .dicts()
            )

            # d. Cantidad y monto total por tipo de obra
            datos_tipo = []
            for tipo in TipoObra.select():
                cantidad = Obra.select().where(Obra.tipo_obra_fk == tipo).count()

                monto = (
                    Obra.select(fn.SUM(Obra.monto_contrato))
                    .where(Obra.tipo_obra_fk == tipo)
                    .scalar()
                ) or 0

                datos_tipo.append(
                    {
                        "tipo": tipo.tipo_obra,
                        "cantidad": cantidad,
                        "monto_total": int(monto),
                    }
                )

            indicadores["datos_por_tipo"] = datos_tipo

            # e. Barrios de comunas 1, 2 y 3
            indicadores["barrios_123"] = list(
                Ubicacion.select(Ubicacion.comuna, Ubicacion.barrio)
                .where(Ubicacion.comuna.in_([1, 2, 3]))
                .group_by(Ubicacion.comuna, Ubicacion.barrio)
                .distinct()
                .order_by(Ubicacion.comuna, Ubicacion.barrio)
                .dicts()
            )

            # f. Obras finalizadas en 24 meses o menos
            indicadores["obras_24m"] = (
                Obra.select()
                .join(Etapa)
                .where((Etapa.etapa == "Finalizada") & (Obra.plazo_meses <= 24))
                .count()
            )

            # g. Monto total de inversión
            indicadores["monto_total_inversion"] = int(
                Obra.select(fn.SUM(Obra.monto_contrato)).scalar() or 0
            )

            return indicadores

        except Exception as e:
            print(f"[ERROR] obtener_indicadores: {e}")
            return None

        finally:
            try:
                cls.desconectar_db("obtener_indicadores")
            except:
                pass


@classmethod
# Ver los campos únicos de cada tabla
def obtener_campos_unicos(cls, modelo, columna):
    print("[MÉTODO] obtener_campos_unicos")
    # Devuelve los valores únicos de la columna que se le dice
    # Validar que el modelo sea un modelo Peewee
    if not hasattr(modelo, "_meta"):
        raise TypeError(f"[raise] {modelo.__name__} no es un modelo Peewee válido.")

    # Validar que la columna exista
    if columna not in modelo._meta.fields:
        raise ValueError(
            f"[raise] La columna '{columna}' no existe en el modelo {modelo.__name__}."
        )

    campo = modelo._meta.fields[columna]

    # SELECT DISTINCT columna. UNIQUE de pandas
    consulta = modelo.select(campo).distinct().tuples()

    # Valor es (3,) valor[0] es 3
    rtado = [valor[0] for valor in consulta]
    print(rtado)
    return rtado


# Creacion de estructura y carga de datos
"""
GestionarObra.extraer_datos()
GestionarObra.limpiar_datos()
GestionarObra.mapear_orm()
GestionarObra.cargar_datos(GestionarObra.df_limpio)
"""

# Cargar una nueva obra
# GestionarObra.nueva_obra()


# Ver los campos únicos de cada tabla

# GestionarObra.obtener_campos_unicos(Etapa, "etapa")
# GestionarObra.obtener_campos_unicos(AreaResponsable, "area_responsable")
# GestionarObra.obtener_campos_unicos(Ubicacion, "direccion")
# GestionarObra.obtener_campos_unicos(Contratacion, "contratacion_tipo")
# GestionarObra.obtener_campos_unicos(Obra, "monto_contrato")


# Probar flujo

# obra = Obra.get_by_id(1)
# obra.nuevo_proyecto("Rescindida")
# obra.iniciar_contratacion()
# obra.adjudicar_obra("Empresa SA", "30-12345678-9")
# obra.iniciar_obra(date(2025, 1, 3), date(2025, 12, 20))
# obra.actualizar_porcentaje_avance(40)
# obra.incrementar_plazo(2)
# obra.finalizar_obra()

# Menú
if __name__ == "__main__":

    print("🔵  Inicializando base de datos...")
GestionarObra.conectar_db("Inicio")
GestionarObra.extraer_datos()
GestionarObra.mapear_orm()
GestionarObra.limpiar_datos()  # Genera df_limpio interno
GestionarObra.cargar_datos(df_limpio=GestionarObra.df_limpio)

while True:
    print("\n===== Observatorio de Obras Urbanas =====")
    print("1. Crear nueva obra")
    print("2. Avanzar etapas de una obra existente")
    print("3. Mostrar indicadores")
    print("4. Ver los valores únicos de una tabla")
    print("5. Salir")
    opcion = input("Seleccione una opción: ").strip()

    match opcion:
        case "1":
            cantidad_obras = 0
            while True:
                obra = GestionarObra.nueva_obra()

                if obra:
                    cantidad_obras += 1
                    print(f"Obra '{obra.nombre}' creada correctamente.")

                if cantidad_obras >= 2:
                    salir = input("¿Desea cargar otra obra? (s/n): ").lower()
                    if salir == "n":
                        break
                else:
                    print("Debe cargar al menos 2 obras antes de salir.")

        case "2":
            try:
                obra_id = int(input("\nIngrese el ID de la obra: "))
                obra = Obra.get_by_id(obra_id)
            except Exception:
                print("ID inválido o la obra no existe.")
                continue

            print(f"\nAvanzando etapas para la obra: {obra.nombre}")

            # Etapa 1
            obra.nuevo_proyecto()

            # Etapa 2
            obra.iniciar_contratacion()

            # Etapa 3
            obra.adjudicar_obra()

            # Etapa 4
            obra.iniciar_obra()

            # Etapa 5
            obra.actualizar_porcentaje_avance()

            # Opcionales
            while True:
                opcionales = (
                    input("\n¿Incrementar plazo de meses y mano de obra? (s/n)")
                    .strip()
                    .lower()
                )

                if opcionales == "s":
                    obra.incrementar_plazo()
                    obra.incrementar_mano_obra()
                    break
                elif opcionales == "n":
                    break

            # Final o rescesion
            while True:
                opcion_final = (
                    input("\n¿Finalizar (F) o Rescindir (R) la obra? ").strip().lower()
                )

                if opcion_final == "f":
                    obra.finalizar_obra()
                    print("La obra ha sido FINALIZADA.")
                    break
                elif opcion_final == "r":
                    obra.rescindir_obra()
                    print("La obra ha sido RESCINDIDA.")
                    break
                else:
                    print("Opción inválida, intente nuevamente.")

        case "3":
            indicadores = GestionarObra.obtener_indicadores()

            print("\n📊 ===== INDICADORES =====\n")

            for key, value in indicadores.items():
                print(f"🔹 {key.upper()}:")
                print(f"   {value}\n")

        case "4":
            print("\nModelos disponibles:")
            print("Etapa, AreaResponsable, Ubicacion, Contratacion, TipoObra, Obra")

            modelo_nombre = input("Ingrese el nombre del modelo: ").strip()
            columna = input("Ingrese el nombre de la columna: ").strip()

            modelos = {
                "Etapa": Etapa,
                "AreaResponsable": AreaResponsable,
                "Ubicacion": Ubicacion,
                "Contratacion": Contratacion,
                "TipoObra": TipoObra,
                "Obra": Obra,
            }

            if modelo_nombre in modelos:
                GestionarObra.obtener_campos_unicos(
                    modelo=modelos[modelo_nombre], columna=columna
                )
            else:
                print("Modelo inválido.")

        case "5":
            print("Cerrando sistema...")
            if not sqlite_db.is_closed():
                sqlite_db.close()
            break

        case _:
            print("Opción inválida. Intente nuevamente.")
