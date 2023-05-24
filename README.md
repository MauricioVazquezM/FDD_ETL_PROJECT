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
10. Se instancian las casas, generos y blood status de los personajes faltantes. Esto con el fin de poder visualizar y poder especializar los queries en Neo4j y MongoDB. En este mismo paso
11. Se instancian los csv para su posterior insercion en Neo4j.


### Insercion a Neo4j

Correr los siguientes comandos en la terminal de Neo4j para la insercion de los documentos:

#### Carga de los csv

Carga de house csv:
```cypher
load csv with headers from "https://raw.githubusercontent.com/MauricioVazquezM/NoSQL_Spring2023_Final_Project/main/DATA/houses_ids.csv" as row
fieldterminator '\t'
create (n: Houses)
set n = row
```

Carga de genero csv:
```cypher
load csv with headers from "https://raw.githubusercontent.com/MauricioVazquezM/NoSQL_Spring2023_Final_Project/main/DATA/gender_ids.csv" as row
fieldterminator '\t'
create (n: Genres)
set n = row
```

Carga de especie csv:
```cypher
load csv with headers from "https://raw.githubusercontent.com/MauricioVazquezM/NoSQL_Spring2023_Final_Project/main/DATA/species_ids.csv" as row
fieldterminator "\t"
create (n: Species)
set n = row
```

Carga de blood status csv:
```cypher
load csv with headers from "https://raw.githubusercontent.com/MauricioVazquezM/NoSQL_Spring2023_Final_Project/main/DATA/bs_ids.csv" as row
fieldterminator "\t"
create (n: Blood_status)
set n = row
```

Carga de characters csv:
```cypher
load csv with headers from "https://raw.githubusercontent.com/MauricioVazquezM/NoSQL_Spring2023_Final_Project/main/DATA/characters.csv" as row
fieldterminator "\t"
create (c:Characters)
set n = row
```

#### Haciendo las relaciones

Correr los siguientes comandos en la terminal de Neo4j para el establecimiento de las relaciones del grafo:

Insercion de la relacion de characters con sus respectivas casas:
```cypher
match (c:Characters), (h: Houses)
where c.idhouses = h.idcasas
create (c)-[:BELONGS_TO]->(h)
```

Insercion de la relacion de characters con su blood status:
```cypher
match (c:Characters), (b: Blood_status)
where c.idsangre = b.idsangre
create (c)-[:HAS_BLOOD_STATUS_OF]->(b)
```

Insercion de la relacion de characters con su genero:
```cypher
match (c:Characters), (g:Genres)
where c.idgender = g.idgen
create (c)-[:IS]->(g)
```

Insercion de la relacion de characters con su especie:
```cypher
match (c:Characters), (s:Species)
where c.idspecies=s.idsp
create (c)-[:IS_A]->(s)
```

</br>

## Queries

### Queries a MongoDB

Query que obtiene las alturas de todos los personajes que sean hombres humanos o las mujeres elfas. Ademas, ordena descendientemente:
```javascript
db.char.aggregate([
  {
    $match: {
      $or: [
        { "attributes.species": "Human", "attributes.gender": "Male" },
        { "attributes.species": "Elf", "attributes.gender": "Female" }
      ],
      "attributes.height": { $exists: true }
    }
  },
  {
    $project: {
      _id: 0,
      name: "$attributes.name",
      species: "$attributes.species",
      gender: "$attributes.gender",
      height: "$attributes.height"
    }
  },
  {
    $sort: { height: -1 }
  }
])
```

Query para obtener cuantos elfos de casa hay por nacionalidad:
```javascript
db.char.aggregate([
  {
    $match: {
      "attributes.nationality": { $exists: true, $ne: "" },
      "attributes.species": { $ne: "House-elf" }
    }
  },
  {
    $group: {
      _id: "$attributes.nationality",
      characterCount: { $sum: 1 }
    }
  },
  {
    $sort: { characterCount: -1 }
  }
])
```

Query que cuenta los humanos que asistieron a Howarts y luego por su color de ojos los agrupa con su correspodiente contador:
```javascript
db.char.aggregate([
  {
    $match: {
      "attributes.eye_color": { $exists: true, $ne: "" },
      "attributes.species": "Human",
      "attributes.house": { $in: ["Ravenclaw", "Slytherin", "Hufflepuff", "Gryffindor"] }
    }
  },
  {
    $group: {
      _id: "$attributes.eye_color",
      characterCount: { $sum: 1 }
    }
  },
  {
    $sort: { characterCount: -1 }
  }
])
```


### Queries a Neo4j

Query que cuenta por casas cuantos miembros tiene cada casa:
```cypher
match (c:Characters)-[:BELONGS_TO]->(h:Houses)
return c.house as house, count(c.house) as house_count
order by house;
```

Query que cuenta, por cada casa, los humanos que tiene ojos azules:
```cypher
match (c: Characters)-[:BELONGS_TO]->(h:Houses), (c)-[:IS_A]->(s:Species)
where c.eye_color = "blue" and s.especie = "human"
return c.name as charactername, c.eye_color as eyeColor, h.casas as houseName, s.especie as speciesName
```
Query que cuenta por casa los humanos que siguen vivos y los ordena de manera ascendente:
```cypher
match (c:Characters)-[:BELONGS_TO]->(h:Houses), (c:Characters)-[:IS_A]->(s:Species)
where c.died <> "missing" and s.especie = "human"
return c.house as casa, count(c.house) as house_count
order by house_count
```

</br>

## Instrucciones

Para la ejecucion del proyecto se tiene que seguir las siguientes instrucciones:

1. Correr el script ['Potter'](CODE/Potter.ipynb) para la extraccion, transformacion y carga de los datos en MongoDB.
2. Abrir terminal de Neo4j y correr los comandos de insercion en Neo4j de los csv [Carga de los csv](#carga-de-los-csv). Posteriormente, insertar las relaciones del grafo de la seccion [Haciendo las relaciones](#haciendo-las-relaciones).
3. Si se quiere, correr los queries propuestos en [Queries](#queries) para mas informacion sobre la API. Se tiene 3 queries para MongoDB y 3 queries para Neo4j.

