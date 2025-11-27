1. Cargar el archivo .csv
2. Hacer la limpieza
3. Crear las tablas
4. Cargar las tablas
5. Método para manipular el dataset

PENDIENTE:
🟡 No existe la comuna cero. Tratar eso.
🟡 Deberiamos verificar cuantos tipos distintos de datos hay
🟡 Unificar mensaje de error
Métodos de una obra existente
🟡 Cuando ingresas un `tipo de contratacion` no existente, no te pide que ignreses uno válido. ⬅️ Y adjudica igualmente la obra.
✨ Más ambicioso y a futuro, permitirle un prompt para que diga si quiere ver los tipos de contratacion existentes, y mostrarselos.  
❌ (NO DEBE PEDIRLO) Al modificar datos de una obra existente, `el cuit`, debe existir en la bdd o puede ser uno nuevo?
✅ Encontrar la manera para permitir el menú, sin tener que correr la ejecución Creacion, limpieza, carga. Si ya estan cargados, llamar solo al menú
❓ Debe pedir el número de expediente? 

ERRORES
✅Error al cargar_datos NOT NULL constraint failed: Etapa.etapa

✅Error al cargar_datos type object 'TipoObra' has no attribute 'nombre'
✅Error al cargar_datos NOT NULL constraint failed: TipoObra.tipo_obra

✅Error al cargar_datos type object 'AreaResponsable' has no attribute 'nombre'
✅Error al cargar_datos NOT NULL constraint failed: AreaResponsable.area_responsable

✅Error al cargar_datos type object 'Ubicacion' has no attribute 'direccion'
✅Error al cargar_datos type object 'Contratacion' has no attribute 'contratacion_tipo'
✅Error al cargar_datos UNIQUE constraint failed: Contratacion.nro_contratacion

| Campo                  | Valor                                                                        |
| ---------------------- | ---------------------------------------------------------------------------- |
| Entorno                | Plan 54 escuelas                                                             |
| Nombre                 | Escuela de Educación Primaria N.° 24 D.E. 15 "Francisco Morazán" - Siglo XXI |
| Etapa                  | Finalizada                                                                   |
| Tipo de obra           | Escuelas                                                                     |
| Área responsable       | Ministerio de Educación                                                      |
| Descripción            | Primaria                                                                     |
| Monto del contrato     | $67.065.700,00                                                               |
| Comuna                 | 12                                                                           |
| Barrio                 | Villa Urquiza                                                                |
| Dirección              | RIVERA, PEDRO I., DR. 4221                                                   |
| Fecha de inicio        | 1/12/2013                                                                    |
| Fecha de finalización  | 31/5/2016                                                                    |
| Plazo en meses         | 29                                                                           |
| Porcentaje de avance   | 100                                                                          |
| Empresa                | Criba S.A.                                                                   |
| Año de licitación      | 2013                                                                         |
| Tipo de contratación   | Licitación Pública                                                           |
| Número de contratación | 2030-MDUGC-2013                                                              |
| CUIT contratista       | 30505454436                                                                  |
| Mano de obra           | 0                                                                            |
| Obra destacada         | SI                                                                           |
| Número de expediente   | 914412-MDUGC-2013                                                            |
| Financiamiento         | Desconocido                                                                  |
