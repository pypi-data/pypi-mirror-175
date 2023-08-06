# Grizzlies   Parseador de un archivo csv a json, y de un archivo json a csv.
# ¿Qué es Grizzlies?
Es una librería capaz de leer archivos tanto en formato **csv** como **json**, además de convertirlos a **csv** o **json** y guardarlos en un directorio especificado por el usuario.
# ¿Qué aporta la librería grizzlies?
* Ser capaz de leer archivos **csv** por el delimitador que se le indique.
* Detección automatica del tipo de archivo introducido.
* Dependiendo del tipo de archivo introducido, sabe a que lo debe convertir y como guardarlo.
* Sencilla utilización. El usuario solo debe llamar a la clase y añadir el método que desea realizar.
# Código fuente y cómo instalarlo.
El repositorio github donde se encuentra el código fuente es el siguiente:
https://github.com/JonJarrinVitoria/Grizzlies.git .

Para instalar la libreria grizzlies: 
https://pypi.org/project/grizzlies/.
```
pip install grizzlies
```
# ¿Cómo funciona grizzlies?
## Ejemplo de configuración y utilización con un archivo csv:

Para el primer paso, se importara la librería y se configurara.
```
 import grizzlies as gz
 conversor = gz.grizzlies()
```
Se procede a leer el arhivo **csv**. En este caso, al ser un archivo **csv**, se debe introducir el nombre del archivo y el delimitador en caso de ser diferente a ";".
```
  conversor.leer('./MiDirectorio/archivo.csv', delimitador=',')
```
En el siguiente paso, se convierte el archivo **csv** a tipo **json**. En este caso, no hace falta que se introduzca nada, ya que coge la información del paso anterior, y sabe identificar que tipo de archivo es, y por ende, a cual debe convertirlo:
```
  conversor.convertir()
```
Finalmente, para poder guardar el arhivo, se le debe indicar el directorio donde se quiere guardar, el nombre con el que se quiere guardar, junto con la extensión a la cual se ha convertido:
```
  conversor.guardar('./MiDirectorio/archivo.json')
```
# Dependencias
* [flatten_json - poner que hace esta libreria]().
  - [pip install flatten_json](https://pypi.org/project/flatten-json/).
# Licencia
Este proyecto se encuentra bajo los terminos de la licencia **MIT** - más información sobre los detalles en [LICENSE.txt]('LICENSE.txt').
