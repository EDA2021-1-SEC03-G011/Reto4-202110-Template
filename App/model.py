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


from DISClib.DataStructures.arraylist import iterator
from os import name
import config as cf
import math
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import linkedlistiterator as lti
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

    catalog["landing_points_name"]=lt.newList("ARRAY_LIST")

    catalog['countries'] = mp.newMap(numelements=250,maptype="PROBING")

    catalog["countries_name"]=lt.newList("ARRAY_LIST")

    
    catalog['landing_countries'] = mp.newMap(numelements=15000,
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


#Crea una tabla de hash donde las llaves son el nombre el pais y el valor son los landing points de dicho pais
def addLandingPoint(catalog, landing_point):
    lt.addLast(catalog["landing_points_name"],landing_point["landing_point_id"])

    mp.put(catalog['landing_points'],landing_point['landing_point_id'],landing_point)

    country = landing_point['name'].split(',')
    country = country[-1].lower()
    exists = mp.get(catalog['landing_countries'],country)
    if exists is None: 
        points_list=lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(points_list,landing_point['landing_point_id'])
    else:
        points_list=me.getValue(exists)
        if not lt.isPresent(points_list,landing_point['landing_point_id']):
            lt.addLast(points_list,landing_point['landing_point_id'])
    mp.put(catalog["landing_countries"],country,points_list)

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
            previous_cable=cable
        #Cerrar el ciclo al unir el primero con el ultimo
        cable = lt.firstElement(cable_names)
        origin=point+"-"+cable
        destination=point+"-"+previous_cable
        addConnection(catalog,origin,destination,0.1)

#Esta función es la que va a conectar las capitales con cada una las ciudades delpais
def addCountryConnections(catalog,country):
    country_couple=mp.get(catalog["landing_countries"],country["CountryName"])
    country_landings=me.getValue(country_couple)

    capital_name=country["CapitalName"]
    iterador=lti.newIterator(country_landings)

    while lti.hasNext(iterador):
        landing_point=lti.next(iterador)

    


def addCountryPoint(catalog, country):
    if country['CountryName'] != "":
        countryname = country['CountryName']+'-'+country['CapitalName']
        addJoint(catalog, countryname)

def addCountry(catalog,country):
    mp.put(catalog["countries"],country["CountryName"],country)
    lt.addLast(catalog["countries_name"],country["CountryName"])

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


# Funciones de consulta

def graphSize(graph):
    return gr.numVertices(graph)

def connectionsSize(graph):
    return gr.numEdges(graph)

# Funciones utilizadas para comparar elementos dentro de una lista

def countrySize(catalog):

    return lt.size(catalog["countries_name"])

def lastCountry(catalog):
    lastCountry=lt.lastElement(catalog["countries_name"])

    couple=mp.get(catalog["countries"],lastCountry)
    
    country_info=me.getValue(couple)

    return country_info


def firstLandingPoint(catalog):
    firstLanding=lt.firstElement(catalog["landing_points_name"])
    
    couple=mp.get(catalog["landing_points"],firstLanding)

    landing_info=me.getValue(couple)

    return landing_info


def compareJointId(stop, keyvaluestop):
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop >stopcode):
        return 1
    else:
        return -1

# Funciones de ordenamiento
