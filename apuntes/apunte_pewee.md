# create_tables -> método de pewee
db.create_tables([Clase])

> [!WARNING] Los nombres de tablas no pueden tener espacios
> Al intentar crear la bd con los nombres de tablas asi: 
> `db_table = "Area responsable"`, da el error: **sqlite3 result code 26: file is not a database python**


> [!WARNING] Peewee espera un objeto, NO una tupla, cuando se lo usa como FK.
> get_or_create() devuelve una tupla, pero estamos pasando la tupla completa como foreign key
```py
etapa = Etapa.get_or_create(...)
# Devuelve 🔽
# (<Etapa: 1>, True)
```