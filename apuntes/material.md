### Python
- https://www.w3sch
- https://www.w3schools.com/python/python_datetime.asp
- https://www.w3schools.com/python/ref_dictionary_items.asp

### Pewee
- https://docs.peewee-orm.com/en/latest/
- https://foro.recursospython.com/Thread-peewee-IntegrityError-NOT-NULL-constraint-failed-person-name?pid=1391
- https://www.tutorialspoint.com/peewee/peewee_constraints.htm
- https://docs.peewee-orm.com/en/latest/peewee/models.html
- https://docs.peewee-orm.com/en/latest/peewee/example.html
- https://www.paradigmadigital.com/dev/como-hacer-bases-datos-con-peewee/
Querying
- https://docs.peewee-orm.com/en/latest/peewee/querying.html
- https://docs.peewee-orm.com/en/3.0.0/peewee/querying.html#creating-a-new-record
- https://docs.peewee-orm.com/en/3.0.0/peewee/api.html#Model.get_or_none

### Pandas
- https://pandas.pydata.org/docs/reference/general_functions.html
- https://www.w3schools.com/python/pandas/ref_df_iterrows.asp
- https://www.geeksforgeeks.org/python/python-pandas-series-str-strip-lstrip-and-rstrip/
- https://www.geeksforgeeks.org/python/capitalize-first-letter-of-a-column-in-pandas-dataframe/
- https://www.geeksforgeeks.org/pandas/pandas-dataframe-iterrows/
- 
### SQLite
- 

### Formatear código python en vscode
- https://www.freecodecamp.org/espanol/news/como-autoformatear-tu-codigo-python-con-black/
- Extensión: https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter

### Paso a paso para instalar *Pip* 
- https://phoenixnap.com/kb/install-pip-windows

### Import de variables desde un archivo a otro con el FROM 
- https://es.stackoverflow.com/questions/164861/import-de-variables-desde-un-archivo-a-otro-con-el-from

### Visualizador de SQLite
- https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer


### Variables de entorno
- https://dev.to/asjordi/como-utilizar-variables-de-entorno-en-python-4pk0

### Instalaciones
## Instalar pip

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
## Instalar pewee
https://docs.peewee-orm.com/en/latest/peewee/installation.html
https://pypi.org/project/peewee/
https://www.geeksforgeeks.org/installation-guide/how-to-install-peewee-python-library-on-windows
```bash
pip install peewee
```

## Alternativa
```bash
python -m pip install peewee
```

## Instalar dotenv
```bash
pip install python-dotenv
```