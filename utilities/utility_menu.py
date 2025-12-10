def menu_opciones(
    GestionarObra, Obra, AreaResponsable, Contratacion, Etapa, TipoObra, Ubicacion, sqlite_db
):
    while True:
        print("\n===== 🔬 Observatorio de Obras Urbanas ⚙️  =====")
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
                            input("\n¿Finalizar (F) o Rescindir (R) la obra? ")
                            .strip()
                            .lower()
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

                except Exception as e:
                    print("[ERROR] - Opción 2", e)
                    continue

                print(f"\nAvanzando etapas para la obra: {obra.nombre}")

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
