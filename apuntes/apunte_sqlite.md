# Base de datos SQLite

`SQLite` es una biblioteca de C que provee una base de datos ligera basada en disco que no requiere un proceso de servidor separado y permite acceder a la base de datos usando una variación no estándar del lenguaje de consulta` SQL`.

Algunas aplicaciones pueden usar `SQLite` para almacenamiento interno. 

--> En algunos momentos de prueba, de testeo, se suele usar `SQLite` para hacer pruebas y antes de PRD se pasa a un motor de bdd. 

También es posible prototipar una aplicación usando `SQLite` y luego transferir el código a una base de datos más grande como PostgreSQL u Oracle.

> [!NOTE]
No llega a ser un motor de base de datos (como `SQL server`), porque es ligera. Es un archivo que tiene la forma de una bdd normalizada, **no** se ejecuta como servicio ni servidor.

## Descargar gestor de `SQLite` https://sqlitebrowser.org/

## Usar el módulo `sqlite3` de Python y crear una conexión

> [!NOTE]
>
> Un módulo es un archivo.py que puede contener desde cosas muy simples, hasta muy complejas. Desde Clases, funciones; estas, dependiendo de su complejidad y su nivel puede formar una bdd como SQLite

1) **importar** la librería de Python llamada sqlite3.
2) **crear** un **objeto Connection** que representa la base de datos.
```py
import sqlite3
bdd = sqlite3.connect("example.bd") # Este es el nombre del archivo al que se va a conectar
print("Base de datos abierta")
```
> [!TIP]
> La ruta que recibe connect puede ser absoluta o relativa
>
> Se pueden especificar modos de acceso; Lectura, escritura

### Crear una tabla en la base de datos
Una vez que se tenga una `Connection`, se puede crear un `objeto Cursor` y llamar su `método execute()` para ejecutar **`comandos SQL`**.

✨Podemos crear tablas directamente desde python.

```py
cursor = bdd.cursor()
# Crear una tabla
cursor.execute('''CREATE TABLE stocks
                  (date text, trans text, symbol text, qty real, price real)''')
```

### Insertar datos en una tabla
> [!WARNING]
> Cada vez que insertemos, modifiquemos o eliminemos un registro en una tabla **es necesario hacer un commit**. 
>
> Es decir, “guardar” nuestros cambios a la base de datos.
>
> Si no hacemos esto, los movimientos no se registrarán.

```py
# Insertar un registro
cursor.execute('''INSERT INTO stocks VALUES ('2025-08-11', 'BUY', 'RHAT', 100, 35.14)''')

# Guardar los cambios
bdd.commit()

# Cerrar la conexión a la bdd
# Hay que asegurarse que los cambios se hayan aplicado o se perderán

bdd.close()
```

### Seleccionar **un** registro de una tabla

Usualmente, las operaciones SQL necesitarán usar valores de variables de Python.

Para ello se deben usar los `parámetros de sustitución DB-API`. 

Es decir, colocar `'?'` como un marcador de posición en el lugar donde se usara un valor, y luego se provee una `tupla de valores` como segundo argumento del método del `cursor execute()`.

```py
t = ("RHAT",)
# Donde dice ?, se reemplaza por t
cursor.execute('SELECT * FROM stocks WHERE symbols = ?', t)
print(cursor.fetchone())
```

El método `fetchone` trae la primer coincidencia


### Seleccionar registros de una tabla
Para obtener los datos luego de ejecutar una sentencia `SELECT`, se puede tratar el `cursor` como un `iterator`,  llamar `fetchall()` para obtener una lista de todos los registros.

```py
for row in cursor.execute('SELECT * FROM stocks ORDER BY price'):
    print(row)
# OUTPUT
('2025-08-11', 'BUY', 'RHAT', 100.0, 35.14)
```

### Eliminar datos de una tabla
```py
symbol = 'SONY'
sentencia = 'DELETE FROM stocks WHERE symbol = ?;'

# Eliminar el registro
# El ? se reemplaza por [symbol]
cursor.execute(sentencia, [symbol])
bdd.commit()
print("Eliminado con éxito")
```

### Actualizar datos en una tabla
```py
qty = 1500
price = 85.00
symbol = 'MSFT'

sentencia = 'UPDATE stocks SET qty = ?, price = ? WHERE symbol = ?;'

# Actualizar el registro
# Cada ? se reemplaza por [qty, price, symbol] en el orden que aparece
cursor.execute(sentencia, [qty, price, symbol])
bdd.commit()
print("Datos guardados")
```

## Conectarse a una base de datos MySQL

Si quiero conectarme a cualquier otro motor, tengo que encontrar el módulo o la librería que me va a permitir manipularlo.

Existen muchos modulos para un motor de bdd.

Cuando un **`módulo es externo`** a la liberia python, lo tengo que **`instalar con pip`**:

```bash
pip install PyMySQL
```

Luego de instalado, puedo importarlo y usarlo.
```py
import pymysql

try:
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        db='example'
    )
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    print(cursor.fetchall())
    db.close()

except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
    print("Ocurrió un error al conectar: ", e)
```