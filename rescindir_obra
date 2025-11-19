def rescindir_obra(self):
    try:
        etapa_rescindida, created = Etapa.get_or_create(nombre="Rescindida")
        self.etapa = etapa_rescindida
        self.save()
        print(f"Obra '{self.nombre}' rescindida.")
        return True
    except Exception as e:
        print(f"Error al rescindir obra '{self.nombre}': {e}")
        return False
