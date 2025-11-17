# create_tables -> método de pewee
db.create_tables([Clase])

> [!WARNING] Los nombres de tablas no pueden tener espacios
> Al intentar crear la bd con los nombres de tablas asi: 
> `db_table = "Area responsable"`, da el error: **sqlite3 result code 26: file is not a database python**