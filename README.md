# NoSQL_Spring2023_Final_Project

<p align="center">
  <img width="600" height="600" src="https://lh5.googleusercontent.com/xpZ0uNADaHiN-ik-tBrPoZOo5ZDjGu1smmrN_4ZTSsKOJsSO-RTQJ8WmzO5cMbz9ofGb8n00PuOUxBUY534mRYlOV2JiIK2ig1JpUi76w5e0zviP4at-QxBD2EEALZc8EaI893T33hudidcqXg9f6g">
</p>




# Problema a solucionar

## Objectivo

Muestrar el entendimiento y capacidad de manejo de las diferentes bases de datos que fueron vistas en el semestre, así como los conceptos relacionados con API’s, ETL’s, etc.

## Planteamiento

Mediante alguna API, de interes para los integrantes del equipo, conectarla, através de python, con una base de datos en MongoDB. Posteriormente, se tiene que hacer un ETL que cargue la base de datos procesada una base de datos estilo grafo, es decir, en Neo4j. Evidentemente, las transformaciones y los subconjuntos de datos ocupados serán diferentes para cada base de datos ya que tienen fines diferentes cada una.

## Entregables

El proyecto debe ser lo más reproducible posible. Por lo cual, se debe de entregar un repositorio completo en github, con los scripts de carga y un Readme.md a manera de instructivo de cómo usar las utilerías implementadas. Además, se requieren al menos 3 queries interesantes, con respecto a cada base de datos (6 en total), que expliquen un poco más el fenómeno del cual la base de datos, está representando.




# Implementación

## Inserción a MongoDB

Para la inserción de todos los caracteres del mundo de Harry Potter, conectamos con la API [PotterDB](https://potterdb.com/) a través del script de python ['Potter'](link aqui). Por medio de la libreria requests, hacemos llamados a la API, antes mencionada, y absorvemos la informacion localmente. Una vez que hemos logrado obtener todos los documentos de tipo 'json' de la PotterDB API, son mandados a una base de datos no relacional a MongoDB bajo el nombre de 'characters'.

## Extract - Transform - Load ( ETL )

