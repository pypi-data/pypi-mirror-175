Esta librería sirve a la hora de comprender y analizar los datos de uno para la realización de un modelo de clasificación binaria. Para ello, detecta aquellas variables que están muy correlacinadas entre sí y elimina una por cada pareja. Además, también se analizan aquellas variables que están fuertemente relacionadas con la variable objetivo.

A continuación se va adjuntar aquellos comandos que se necesitan para su instalación y futuro uso. También, se explican la manera de utilizar la librería y todas sus funciones.

## La instalación
El primer paso consiste en la instalación del paquete:
```sh
pip install libreria-correlaciones==0.7
```
## Llamada del paquete
```sh
from libreria_correlaciones.libreria_correlaciones import deteccion_correlaciones
```
## Instanciar la clase
Para la realización de esta librería, se ha decido crear una clase que recoja 6 funciones. Para ello, lo primero que hay que hacer es indicar cuales son los datos que se quieren analizar.
```sh
archivo = ' ' #añadir el dataset deseado
datos = deteccion_correlaciones(archivo)
```
## Utilización de la librería
Lo primero que realiza esta clase una vez insertado los datos es crear dos variables. Una de ellas llamada "numericas" que hace referencia a todas las variables númericas existentes en el dataset. La otra, "variables_corr_para_modelar", indica todas aquellas variables que no sean la variable objetivo. Es decir, quita la variable clase del dataset.

La primera función elimina aquellas variables para modelar que estén más correlacionadas.
```sh
datos.eliminacion_variables_correlacionadas()
```
Después, la siguiente función coge las variables numéricas y analiza cuales tienen más relación con la variable objetivo.
```sh
data = datos.variables_mas_importantes()
```
Una vez habiendo asignado el resultado de esta función a una variable, se puede ejecutar la función que te permite visualizar los histogramas de estas variables.
```sh
datos.histogramas(data)
```
Finalmente, se pueden visualizar los resultados del filtrado a través de mapas de calor.
```sh
datos.correlaciones_a_eliminar()
```
```sh
datos.correlaciones_variables_importantes()
```
