1) Cargar el archivo .csv
2) Hacer la limpieza
3) Crear las tablas
4) Cargar las tablas
5) Método para manipular el dataset

PENDIENTE: 
🟡 No existe la comuna cero. Tratar eso.
🟡 Deberiamos verificar cuantos tipos distintos de datos hay


ERRORES
🟡Error al cargar_datos NOT NULL constraint failed: Etapa.etapa

✅Error al cargar_datos type object 'TipoObra' has no attribute 'nombre'
🟡Error al cargar_datos NOT NULL constraint failed: TipoObra.tipo_obra

✅Error al cargar_datos type object 'AreaResponsable' has no attribute 'nombre'
🟡Error al cargar_datos NOT NULL constraint failed: AreaResponsable.area_responsable

✅Error al cargar_datos type object 'Ubicacion' has no attribute 'direccion'
✅Error al cargar_datos type object 'Contratacion' has no attribute 'contratacion_tipo'
✅Error al cargar_datos UNIQUE constraint failed: Contratacion.nro_contratacion