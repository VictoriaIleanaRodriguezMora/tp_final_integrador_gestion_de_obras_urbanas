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

#### 3. Modelo ORM Pewee
- Crear módulo `modelo_orm.py` que contenga:
  - Definición de clases y atributos necesarios, siguiendo el modelo *ORM de Pewee*, para poder persistir los datos importados del dataset en una base de datos relacional de tipo SQLite `obras_urbanas.db`
  - Aquí se debe incluir  además la clase `BaseModel` heredando de `peewee.Model`
- https://docs.peewee-orm.com/en/latest/peewee/models.html
- https://www.paradigmadigital.com/dev/como-hacer-bases-datos-con-peewee/
- https://haseeb987.medium.com/best-python-orms-sqlalchemy-sqlalchemy-peewee-ponyorm-cd81b5b2d28c
- https://youtu.be/ej-PPefJwFY?si=vqQvN_AB3N_4C1lx
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

#### 5. Clase Obra,  es una de las clases que debe formar parte del modelo ORM, debe incluir  los siguientes métodos de instancia con el objetivo de definir las diferentes etapas de avance  de obra: 
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

### Flujo de Trabajo - Especificaciones para la Gestión de Obras
#### 6.  Se deberán crear nuevas instancias de Obra (dos instancias como mínimo) 
- invocando al  método de clase `GestionarObra.nueva_obra()`. 

7. Cada una de las nuevas obras deben pasar por todas las etapas definidas, salvo `incrementar_plazo()` e `incrementar_mano_obra()` que son opcionales. Para ello se debe invocar a los métodos de instancia de la clase Obra, siguiendo el orden de la declaración de las etapas (desde `nuevo_proyecto()` hasta `finalizar_obra()` ó `rescindir_obra()`). Luego de cada cambio de estado del objeto Obra producto de una nueva etapa de avance de la obra, se deben persistir los nuevos valores usando el método `save()`.

8. Para iniciar un nuevo proyecto de obra se debe invocar al método `nuevo_proyecto()`. Aquí la etapa inicial de las nuevas instancias de Obra debe tener el valor “Proyecto” (si este valor no existe en la tabla “etapas” de la BD, se deberá crear la instancia y luego insertar el nuevo registro). Los valores de los atributos `tipo_obra`, `area_responsable` y `barrio` deben ser alguno de los existentes en la base de datos.

9. A continuación, se debe iniciar la licitación/contratación de la obra, para ello se debe invocar al método `iniciar_contratacion()`, asignando el `TipoContratacion` (debe ser un valor existente en la BD) y el `nro_contratacion`.

10. Para adjudicar la obra a una empresa, se debe invocar al método `adjudicar_obra()` y asignarle la `Empresa` (debe ser una empresa existente en la BD) y el `nro_expediente`.

11. Para indicar el inicio de la obra, se debe invocar al método `iniciar_obra()`, y asignarle valores a los siguientes atributos: `destacada`, `fecha_inicio`, `fecha_fin_inicial`, `fuente_financiamiento` (debe ser un valor existente en la BD) y `mano_obra`.

12. Para registrar avances de la obra, se debe invocar al método `actualizar_porcentaje_avance()` y actualizar el valor del atributo `porcentaje_avance`.

13. Para incrementar el plazo de la obra, se debe invocar al método `incrementar_plazo()` y actualizar el valor del atributo `plazo_meses`. (Esta acción es opcional, pero el método debe estar definido).

14. Para incrementar la cantidad de mano de obra, se debe invocar al método `incrementar_mano_obra()` y actualizar el valor del atributo `mano_obra`. (Esta acción es opcional, pero el método debe estar definido).

15. Para indicar la finalización de una obra, se debe invocar al método `finalizar_obra()` y actualizar el valor del atributo etapa a “Finalizada” y del atributo `porcentaje_avance` a “100”.

16. Para indicar la rescisión de una obra, se debe invocar al método `rescindir_obra()` y actualizar el valor del atributo etapa a “Rescindida”.

17. Para finalizar la ejecución del programa, se debe invocar al método de clase `GestionarObra.obtener_indicadores()` para obtener y mostrar por consola la siguiente información:  
    a. Listado de todas las áreas responsables.  
    b. Listado de todos los tipos de obra.  
    c. Cantidad de obras que se encuentran en cada etapa.  
    d. Cantidad de obras y monto total de inversión por tipo de obra.  
    e. Listado de todos los barrios pertenecientes a las comunas 1, 2 y 3.  
    f. Cantidad de obras finalizadas en un plazo menor o igual a 24 meses.  
    g. Monto total de inversión.
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


## Instalaciones
### Instalar pip

https://pip.pypa.io/en/stable/installation/
https://www.geeksforgeeks.org/installation-guide/how-to-install-pip-on-windows/
1) Descargar PIP
- https://bootstrap.pypa.io/get-pip.py -> guárdalo en el mismo directorio donde está instalado Python
2) Para saber donde tengo instalado python
```bash
where python
```
3) Cambie la ruta actual del directorio en la línea de comandos a la ruta del directorio donde se encuentra el archivo mencionado anteriormente.
4) Ejecutar el comando para instalar Python
```bash
python get-pip.py
```
4) Ejecutar el comando para ver donde se instaló Pip
```bash
where pip
```
5) Agregar esa ruta de PIP a las variables de entorno de Windows. 
- Variables de entorno > Click en boton 'Variables de entorno' > Doble click en donde dice 'PATH' > Click en 'Nuevo' > Pegar la ruta de pip
- 
### Instalar pewee
https://docs.peewee-orm.com/en/latest/peewee/installation.html
https://pypi.org/project/peewee/
https://www.geeksforgeeks.org/installation-guide/how-to-install-peewee-python-library-on-windows
```bash
pip install peewee
```

### ALternativa
```bash
python -m pip install peewee
```

### Import de variables desde un archivo a otro con el FROM
- https://es.stackoverflow.com/questions/164861/import-de-variables-desde-un-archivo-a-otro-con-el-from