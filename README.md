# Instituto de Formación Técnica Superior Nro 18

## Carrera: Técnico Superior en Desarrollo de Software
### Trabajo Práctico Final Integrador

**Materia:** Desarrollo de Sistemas Orientados a Objetos  
**Curso:** 1er Año  
**Profesor:** Lic. Eduardo Iberti  
**Ciclo Lectivo:** 2do Cuatrimestre 2025  
**Fecha límite de entrega:** jueves 20 de Noviembre de 2025  

---

### Modalidad de Trabajo
- El trabajo se debe realizar en grupo de cinco alumnos.
- **Nombre de la carpeta del proyecto:** `rodriguez-pobeda-lescano-delossantos-arias`

---

### Tema
Sistema de gestión de obras urbanas del GCBA. Desarrollo con POO, importación de datasets desde un archivo CSV, limpieza y normalización de datos, y persistencia de objetos con ORM Peewee en una base de datos SQLite.

---

### Descripción del Proyecto
Se requiere desarrollar un software en Python para gestionar las obras urbanas de la Ciudad de Buenos Aires, tomando como origen de datos un dataset público del gobierno de la ciudad y haciendo uso de la librería **Peewee**. Para el manejo y operaciones con el dataset se debe utilizar la librería **Pandas**, y para el manejo y operaciones con arrays pueden utilizar la librería **NumPy**.

---

### Requerimientos Técnicos

#### 1. Estructura del Proyecto
- Crear carpeta del proyecto con el formato: `apellido1-apellido2-apellido3-apellido4-apellido5`

#### 2. Datos de Entrada
- Utilizar el archivo CSV: `observatorio-de-obras-urbanas.csv`
- **Fuente de datos:**
  - https://data.buenosaires.gob.ar/dataset/ba-obras
  - https://cdn.buenosaires.gob.ar/datosabiertos/datasets/secretaria-general-y-relaciones-internacionales/ba-obras/observatorio-de-obras-urbanas.csv

#### 3. Modelo ORM
- Crear módulo `modelo_orm.py` que contenga:
  - Definición de clases y atributos necesarios
  - Clase `BaseModel` heredando de `peewee.Model`
  - Persistencia en base de datos SQLite: `obras_urbanas.db`

#### 4. Gestión de Obras
- Crear módulo `gestionar_obras.py` con la clase abstracta `GestionarObra` y los siguientes métodos:

| Método | Descripción |
|--------|-------------|
| `extraer_datos()` | Manipular dataset con DataFrame de Pandas |
| `conectar_db()` | Conexión a la base de datos |
| `mapear_orm()` | Crear estructura de la BD con Peewee |
| `limpiar_datos()` | Limpieza de datos nulos y no accesibles |
| `cargar_datos()` | Persistir datos limpios en la BD |
| `nueva_obra()` | Crear nuevas instancias de Obra |
| `obtener_indicadores()` | Obtener información de obras existentes |

#### 5. Clase Obra - Métodos de Instancia
- `nuevo_proyecto()`
- `iniciar_contratacion()`
- `adjudicar_obra()`
- `iniciar_obra()`
- `actualizar_porcentaje_avance()`
- `incrementar_plazo()` (opcional)
- `incrementar_mano_obra()` (opcional)
- `finalizar_obra()`
- `rescindir_obra()`

---

### Flujo de Trabajo

#### 6-7. Creación y Gestión de Obras
- Crear **mínimo 2 instancias** de Obra usando `GestionarObra.nueva_obra()`
- Cada obra debe pasar por todas las etapas definidas
- Persistir cambios después de cada etapa con `save()`

#### 8-16. Secuencia de Etapas
1. **Proyecto:** `nuevo_proyecto()` - Etapa inicial "Proyecto"
2. **Contratación:** `iniciar_contratacion()` - Asignar tipo y número de contratación
3. **Adjudicación:** `adjudicar_obra()` - Asignar empresa y número de expediente
4. **Inicio:** `iniciar_obra()` - Asignar datos de inicio y financiamiento
5. **Avance:** `actualizar_porcentaje_avance()` - Actualizar porcentaje
6. **Opcionales:** `incrementar_plazo()` y `incrementar_mano_obra()`
7. **Finalización:** `finalizar_obra()` o `rescindir_obra()`

#### 17. Indicadores Finales
- Listado de todas las áreas responsables
- Listado de todos los tipos de obra
- Cantidad de obras en cada etapa
- Cantidad de obras y monto total de inversión por tipo de obra
- Listado de barrios de las comunas 1, 2 y 3
- Cantidad de obras finalizadas en ≤ 24 meses
- Monto total de inversión

---

### Aclaraciones Importantes

1. **Clase GestionarObra:** Todos los métodos deben ser de clase, así como sus atributos.
2. **Manejo de Excepciones:** Incluir código para manejar posibles excepciones.

---

### Recursos y Bibliotecas

#### Pandas
- Biblioteca para manipulación y análisis de datos en Python
- Trabaja con DataFrames (tablas bidimensionales)
- **Recursos:**
  - https://datascientest.com/es/pandas-python
  - https://www.w3schools.com/python/pandas/default.asp
  - https://pypi.org/project/pandas/

#### NumPy
- Librería especializada en cálculo numérico y análisis de datos
- Utiliza arrays para procesamiento eficiente
- **Recursos:**
  - https://aprendeconalf.es/docencia/python/manual/numpy/
  - https://facundoq.github.io/courses/images/res/03_numpy.html
  - https://joserzapata.github.io/courses/python-ciencia-datos/numpy/
  - https://geekflare.com/es/numpy-arrays/

---

### Estructura del Dataset
Información de las obras públicas realizadas en la Ciudad, incluyendo empresas constructoras, fechas, montos, descripción, ubicación y ministerio responsable.

**Documentación completa de la estructura:**
https://data.buenosaires.gob.ar/dataset/ba-obras/resource/b18dc277-ed29-4d2b-a5f5-d8bd10751920
