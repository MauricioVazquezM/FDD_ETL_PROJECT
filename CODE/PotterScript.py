'''
Librerias por utilizar.
'''
import requests
import json
import pymongo
import random
from bson import ObjectId
import pandas as pd
import numpy as np




'''
En esta parte del codigo, se hacen los request a la API. De igual manera,
se van insertando los documentos en MongoDB, por medio de la liberia pymongo.
'''
for i in range(41):
    url = "https://api.potterdb.com/v1/characters?page[number]="+str(i+1)

    # Haciendo request a la API
    response = requests.get(url)
    # print(response.text)

    # Revisando el status de la request
    if response.status_code == 200:
        # Pasando la respuesta a un json
        data = response.json()

        # Guardando la informacion en un archivo del tipo json
        with open("hp_data.json", "w") as file:
            json.dump(data, file)
            print("Data downloaded and saved successfully.")
    else:
        print("Failed to retrieve data from the API. Status code:", response.status_code)
        print("Error message:", response.text)


    # Configurando un cliente y una base de datos MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['potter']

    # Insertando los documentos en la coleccion 
    my_collection = db['characters']
    my_data = [data]
    insert_result = my_collection.insert_many(my_data)
# # Print the data
# print(data)


'''
Se instaura un pipile, con el fin de restaurar los ids de los documentos.
Esto debido a que dado la estructura del json, proveniente de la API, 
la insercion inicial en MongoDB duplica los ids 
'''
seed = 1234

pipeline = [
    {"$unwind": "$data"},
    {"$set": {"_id": "$data.id"+str(random.randint)}},
    {"$out": "char"}
]
db.characters.aggregate(pipeline)


'''
Pipiline auxiliar de ordenacion en MongoDB.
'''
pipeline2 = [
    {
        '$replaceWith': {
            '$mergeObjects': ['$data', '$$ROOT']
        }
    },
    {
        '$unset': 'data'
    }
]

db.char.update_many({}, pipeline2)


'''
Cambio de id por la duplicacion al momento de la insercion.
'''
db.char.update_many({}, {'$unset': {'data.id': 1}})


'''
Ayudandonos de MongoDB para poder meter los documentos en un dataframe.
De esta manera, podremos manejar de manera mas secuencial y sencilla la transformacion.
'''
# Clase de codificador JSON personalizado para manejar la serialización de ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

# Conectando con MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['potter']
collection = db['char']

# Obtener los documentos de la colección.
documents = collection.find()

# Conviertiendo los documentos en diccionarios
documents_list = [doc for doc in documents]

# Guardando en json
with open('exported_data.json', 'w') as file:
    json.dump(documents_list, file, indent=4, cls=JSONEncoder)


'''
Preparando la data para, por medio de pandas, insertarla en un dataframe.
'''
# Abriendo el archivo JSON
f = open('exported_data.json')

# devuelve el objeto JSON como
# un diccionario
data = json.load(f)

# Cerrando el documento
f.close()
# data


'''
Al utilizar la funcion de 'json_normalize' de la libreria pandas, 
metemos los archivos JSON a un dataframe para su transformacion.
'''
df = pd.json_normalize(data)

# Tirando las columnas que no nos seran de utilidad.
new_df = df.drop(['_id','meta.pagination.current', 'meta.pagination.next',
       'meta.pagination.last', 'meta.pagination.records', 'meta.copyright',
       'meta.generated_at', 'links.self', 'links.current', 'links.next',
       'links.last', 'meta.pagination.first', 'meta.pagination.prev',
       'links.first', 'links.prev','attributes.image',
       'attributes.wiki','attributes.height', 'attributes.weight'],axis = 1)

# Cambiamos el nombre de las columnas, eliminando 'attribute.'
columnas = new_df.columns.tolist()
new_columnas = [name.split(".")[1] if len(name.split(".")) > 1 else name for name in columnas]
new_df.columns = new_columnas

# Revisando los valos na de las variables o columnas.
suma = new_df.isna().sum()
#print(suma)

