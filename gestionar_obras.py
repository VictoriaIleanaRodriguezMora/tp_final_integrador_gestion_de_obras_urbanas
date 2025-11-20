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
)


class GestionarObra(ABC):
    df_limpio = []

    # sentencias necesarias para manipular el dataset a través de un objeto Dataframe del módulo “pandas”.
    @classmethod
    def extraer_datos(cls):
        try:
            df = pd.read_csv(CVS_PATH, sep=";", encoding="latin1")
            # print(df)
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
            print(
                "No se ha podido conectar con la base de datos", e
            )  # 🟡 Agregar info del error

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
            print("✨ Los datos se mapearon correctamente mapear_orm")
        except Exception as e:
            print("[ERROR] mapear_orm - Error al cargar_datos", e)
        finally:
            GestionarObra.desconectar_db("mapear_orm")

    # sentencias necesarias para persistir los datos de las obras (ya transformados y “limpios”) que contiene el objeto Dataframe en la base de  datos relacional SQLite. Para ello se debe utilizar el método de clase Model create() en  cada una de las clase del modelo ORM definido.
    @classmethod
    def limpiar_datos(cls):
        print("[MÉTODO] limpiar_datos")
        try:
            df = cls.extraer_datos()
            # print("df obtenido: ", df)

            # 🟢 Normalizar nombres de columnas
            df.columns = (
                df.columns.str.strip()
                .str.lower()
                .str.replace("-", "_")
                .str.replace(" ", "_")
            )

            # Se crea el cls.df_limpio, donde ya usa las columnas normalizadas de df.columns
            cls.df_limpio = (
                df.drop(  # Quita las columnas especificadas
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
                .drop_duplicates()  # Quita filas duplicadas
                .assign(
                    monto_contrato=df["monto_contrato"].str.strip()
                )  # Assign agrega una nueva columna al df
                .fillna(  # Rellena los valores nulos
                    {
                        "expediente_numero": 0,
                        "destacada": "Desconocido",
                        "contratacion_tipo": "Desconocida",
                        "tipo": "Desconocido",
                        "descripcion": "Desconocido",
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

            # 🟢 Normalizar valores de columna 'etapa'
            cls.df_limpio["etapa"] = cls.df_limpio["etapa"].str.capitalize().str.strip()
            cls.df_limpio["etapa"] = cls.df_limpio["etapa"].fillna("Desconocida")
            cls.df_limpio["etapa"] = cls.df_limpio["etapa"].replace("", "Desconocida")
            cls.df_limpio["etapa"] = (
                cls.df_limpio["etapa"].str.strip().replace("", "Desconocida")
            )

            # 🟢 Normalizar valores de columna  'direccion'
            cls.df_limpio["direccion"] = cls.df_limpio["direccion"].str.upper()

            # 🟢 Quitar valores duplicados
            cls.df_limpio = cls.df_limpio.drop_duplicates()

            cls.df_limpio.to_csv(
                "datos_limpios.csv", index=False
            )  # Aca creamos csv con datos limpios.
            # print("df df_limpio: ", df_limpio["monto_contrato"])

            print("✅ Datos limpiados")
            print("✨ Los datos se limpiaron correctamente limpiar_datos")
            return cls.df_limpio
        except Exception as e:
            print("[ERROR] limpiar_datos - Error al limpiar_datos", e)

    # sentencias necesarias para persistir los datos de las obras (ya transformados y “limpios”)
    @classmethod
    def cargar_datos(cls, df_limpio):
        GestionarObra.conectar_db("cargar_datos")
        try:
            print("[MÉTODO] cargar_datos")
            for index, row in df_limpio.iterrows():
                # SÍ ANDA 🔽
                ubicacion_obj, booleano = Ubicacion.get_or_create(
                    comuna=row["comuna"],
                    barrio=row["barrio"],
                    direccion=row["direccion"],
                )

                contratacion_obj, booleano = Contratacion.get_or_create(
                    contratacion_tipo=row["contratacion_tipo"],
                    nro_contratacion=row["nro_contratacion"],
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
            print("✨ Se realizó la carga de datos cargar_datos")
        except Exception as e:
            print("[ERROR] cargar_datos - Error al cargar_datos", e)
        finally:
            GestionarObra.desconectar_db("cargar_datos")

    # sentencias necesarias para obtener información de las obras existentes en la base de datos SQLite a través de sentencias ORM.
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
                    "nro_contratacion": "el número de contratación",
                    "contratacion_tipo": "el tipo de contratación",
                    "cuit_contratista": "el cuit del contratista",
                },
            )

            # Etapa
            nva_etapa = utility_nueva_obra(Etapa, "etapa", "el estado de la etapa")

            # Tipo de obra
            nvo_tipo = utility_nueva_obra(TipoObra, "tipo_obra", "el tipo de obra")

            # Ubicación
            nueva_ubicacion = utility_nueva_obra_multi(
                Ubicacion,
                {
                    "comuna": "la comuna",
                    "barrio": "el barrio",
                    "direccion": "la dirección",
                },
            )

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
    def obtener_indicadores(
        cls,
    ):  # devuelve un dicionario con indicadores basados en las obras almacenadas en la base SQLite usando Peewee ORM
        try:
            cls.conectar_db()  # abre conexion

            indicadores = {}  # se crea diccionario con las consultas ORM Peewee

            # total de obras, cuenta todos los registros en Obra
            indicadores["total_obras"] = Obra.select().count()

            # obras por etapa
            query_etapa = (
                Obra.select(
                    Etapa.etapa.alias("etapa"), fn.COUNT(Obra.id).alias("cantidad")
                )
                .join(
                    Etapa, on=(Obra.etapa_fk == Etapa.id)
                )  # une la tabla Obra con Etapa por la FK
                .group_by(Etapa.etapa)  # agrupa por el nombre de la etapa
            )  # resultado: filas con etapa y cantidad
            indicadores["obras_por_etapa"] = [
                {"etapa": r.etapa, "cantidad": r.cantidad} for r in query_etapa
            ]
            # obras por tipo de obra
            query_tipo = (
                Obra.select(
                    TipoObra.tipo_obra.alias("tipo"),
                    fn.COUNT(Obra.id).alias("cantidad"),
                )
                .join(TipoObra, on=(Obra.tipo_obra_fk == TipoObra.id))
                .group_by(TipoObra.tipo_obra)
            )
            indicadores["obras_por_tipo"] = [
                {"tipo": r.tipo, "cantidad": r.cantidad} for r in query_tipo
            ]
            # obras por comuna
            query_comuna = (
                Obra.select(
                    Ubicacion.comuna.alias("comuna"),
                    fn.COUNT(Obra.id).alias("cantidad"),
                )
                .join(Ubicacion, on=(Obra.ubicacion_fk == Ubicacion.id))
                .group_by(Ubicacion.comuna)
            )
            indicadores["obras_por_comuna"] = [
                {"comuna": r.comuna, "cantidad": r.cantidad} for r in query_comuna
            ]
            # monto total adjudicado
            monto_total = Obra.select(fn.SUM(Obra.monto_contrato)).scalar()
            indicadores["monto_total"] = int(
                monto_total or 0
            )  # suma todos los monto_contrato, .scalar devuelve el valor o None si no hay registros

            # avance promedio
            avance_promedio = Obra.select(fn.AVG(Obra.porcentaje_avance)).scalar()
            indicadores["avance_promedio"] = float(
                avance_promedio or 0
            )  # devuelve promedio

            # obras destacadas
            obras_destacadas = Obra.select().where(Obra.destacada == "SI").count()
            indicadores["obras_destacadas"] = obras_destacadas

            # top 5 barrios con mas obras desde Ubicacion.barrio
            query_barrios = (
                Obra.select(
                    Ubicacion.barrio.alias("barrio"),
                    fn.COUNT(Obra.id).alias("cantidad"),
                )
                .JOIN(Ubicacion, on=(Obra.ubicacion_fk == Ubicacion.id))
                .order_by(fn.COUNT(Obra.id).desc())
                .limit(5)
            )
            indicadores["top5_barrios"] = [
                {"barrio": r.barrio, "cantidad": r.cantidad} for r in query_barrios
            ]

            # obras por area responsable
            query_area = (
                Obra.select(
                    AreaResponsable.area_responsable.alias("area"),
                    fn.COUNT(Obra.id).alias("cantidad"),
                )
                .join(
                    AreaResponsable, on=(Obra.area_responsable_fk == AreaResponsable.id)
                )
                .group_by(AreaResponsable.area_responsable)
            )
            indicadores["obras_por_area"] = [
                {"area": r.area, "cantidad": r.cantidad} for r in query_area
            ]

            # devuelve diccionario
            return indicadores

        except Exception as e:
            print(f"[ERROR] al obtener indicadores: {e}")
            return None

        finally:
            try:
                cls.desconectar_db()
            except Exception:
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

GestionarObra.extraer_datos()
GestionarObra.limpiar_datos()
GestionarObra.mapear_orm()
GestionarObra.cargar_datos(GestionarObra.df_limpio)
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
