@classmethod
def obtener_indicadores(cls):
    print("In --- Indicadores de Obras Urbanas --- ")
    try:
        # a. Listado de todas las áreas responsables
        print("a. Áreas Responsables:")
        for ar in AreaResponsable.select().order_by(AreaResponsable.nombre):
            print(f"- {ar.nombre}")

        # b. Listado de todos los tipos de obra
        print("\nb. Tipos de Obra:")
        for to in TipoObra.select().order_by(TipoObra.nombre):
            print(f"- {to.nombre}")

        # c. Cantidad de obras por etapa
        print("\nc. Cantidad de obras por Etapa:")
        etapas_count = (Obra
                        .select(Etapa.nombre, fn.COUNT(Obra.id).alias('count'))
                        .join(Etapa)
                        .group_by(Etapa.nombre)
                        .order_by(Etapa.nombre))
        for ec in etapas_count:
            print(f"- {ec.etapa.nombre}: {ec.count} obras")

        # d. Cantidad de obras y monto total por tipo de obra
        print("\nd. Obras y Monto de Inversión por Tipo de Obra:")
        tipo_obra_stats = (Obra
                           .select(TipoObra.nombre,
                                   fn.COUNT(Obra.id).alias('count'),
                                   fn.SUM(Obra.monto_inversion).alias('total_inversion'))
                           .join(TipoObra)
                           .group_by(TipoObra.nombre)
                           .order_by(TipoObra.nombre))
        for tos in tipo_obra_stats:
            print(f"- {tos.tipo_obra.nombre}: {tos.count} obras, Inversión Total: ${tos.total_inversion:,.2f}")

        # e. Barrios en comunas 1, 2 y 3
        print("\ne. Barrios en Comunas 1, 2 y 3:")
        barrios_comunas = Barrio.select().where(Barrio.comuna.in_([1, 2, 3])).order_by(Barrio.nombre)
        for bc in barrios_comunas:
            print(f"- {bc.nombre} (Comuna {bc.comuna})")

        # f. Obras finalizadas en <= 24 meses
        print("\nf. Obras finalizadas en <= 24 meses:")
        try:
            etapa_finalizada = Etapa.get(Etapa.nombre == "Finalizada")
            obras_finalizadas_24m = Obra.select().where(
                (Obra.etapa == etapa_finalizada) &
                (Obra.plazo_meses <= 24)
            ).count()
            print(f"- Cantidad: {obras_finalizadas_24m} obras")
        except Etapa.DoesNotExist:
            print("- La etapa 'Finalizada' no existe en la base de datos.")

        # g. Monto total de inversión
        print("\ng. Monto Total de Inversión:")
        total_inversion = Obra.select(fn.SUM(Obra.monto_inversion)).scalar()
        print(f"- Monto Total: ${total_inversion:,.2f}" if total_inversion else "- Monto Total: $0.00")

    except Exception as e:
        print(f"Error al obtener indicadores: {e}")
