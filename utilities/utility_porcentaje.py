def pedir_porcentaje(self):
    print("[METODO UTILITARIO] - pedir_porcentaje")
    while True:
        try:
            # Sí no es un valor válido, entra al except, hasta que lo sea.
            nuevo_porcentaje = input("Ingrese nuevo porcentaje (0 a 100): ").strip()
            nuevo_porcentaje = int(
                input("🔄️ Porfavor ingrese un porcentaje válido (0 a 100): ").strip()
            )

            return nuevo_porcentaje

        except ValueError:
            print(
                "🔄️ Usd ignresó un valor inválido, porfavor ingrese un número entre 0 y 100."
            )
            return False
