from datetime import *


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
            filtros[campo] = valor_user # filtros[nro_contratacion] = valor_user
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
            obj = Model.get_or_none(**filtros) # Trae la fila donde todos los campos coinciden
            if obj:
                return obj

            print("No se encontró un registro con esos datos. Intente nuevamente.\n")

        except Exception as e:
            print(f"[ERROR] Validando datos: {e}")
            return None
        
# Validador de enteros
def pedir_int(texto):
    while True:
        valor = input(texto).strip()
        if valor.isdigit():
            return int(valor)
        print("Debe ingresar un número entero válido.")

# Validador de string no vacío
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
