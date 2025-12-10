def pedir_porcentaje(self):
    print("[METODO UTILITARIO] - pedir_porcentaje")

    try:
        nuevo_porcentaje = (input("Ingrese nuevo porcentaje (0 a 100): ").strip())
        while type(nuevo_porcentaje)  is not int: 
                    nuevo_porcentaje = int(input("🔄️ Porfavor ingrese un porcentaje válido (0 a 100): ").strip())
        
        return True
    
    except ValueError:
        print("[ERROR] [METODO UTILITARIO] Debe ingresar un número entre 0 y 100.")
        return False
