# README

### Alumno: Contrera Cristian.

## Desarrollo

El programa se fue implementando con ejemplos y tutoriales mayormente sacados de los enlaces proporcionados por la catedra, la utilizacion del framework flask, facilita y organiza mucho el desarrollo de un proyecto, pero creo que este limita la forma del mismo ya que se deben respetar ciertas estructuras planteadas por la herramienta.

## Estructura

Se utilizaron solo los archivos que la catedra proporciono, dividiendo el programa en:

#### Auth:
Este archivo realiza el trabajo de loguear a un usuario con la información brindada por las api de github y google, para esta tarea nos basamos en los ejemplos descargados de (https://github.com/lepture/flask-oauthlib/tree/master/example)
donde ademas se guarda a los usuarios en una base de datos, que antes comprueba que el usuario no este registrado con anterioridad.

#### Runserver:
Este archivo maneja todo lo referido la ejecución de las partes de la pagina, como loguearse, agregar/eliminar/mostrar feed. 
La complicación con esta parte fue la funcion new_feed ya que hay feed que no disponen de descripcion en sus datos, esto lo solucionamos, verificando si esta descripción existía en un bloque try.. catch.. cuando creamos los feed que guardara cada usuario.

#### App:
Este archivo solo realiza, la inicialización de la app, la base de datos, el login manager y la proteccion contra CSRF para ser todo importado en runserver.

## Decisiones de diseño

* Un mismo usuario se puede loguear con las diferentes api's, para obtener varias cuentas.
* En caso de que una api no proporcione los datos pedidos para el logueo de un usuario, como "nombre", se lo reemplaza por otros datos que tengamos.
* Se agrego en el ID de cada usuario una inicial que identifica con que api se logueo, para solucionar el caso de que dos api's distintas nos dieran el mismo id para dos usuarios distintos.
* Se utilizó una libreria además de las propuestas por la catedra "flask_wtf", la cual se debe descargar con:

        pip install flask_wtf

esta se utiliza para la proteccion contra CSRF.

## Uso del programa

El programa se corre ejecutando desde la carpeta que poseen los archivos:

        python runserver.py

y accediendo desde un navegados a: http://localhost:5000.
