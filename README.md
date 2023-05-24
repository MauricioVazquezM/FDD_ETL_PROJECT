# NoSQL_Spring2023_Final_Project

<p align="center">
  <img width="800" height="300" src="https://static.vecteezy.com/system/resources/previews/020/118/322/original/harrypotter-logo-free-download-free-vector.jpg">
</p>

</br>

## Equipo

- [Mariana Luna Rocha](https://github.com/MarianaMoons), estudiante de la Licencitura en Ciencia de Datos en el ITAM.
- [Carlos Elías Rivera Mercado](https://github.com/Carlos-Elias-Riv), estudiante de la Licencitura en Ciencia de Datos en el ITAM.
- [Mauricio Vázquez Moran](https://github.com/MauricioVazquezM), estudiante de la Licencitura en Ciencia de Datos y la Licenciatura en Actuaría en el ITAM.
  


</br>

## Problema a solucionar

### Objectivo

Muestrar el entendimiento y capacidad de manejo de las diferentes bases de datos que fueron vistas en el semestre, así como los conceptos relacionados con API’s, ETL’s, etc.

### Planteamiento

Mediante alguna API, de interes para los integrantes del equipo, conectarla, através de python, con una base de datos en MongoDB. Posteriormente, se tiene que hacer un ETL que cargue la base de datos procesada una base de datos estilo grafo, es decir, en Neo4j. Evidentemente, las transformaciones y los subconjuntos de datos ocupados serán diferentes para cada base de datos ya que tienen fines diferentes cada una.

### Entregables

El proyecto debe ser lo más reproducible posible. Por lo cual, se debe de entregar un repositorio completo en github, con los scripts de carga y un Readme.md a manera de instructivo de cómo usar las utilerías implementadas. Además, se requieren al menos 3 queries interesantes, con respecto a cada base de datos (6 en total), que expliquen un poco más el fenómeno del cual la base de datos, está representando.



</br>

## Implementacion

### Insercion a MongoDB

Para la inserción de todos los caracteres del mundo de Harry Potter, conectamos con la API [PotterDB](https://potterdb.com/) a través del script de python ['Potter'](CODE/Potter.ipynb). Por medio de la libreria 'requests', hacemos llamados a la API, antes mencionada, y absorvemos la informacion localmente. Una vez que hemos logrado obtener todos los documentos de tipo 'json' de la PotterDB API, son mandados a una base de datos no relacional a MongoDB bajo el nombre de 'characters'.

### Extract - Transform - Load ( ETL )

Para la extraccion, transformacion y carga de los datos obtenidos de la API, se siguieron los siguientes pasos en la limpieza de datos:

1. Se extraen los datos apoyandonos en la libreria 'request'. Por medio de sencillas iteraciones, iteramos sobre las diferentes paginas de la API extrayendo los documentos tipos 'json'. Obtenemos como total 4066 documentos, correspondientes a los personajes de la saga Harry Potter.
2. Hacemos una primera importacion a MongoDB, bajo el nombre de la coleccion 'characters' en la base de datos 'potter'.
3. Apoyandonos de un pipeline desde python hacia MongoDB, limpiamos los id de los personajes para no tener problemas en la posterioridad del ETL.
4. Habiendo mandado los documentos a MongoDB, absorbemos los archivos 'json' en python y verificamos que esten correctos los id.
5. Por medio de la libreria 'pandas', mandamos los documentos a un dataframe para simplificar y agilizar su transformacion.
6. Revisamos las columnas del dataframe y soltamos las columnas que no nos son de utilidad. En otras palabras, dropeamos los metadatos que venian con los documentos desde la API.
7. Limpiamos los nombres de nuestras variables, es decir, los nombres de nuestras columnas. En este mismo paso, revisamos los tipos de datos que tenemos en las diferentes variables para su transformacion en el correcto data type.
8. Revisamos los na's que contiene el dataframe. Utilizamos la estrategia de sustituir los na's por el valor de 'missing'. Bajo este mismo paso y con miras de hacer una base de tipo grafo en Neo4j, sustituimos los na's, en algunas variables, por valores provenientes de otros caracteres y, de esta manera, poder crear los grafos para su posterior carga en Neo4j.
9. Con la utilizacion de una funcion auxiliar, retiramos los caracteres no desados de las cadenas de texto. Asimismo, normalizamos las cadenas de string para que en la posteriedad el analisis de esta base de datos sea con mayor facilidad. 


### Insercion a Neo4j

#### Carga de los csv
Carga de house csv:
```cypher

```

Carga de genero csv:
```cypher

```

Carga de especie csv:
```cypher

```

Carga de blood status csv:
```cypher

```

#### Haciendo las relaciones

Insercion house:
```cypher

```

Insercion genero:
```cypher

```

Insercion especie:
```cypher

```

Insercion blood status:
```cypher

```

</br>

## Queries

### Queries a MongoDB

Explicacion del query1 aqui:
```javascript

```

Explicacion del query2 aqui:
```javascript

```

Explicacion del query3 aqui:
```javascript

```


### Queries a Neo4j

Explicacion del query1 aqui:
```cypher

```

Explicacion del query2 aqui:
```cypher

```

Explicacion del query3 aqui:
```cypher

```

</br>

## Instrucciones


