df.drop_duplicates()

✔️ Quita duplicados solo si TODA la fila es igual
❌ No quita duplicados en columnas específicas

df.drop_duplicates(subset=["direccion"])
✔️ Quita duplicados solo por esa columna. Independientemente de las demás columnas