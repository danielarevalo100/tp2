# tp2
# Espacio para escribir nuestras hipotesis

# Santiago Bianucci
#Creacion de Carpetas:
Investigue sobre la libreria OS, empece obteniendo la direccion base donde se desarrola el trabajo,
para luego comenzar a desarrollar el tp.
Una vez obtenida la direccion base, empece a abrir los archivos csv de los respectivos asuntos.(docentes,alumnos,docentes_alumnos)
Con estas funciones obtuve las listas con el contenido de esos archivos.
Cree en primer lugar la carpeta de la evaluacion con os.mkdir y luego abri ciclos for con las listas obtenidas de los .csv para crear
en primer lugar la carpeta de los docentes con os.mkdir y metiendome en la carpeta de la evaluacion con os.path.join.
Luego cree la de los alumnos comparando si el primer elemento de la lista de docentes-alumnos era igual al primero de la lista de docentes
y por ultimo si el segundo elemento de la lista de docentes-alumnos era igual al primero de alumnos para crear la carpeta de los alumnos 
separados por lo docentes correspondientes de nuevo utlizando os.path.join para meterme dentro de la carpeta del respectivo docente. 
A la carpeta de alumnos le agregue en el nombre el segundo elemento de la lista de alumnos que es el padron para diferenciar en caso
de que haya nombres repetidos entre los alumnos

# Mateo Lardiez
A mi me toco hacer la parte de google drive con la API. Tuve muchos problemas al principio para poder conectar configurar la API (a travez de service_drive.py) y tambien me costo interpretar la documentacion. Lo que hice fue lo siguiente:
Crear archivos/carpetas en el drive:
Para crear un archivo en el drive, le doy la opcion al usuario que elija que tipo de archivo quiere subir y lo subo a la carpeta principial del drive. Para crear carpetas le doy la opcion al usuario que elija la cantidad de carpetas que quiere subir.
Recorrer el drive:
En este punto me ayudo Daniel ya que lo tenia mal hecho. Usamos recursividad cada ves que encuentra un archivo que sea una carpeta. Esto lo sabemos a travez de su mimetype.
Subir archivos:
Le digo al usuario que ponga todos los archivos que quiere subir a la carpeta 'Archivos_a_subir' y luego subo los que se encuentran en esa carpeta al drive. Finalmente limpio la carpeta para un nuevo uso
Descargar archivo:
Le muestro todos los arhivos podibles al usuario a travez de la funcion recrrer el drive, y el usuario elije el archivo que quiere descargar a travez de su id. Tambien le doy la opcion al usuario que le cambie el nombre antes de descargarlo.
Sincronizacion: 
Genero 2 diccionarios (la funcion diccionarios_archivos), uno con los nombres de los archivos locales como claves y su fecha de ultima modificacion como valor; y otro con los nombres de los archivos remotos con una lista de datos que uso mas adelante, como valores. Luego le dejo la posibilidad al usuario que haga una lista con los archivos que se encuentran a nivel local, que no quiera subir al remoto(ej el archivo client_secret,json).Recorro los archivos locales y si veo que el mismo se encuentra en remoto llamo a la funcion comparar fechas. Si la ultima fecha de modificacion del archivo local es mayor que la del archivo remoto, sube el archivo local a remoto; si pasa lo contrario, borra el archivo local y descarga el archivo remoto. Si un archivo local no se encuentra en el google drive lo sube. Luego veo si un archivo si un archivo remoto no esta en local, si sucede esto lo descargo al local.

# Diego Lavia
me toco hacer la parte de carpetas, para la funcion crear_carpeta_local() busque informacion sobre las funciones de la
libreria os.path, entre ellas use isfile, join (ambas tambien usadas para listas el directorio), isdir. 
tambien utilice el os.remove para archivos y os.rmdir para carpetas. y funciones de la libreria
time para la ultima modificacion de un archivo en local, como localtime, datetime y stat

# Daniel Arevalo
Fue un proyecto bastante retador ya que manejamos temas un poco avanzados, requirio leer bastante la documentacion vaga que ofrece google pero al final logramos terminarlo, en mi caso, estaba acargo de todo lo relacionado con Gmail, enviar correos, buscoar correos, descargar archivos adjuntos y descomprimir.
Para esto me enfoque en hacer mas que todo utilidades ya que no era algo complejo y esto requeria usarse en varios lugares del programa, todo lo relacionado con esto lo hice dentro del archivo 'gmailUtils.py' el que incluye enviar mail, buscar un mail por ID y buscar un mail con una query.

Para que nuestro programa funcione, se debe ingresar las credenciales descargadas de la consola de google y nombrarlas como client_secret.json, igualmente que los archivos relacionados con la conexion a las APIs seran service_gmail y service_drive respectivamente.