# Convirtiendo los data type a unos de mayor agilidad para mamipular como lo
# es una cadena de string
char = new_df.convert_dtypes()
#print("Nuevos tipos:")
#print(char.dtypes)

'''
Seleccionandole casa aleatoria, con el fin de crear posteriormente, un mejor grafo en Neo4j.
'''
seed = 1234

# new_df['house'].unique()

lista = ['Ravenclaw', 'Gryffindor', 'Slytherin', 'Hufflepuff',
       'Thunderbird', 'Did not attend Hogwarts', 'Horned Serpent',
       'Hogwarts School of Witchcraft and Wizardry', 'Pukwudgie',
       'Wampus']


'''
Funcion auxiliar de ponerle casa a los caracteres que no tengan
'''
def ponerCasa(cell):
        if cell is None or cell is pd.NA or cell == 'Unknown':
            # print("Entre a este caso")
            var = random.choice(lista) 
            print(var)
            return var
        else:
            return cell

char['house'] = char['house'].apply(ponerCasa)
#char


# Diccionario auxiliar para la siguiente funcion
dict_aux = {'Gryffindor': ['Gryffindor', 'Gryffindor (likely)', 
'Gryffindor (possibly)', 'Gryffindor or Slytherin', 
'Gryffindor, Hufflepuff or Ravenclaw', 'Gryffindor, Hufflepuff,  or Slytherin', 
'Gryffindor, Hufflepuff, or Ravenclaw', 'Gryffindor, Hufflepuff, or Slytherin', 'Pub landlady'], 'Did not attend Hogwarts': [None], 
'Hogwarts School of Witchcraft and Wizardry': [None], 'Horned Serpent': ['Horned Serpent'], 'Hufflepuff': ['Hufflepuff', 'Hufflepuff (likely)', 
'Hufflepuff (possibly)', 'Hufflepuff or Ravenclaw', 'Hufflepuff or Slytherin', 'Hufflepuff, Ravenclaw or Slytherin'], 
'Pukwudgie': ['Pukwudgie'], 'Ravenclaw': ['Ravenclaw', 'Ravenclaw (likely)', 'Ravenclaw (possibly)', 
'Ravenclaw or Hufflepuff', 'Ravenclaw or Slytherin', 'Ravenclaw, Slytherin or Hufflepuff'], 'Slytherin': ['Slytherin', 
'Slytherin (likely)', 'Slytherin (most likely)', 'Slytherin (possibly)'], 'Thunderbird': ['Thunderbird'], 'Wampus': ['Wampus'], 'Unknown': [None]}


'''
Funcion auxiliar para limpiar la variable de house. Esto con el fin de simplificar las
relaciones que se estableceran en el grafo de Neo4j.
'''
def mantenerCasas(cell):
    for elem in dict_aux: 
        if cell is not None or cell is not np.nan: 
            # print("Entre a este caso")
            if cell == elem: 
                return elem
            if cell in dict_aux[elem]:
                return elem

        else: 
            return None


# Aplicando la funcion para limpir la variable house
aux = char['house'].apply(mantenerCasas)


'''
Sustituyendo los valores na's. Se utilizo una estrategia de sustituir
los na's por 'missing'. 
'''
char.fillna("missing", inplace=True)


char = char.apply(lambda x: x.astype(str).str.lower())


'''
Funcion auxiliar que nos ayudara a quitar lo caracteres especiales. 
'''
def quitar(cell):
    cell = cell.astype(str)
    resp = cell.replace(to_replace=r'[\!\#\$\%\&\(\)\'\"\*\+\-\.\/\:\;\<\=\>\?\@\^\`\{\|\}\~\†]', value=' ', regex=True)
    return resp

char = char.apply(quitar)


'''
En esta parte del codigo nos apoyamos para asignarle un id a las
casas con el fin de crear csv intermedio para el posterior grafo en Neo4j. 
'''
lista = ['ravenclaw', 'gryffindor', 'slytherin', 'hufflepuff',
       'thunderbird', 'did not attend hogwarts', 'horned serpent',
       'hogwarts school of witchcraft and wizardry', 'pukwudgie',
       'wampus']
