# Métodos utilitarios para obras

from datetime import *
from modelo_orm import Ubicacion
from peewee import fn
from modelo_orm import Contratacion


# Pide al usuario un valor, valida que exista en la base, y devuelve el objeto Peewee correspondiente.
def utility_nueva_obra(Model, column_name, input_label):
    campo = Model._meta.fields[column_name]  # Obtiene el campo Peewee

    while True:
        valor = input(f"Ingrese {input_label}: ").strip()

        # Consulta dinámica -> field == valor
        query = Model.get_or_none(campo == valor)

        if query:
            return query

        print(f"{input_label} no encontrado. Intente nuevamente.")


# Pide múltiples valores al usuario y devuelve el objeto si existe.
def utility_nueva_obra_multi(Model, campos):
    # `campos` debe ser un dict:
    # {"nombre_campo_peewee": "Texto a mostrar al usuario"}
    while True:
        filtros = {}
        # .items devuelve un array de tuplas [('brand', 'Ford'), ('model', 'Mustang')
        for campo, texto in campos.items():
            # print("campo ", campo)
            # print("texto ", texto)
            valor_user = input(f"Ingrese {texto}: ").strip()
            filtros[campo] = valor_user  # filtros[nro_contratacion] = valor_user
            """
            filtros = {
                nro_contratacion : 'valor_user'
            }
            """

        try:
            """
            los ** son un desempaquetador de diccionarios
            {"nro_contratacion": 'valor_user', "b": 2}
            nro_contratacion=valor_user', b=2
            """
            # nro_contratacion=valor_user' es lo que le llega a get_or_none
            obj = Model.get_or_none(
                **filtros
            )  # Trae la fila donde todos los campos coinciden
            if obj:
                return obj

            print("No se encontró un registro con esos datos. Intente nuevamente.\n")

        except Exception as e:
            print(f"[ERROR] Validando datos: {e}")
            return None

# Validador de enteros. Se usa para pedir, monto contrato, mano de obra, etc
def pedir_int(texto):
    while True:
        valor = input(texto).strip()
        if valor.isdigit():
            return int(valor)
        print("Debe ingresar un número entero válido.")

# Validador de string no vacío. Se utiliza para pra pedir nombre empresa, etc
def pedir_str(texto):
    while True:
        valor = input(texto).strip()
        if valor != "":
            return valor
        print("El valor no puede estar vacío.")

# Validador de fecha DD/MM/YYYY
def pedir_fecha(texto):
    while True:
        valor = input(texto).strip()
        try:
            return datetime.strptime(valor, "%d/%m/%Y").date()
        except ValueError:
            print("Formato incorrecto. Debe ser DD/MM/YYYY.")

# Genera un número de contratación automático con el formato 'N/YYYY', donde N es un contador incremental por año.
def generar_nro_contratacion() -> str:
    # Ej: '1/2025' '2/2025'
    # El cálculo se basa en buscar la contratación más reciente del año actual.
    anio_actual = datetime.now().year

    # Buscar el último nro_contratacion del año actual
    ultimo = (
        Contratacion.select()
        .where(Contratacion.nro_contratacion.contains(f"/{anio_actual}"))
        .order_by(Contratacion.id.desc())
        .first()
    )

    # Calcular el próximo número
    if ultimo:
        try:
            ultimo_num = int(ultimo.nro_contratacion.split("/")[0])
        except ValueError:
            # Si por algún motivo no cumple el formato, comenzamos desde 1
            ultimo_num = 0
        nuevo_num = ultimo_num + 1
    else:
        nuevo_num = 1

    return f"{nuevo_num}/{anio_actual}"

# Si la ubicación ingresada NO existe en la bdd, la crea. Si no, la reutiliza. 
def obtener_o_crear_ubicacion():
    """
    Loop de ingreso de comuna, barrio y dirección.
    - Repite la carga si comuna NO existe.
    - Repite la carga si barrio NO existe.
    - Si la combinación completa existe → la devuelve.
    - Si no existe → la crea.
    No se sale hasta que devuelva una Ubicación válida.
    """
    while True:
        try:
            comuna = input("Ingrese la comuna: ").strip()
            barrio = input("Ingrese el barrio: ").strip()
            direccion = input("Ingrese la dirección: ").strip()

            # Validación de comuna
            existe_comuna = Ubicacion.select().where(Ubicacion.comuna == comuna).first()

            if not existe_comuna:
                print("❌ La comuna ingresada no existe. Intente nuevamente.\n")
                continue  # vuelve a pedir todo

            # Validación de barrio
            existe_barrio = Ubicacion.select().where(Ubicacion.barrio == barrio).first()

            if not existe_barrio:
                print("❌ El barrio ingresado no existe. Intente nuevamente.\n")
                continue  # vuelve a pedir todo

            # Buscar ubicación completa
            ubicacion = (
                Ubicacion.select()
                .where(
                    (Ubicacion.comuna == comuna)
                    & (Ubicacion.barrio == barrio)
                    & (Ubicacion.direccion == direccion)
                )
                .first()
            )

            if ubicacion:
                print("✔ Se encontró una ubicación existente.\n")
                return ubicacion

            # Crear nueva ubicación
            nueva = Ubicacion.create(comuna=comuna, barrio=barrio, direccion=direccion)
            print("✔ Ubicación nueva creada.\n")
            return nueva

        except Exception as e:
            print(f"[ERROR] obtener_o_crear_ubicacion - {e}")
            print("Intentemos nuevamente...\n")
