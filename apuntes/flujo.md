1. Cargar el archivo .csv
2. Hacer la limpieza
3. Crear las tablas
4. Cargar las tablas
5. Método para manipular el dataset

## 🟡 PENDIENTE

- No existe la comuna cero. Tratar eso.
- Deberiamos verificar cuantos tipos distintos de datos hay
- Unificar mensaje de error
  Métodos de una obra existente
- Cuando ingresas un `tipo de contratacion` no existente, no te pide que ignreses uno válido. ⬅️ Y adjudica igualmente la obra.
- ¿Desea cambiar la empresa adjudicataria? (S) Sí, (N) No h ----> se le pone una opcion que no es y no dice
  No se modifica el nombre de la empresa
  o no te pide que ingreses S o N
- Si en fecha inicio se pone 34 o en mes, 13 no lo toma, mejorar el mensaje de error

## ERRORES DETECTADOS

- (NO DEBE PEDIRLO) Al modificar datos de una obra existente, `el cuit`, debe existir en la bdd o puede ser uno nuevo?

- Si se ingresa fecha inválida: [ERROR] Formato de fecha inválido. . y no permite ingresar un dato denuevo
  [ERROR] Formato de fecha inválido. time data 'f' does not match format '%d/%m/%Y'
- Si se ingresa porcentaje no válido [ERROR] Debe ingresar un número entre 0 y 100. y no permite ingresar un dato denuevo
- (SI no quiero ninguna? que me deje no finalizar ni rescindir) ¿Finalizar (F) o Rescindir (R) la obra?

## ✨ AMBICIOSOS

- permitirle un prompt para que diga si quiere ver los tipos de contratacion existentes, y mostrarselos.
- A futuro, ver de agregar mensajes particulares para el evento KeyboardInterrupt. Que no te permita cerrar en medio de un proceso de carga o actualizacion

## ✅ SOLUCIONADOS

- Error al cargar_datos NOT NULL constraint failed: Etapa.etapa

- Error al cargar_datos type object 'TipoObra' has no attribute 'nombre'
- Error al cargar_datos NOT NULL constraint failed: TipoObra.tipo_obra

- Error al cargar_datos type object 'AreaResponsable' has no attribute 'nombre'
- Error al cargar_datos NOT NULL constraint failed: AreaResponsable.area_responsable

- Error al cargar_datos type object 'Ubicacion' has no attribute 'direccion'
- Error al cargar_datos type object 'Contratacion' has no attribute 'contratacion_tipo'
- Error al cargar_datos UNIQUE constraint failed: Contratacion.nro_contratacion
- Encontrar la manera para permitir el menú, sin tener que correr la ejecución Creacion, limpieza, carga. Si ya estan cargados, llamar solo al menú
- Debe pedir el número de expediente? Sí, por seguridad
- Crear lógica y manejo, para que al correr el archivo gestionar_obras. el codigo sepa si ya se crearon las bdd o no. puede ser una consulta peewee o sqlite, o guardar el dato en un archivo, y consultarlo de ahí.
- Si no se ingresa una empresa adjudicataria, dice [CAMPO INVÁLIDO] La empresa no puede quedar vacía. y no permite ingresar un dato denuevo
- Se controla globalmente el keyboard interrumpt
- Desea modificar el nombre de la empresa adjudicataria?
  --> Sí: Modificar y guardar
  --> No: Nada
- Limpiar y reacomodar las utilidades de utility_fechas.py
  | Campo | Valor |
  | ---------------------- | ---------------------------------------------------------------------------- |
  | Entorno | Plan 54 escuelas |
  | Nombre | Escuela de Educación Primaria N.° 24 D.E. 15 "Francisco Morazán" - Siglo XXI |
  | Etapa | Finalizada |
  | Tipo de obra | Escuelas |
  | Área responsable | Ministerio de Educación |
  | Descripción | Primaria |
  | Monto del contrato | $67.065.700,00 |
  | Comuna | 12 |
  | Barrio | Villa Urquiza |
  | Dirección | RIVERA, PEDRO I., DR. 4221 |
  | Fecha de inicio | 1/12/2013 |
  | Fecha de finalización | 31/5/2016 |
  | Plazo en meses | 29 |
  | Porcentaje de avance | 100 |
  | Empresa | Criba S.A. |
  | Año de licitación | 2013 |
  | Tipo de contratación | Licitación Pública |
  | Número de contratación | 2030-MDUGC-2013 |
  | CUIT contratista | 30505454436 |
  | Mano de obra | 0 |
  | Obra destacada | SI |
  | Número de expediente | 914412-MDUGC-2013 |
  | Financiamiento | Desconocido |
