def iniciar_contratacion(self, tipo_contratacion_nombre, nro_contratacion):
    try:
        # Asignar número de contratación
        self.nro_contratacion = nro_contratacion

        # Etapa: Contratación
        etapa_contratacion, _ = Etapa.get_or_create(nombre="Contratacion")
        self.etapa = etapa_contratacion

        # Persistir cambios
        self.save()
        print(f"Obra '{self.nombre}' en etapa de 'Contratación'. Nro Contratación: {self.nro_contratacion}")
        return True
    except Exception as e:
        print(f"Error al iniciar contratación para obra '{self.nombre}': {e}")
        return False
