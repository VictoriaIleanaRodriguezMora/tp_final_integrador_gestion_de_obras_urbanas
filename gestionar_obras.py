# Crear módulo `gestionar_obras.py` con la clase abstracta `GestionarObra` y los siguientes métodos:
"""
a. extraer_datos(), que debe incluir las sentencias necesarias para manipular el dataset a través de un objeto Dataframe del módulo “pandas”.
b. conectar_db(), que debe incluir las sentencias necesarias para realizar la conexión a la base de datos “obras_urbanas.db”.
c. mapear_orm(), que debe incluir las sentencias necesarias para realizar la creación de la estructura de la base de datos (tablas y relaciones) utilizando el método de instancia “create_tables(list)” del módulo “peewee”.
d. limpiar_datos(), que debe incluir las sentencias necesarias para realizar la “limpieza” de los datos nulos y no accesibles del Dataframe.
e. cargar_datos(), que debe incluir las sentencias necesarias para persistir los datos de las obras (ya transformados y “limpios”) que contiene el objeto Dataframe en la base de  datos relacional SQLite. Para ello se debe utilizar el método de clase Model create() en  cada una de las clase del modelo ORM definido.
f. nueva_obra(), que debe incluir las sentencias necesarias para crear nuevas instancias de Obra. Se deben considerar los siguientes requisitos:
• Todos los valores requeridos para la creación de estas nuevas instancias deben ser ingresados por teclado.
• Para los valores correspondientes a registros de tablas relacionadas (foreign key), el valor ingresado debe buscarse en la tabla correspondiente mediante sentencia de búsqueda ORM, para obtener la instancia relacionada, si el valor ingresado no existe en la tabla, se le debe informar al usuario y solicitarle un nuevo ingreso por teclado.
• Para persistir en la BD los datos de la nueva instancia de Obra debe usarse el método save() de Model del módulo “peewee”.
• Este método debe retornar la nueva instancia de obra.
g. obtener_indicadores(), que debe incluir las sentencias necesarias para obtener información de las obras existentes en la base de datos SQLite a través de sentencias ORM.
"""

"""
1. En la clase abstracta “GestionarObra”, todos sus métodos deben ser métodos de clase y sus atributos (en caso que considere que deba existir alguno) también serán atributos de clase.
2. Incluir código Python para manejar posibles excepciones donde considere conveniente para atrapar aquellas que puedan llegar a generarse.
"""


"""
Los métodos de clase permiten acceder y modificar atributos de clase,
crear nuevas instancias de la clase o manipular la clase en sí.
• Deben contar con el decorador @classmethod.
• Reciben como argumento cls, que hace referencia a la clase.
• Los métodos de clase pueden acceder a la clase pero no a la instancia.
• Sí pueden modificar los atributos de clase.
"""

from abc import ABC
import pandas as pd
from peewee import *
from modelo_orm import *
import sqlite3
from modelo_orm import sqlite_db


class GestionarObra(ABC):

    # sentencias necesarias para manipular el dataset a través de un objeto Dataframe del módulo “pandas”.
    @classmethod
    def extraer_datos(cls):
        try:
            # print('extraer_datos')
            df = pd.read_csv(
                "observatorio-de-obras-urbanas.csv", sep=";", encoding="latin1"
            )
            # print(df)
            return df

        except FileNotFoundError as e:
            print("No se ha encontrado el archivo csv", e)

    #  else:
    #      return df

    # sentencias necesarias para realizar la conexión a la base de datos “obras_urbanas.db”.
    @classmethod
    def conectar_db(cls):
        try:
            sqlite_db.connect()
            print("🔓 Conexión a la BDD abierta en conectar_db()")
        except FileNotFoundError as e:
            print("No se ha podido conectar con la base de datos", e)
        # finally:
        #     sqlite_db.close()
        #     print("🔒 Conexión a la BDD cerrada en conectar_db()")

    @classmethod
    def desconectar_db(cls):
        try:
            db = sqlite_db.close()
            return db

        except FileNotFoundError as e:
            print("No se ha podido cerrar  la base de datos", e)  

    # sentencias necesarias para realizar la creación de la estructura de la base de datos (tablas y relaciones) utilizando el método de instancia “create_tables(list)” del módulo “peewee”.
    @classmethod
    # 🟡 Agregar manejo de errores
    def mapear_orm(cls):
        print("mapear_orm")
        GestionarObra.conectar_db()
        sqlite_db.create_tables(  # db no existe
            [Etapa, TipoObra, AreaResponsable, Ubicacion, Contratacion, Obra]
        )
        GestionarObra.conectar_db()

    # sentencias necesarias para persistir los datos de las obras (ya transformados y “limpios”) que contiene el objeto Dataframe en la base de  datos relacional SQLite. Para ello se debe utilizar el método de clase Model create() en  cada una de las clase del modelo ORM definido.
    # ? No entiendo lo de: utilizar el método de clase Model create() en  cada una de las clase del modelo ORM definido.
    @classmethod
    # 🟡 Agregar manejo de errores
    def limpiar_datos(cls):
        print("limpiar_datos")
        df = cls.extraer_datos()
        print("df obtenido: ", df)
        df_limpio = (
            df.drop(  # Quita las columnas especificadas
                columns=[
                    "lat",
                    "lng",
                    "imagen_1",
                    "imagen_2",
                    "imagen_3",
                    "imagen_4",
                    "beneficiarios",  # Nose si la sacaria
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
                    "expediente-numero": 0,
                    "mano_obra": 0,
                    "destacada": "Desconocido",
                    "contratacion_tipo": "Desconocida",  # No pondría 'no posee', porque un tipo tiene que tener. Es desconocido
                }
            )
        )
        # print("df df_limpio: ", df_limpio)
        print("df df_limpio: ", df_limpio["monto_contrato"])

        return df_limpio

    """sentencias necesarias para crear nuevas instancias de Obra. Se deben considerar los siguientes requisitos:
    • Todos los valores requeridos para la creación de estas nuevas instancias deben ser ingresados por teclado.
    • Para los valores correspondientes a registros de tablas relacionadas (foreign key), el valor ingresado debe buscarse en la tabla correspondiente mediante sentencia de búsqueda ORM, para obtener la instancia relacionada, si el valor ingresado no existe en la tabla, se le debe informar al usuario y solicitarle un nuevo ingreso por teclado.
    • Para persistir en la BD los datos de la nueva instancia de Obra debe usarse el método save() de Model del módulo “peewee”.
    • Este método debe retornar la nueva instancia de obra.
    """

    @classmethod
    # 🟡 Agregar manejo de errores
    def cargar_datos(cls, limpiar_datos):
        pass

    # sentencias necesarias para obtener información de las obras existentes en la base de datos SQLite a través de sentencias ORM.
    @classmethod
    # 🟡 Agregar manejo de errores
    def nueva_obra(self):
        pass


# GestionarObra.extraer_datos()
GestionarObra.limpiar_datos()
GestionarObra.mapear_orm()