idscasas = ['r', 'g', 's', 'h', 't', 'd', 'hs', 'h', 'p', 'w']
intermediario = {'casas': lista, 'idcasas': idscasas}

inter = pd.DataFrame(intermediario)


dict_casas= {'gryffindor': 'g', 'hufflepuff': 'h', 'ravenclaw': 'r', 'slytherin': 's',
             'thunderbird': 't', 'wampus': 'w', 'pukwudgie': 'p',  'horned serpent':'hs', 
             'hogwarts school of witchcraft and wizardry': 'h', 'did not attend hogwarts' : 'd'}

char['idhouses'] = char['house'].map(dict_casas)


'''
En esta parte del codigo nos apoyamos para asignarle un id a los
generos con el fin de crear csv intermedio para el posterior grafo en Neo4j. 
'''
lista2 = ['missing', 'female', 'male', 'male  most likely ',
       'males, females', 'male, female', 'males', 'male  likely ',
       'females', 'four males, one female', 'unknown',
       'males and females', 'female, male',
       'male  as depicted in the tales of beedle the bard ',
       'male  possibly ', 'male  father , female  mother ',
       'female  likely ', '3 males, 9 unknown gender', 'male, 2 females',
       'female  mother , unknown  baby ', 'at least one boy', 'mixed',
       'two girls, one boy', 'females, males']
idsgen = ["g"+str(i) for i in range(len(lista2))]
intermediario2 = {'genero': lista2, 'idgen': idsgen}

inter2 = pd.DataFrame(intermediario2)

dictgen = {}
for pos, elem in enumerate(lista2): 
    dictgen[elem] = 'g' + str(pos)

char['idgender'] = char['gender'].map(dictgen)

lista3 = list(char['species'].unique()) 
idspecies = ["sp"+str(i) for i in range(len(lista3))]
intermediario3 = {'especie': lista3, 'idsp': idsgen}

inter3 = pd.DataFrame(intermediario3)


'''
En esta parte del codigo nos apoyamos para asignarle un id a las
especies con el fin de crear csv intermedio para el posterior grafo en Neo4j. 
'''
dictsp = {}
for pos, elem in enumerate(lista3): 
    dictsp[elem] = 'sp' + str(pos)

char['idspecies'] = char['species'].map(dictsp)


'''
Se asigna un blood status a todos los valores missing. Esto con 
el fin de limpiar la variable de casos sin sentido. De esta manera, se podra
estructurar el grafo de mejor manera. 
Se debe agregar que, como en pasos anteriores, se izo uso de un diccionario
para el manejo y creacion de csv intermedio para el blood status.
'''
listasangre = list(char['blood_status'].unique())
listasangre.remove("missing")
def asignarSangre(cell):
    if cell == 'missing':
        return random.choice(listasangre)

    else: 
        return cell

char['blood_status'] = char['blood_status'].apply(asignarSangre)
dictsangre = {}
idsangre = []
for pos, elem in enumerate(listasangre):
    dictsangre[elem] = 's' + str(pos)
    idsangre.append('s' + str(pos))

intersangre = {'sangre': listasangre, 'idsangre': idsangre}

char['idsangre'] = char['blood_status'].map(dictsangre)

inter4 = pd.DataFrame(intersangre)


'''
Creamos los csv que seran cargados a Github. Con estos subiremos la base de datos
en Neo4j para el grafo. 
'''
# CSV donde tenemos todos los datos
#char.to_csv("characters", sep ='\t', encoding='utf-8', index=False, header = True)

# CSV donde tenemos los ids de las casas, intermediario 1
#inter.to_csv("houses_ids", sep = '\t', encoding='utf-8', index=False, header = True)

# CSV donde tenemos los ids del genero, intermediario 2
#inter2.to_csv("gender_ids", sep = '\t', encoding='utf-8', index=False, header = True)

# CSV donde tenemos los ids del genero, intermediario 3
#inter3.to_csv("species_ids", sep = '\t', encoding='utf-8', index=False, header = True)

# CSV donde tenemos los ids del genero, intermediario 4
#inter4.to_csv("bs_ids", sep = '\t', encoding='utf-8', index=False, header = True)