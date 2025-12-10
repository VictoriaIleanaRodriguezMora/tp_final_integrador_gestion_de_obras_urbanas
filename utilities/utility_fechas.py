from datetime import datetime

def  pedir_fecha(texto=""):
    print("[METODO UTILITARIO] - pedir_fecha")
    while True:
        # Sí no es un valor válido, entra al except, hasta que lo sea.
        fecha = input(texto).strip()

        try:
            # Cuando es válido, sale de la ejecución con return
            return datetime.strptime(fecha, "%d/%m/%Y").date()

        except ValueError:
            print("🔄️ Usd ingresó un valor inválido, porfavor ingrese nuevamente. Formato correcto: DD/MM/YYYY. ")
