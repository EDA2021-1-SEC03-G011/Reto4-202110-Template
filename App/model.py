"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from os import name
import config as cf
import math
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
# Construccion de modelos
def newCatalog():

    catalog = {
               'connections':None,
               'landing_points':None,
               'countries':None
               }

    catalog['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                         directed = False,
                                         size= 15000,
                                         comparefunction=compareJointId)
    
    catalog['local_landings']=mp.newMap(numelements=1500,maptype='PROBING')
    catalog['landing_points'] = mp.newMap(numelements=15000,
                                          maptype='PROBING')

    catalog['countries'] = mp.newMap(numelements=250,
                                          maptype='PROBING')

    return catalog



# Funciones para agregar informacion al catalogo

def addCable(catalog, cable):
    origin = cable['origin']
    destination = cable['destination']
    ori_couple = mp.get(catalog['landing_points'],origin)
    ori_coor = me.getValue(ori_couple)
    des_couple = mp.get(catalog['landing_points'],destination)
    des_coor = me.getValue(des_couple)
    distance = haversine (float(ori_coor['latitude']),float(ori_coor['longitude']),float(des_coor['latitude']),float(des_coor['longitude']))
    name_ori = formatVertex(cable['origin'],cable['cable_name'])
    name_des = formatVertex(cable['destination'],cable['cable_name'])
    addJoint(catalog,name_ori)
    addJoint(catalog,name_des)
    addConnection(catalog, name_ori, name_des, distance)
    addRoute(catalog,cable['origin'],cable["cable_name"])
    addRoute(catalog,cable['destination'],cable["cable_name"])


# Funciones para creacion de datos



def addLandingPoint(catalog, landing_point):
    mp.put(catalog['landing_points'],landing_point['landing_point_id'],landing_point)

def formatVertex(origin, name):
    format = origin + '-' + name
    return format

def addJoint(catalog, vertex):
    if not gr.containsVertex(catalog['connections'],vertex):
        gr.insertVertex(catalog['connections'],vertex)

def addConnection(catalog, origin, destination, distance):
    edge = gr.getEdge(catalog['connections'],origin,destination)
    if edge is None:
        gr.addEdge(catalog['connections'],origin, destination,distance)



def haversine(lat1,lon1,lat2,lon2):


    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def addRoute(catalog,landing_point,cable_name):

    p=mp.get(catalog["local_landings"],landing_point)
    if p is None: 
        cables_list=lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(cables_list,cable_name)
    else:
        cables_list=me.getValue(p)
        if not lt.isPresent(cables_list,cable_name):
            lt.addLast(cables_list,cable_name)
    mp.put(catalog["local_landings"],landing_point,cables_list)

def addLandingConnection(catalog):
    landing_points=mp.keySet(catalog["local_landings"])

    for point in lt.iterator(landing_points):
        cable_couple=mp.get(catalog["local_landings"],point)
        cable_names=me.getValue(cable_couple)
        previous_cable=None
        for cable in lt.iterator(cable_names):
            if previous_cable!=None:
                origin=point+"-"+cable
                destination=point+"-"+previous_cable
                addConnection(catalog,origin,destination,0.1)
                print("hola")
            previous_cable=cable




# Funciones de consulta

def graphSize(graph):
    return gr.numVertices(graph)

# Funciones utilizadas para comparar elementos dentro de una lista

def compareJointId(stop, keyvaluestop):
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop >stopcode):
        return 1
    else:
        return -1

# Funciones de ordenamiento

print(haversine(4.716165657240686, -74.049249231947, 5.780219354367528, -73.12374102667047))