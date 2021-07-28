# tp2
# Espacio para escribir nuestras hipotesis


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