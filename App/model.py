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
from DISClib.DataStructures import linkedlistiterator as lli
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
# Construccion de modelos
def newCatalog():

    catalog = {
               'graph':None,
               'landing_points_map':None,
               'countries':None
               }

    catalog['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                         directed = False,
                                         size= 15000,
                                         comparefunction=compareJointId)

    catalog['landing_points_map'] = mp.newMap(numelements=15000,
                                          maptype='PROBING')
    
    catalog['same_landing_point_map']=mp.newMap(numelements=1500,maptype='PROBING')
    

    catalog['countries'] = mp.newMap(numelements=250,
                                          maptype='PROBING')
    
    catalog['landing_by_country_map'] = mp.newMap(numelements=15000,
                                          maptype='PROBING')

    catalog["countries_name"]=lt.newList("ARRAY_LIST")

    catalog["landing_points_name"]=lt.newList("ARRAY_LIST")
    
    return catalog



# Funciones para agregar informacion al catalogo

def addLandingPoint(catalog, landing_point):
    """
    Agrega a un mapa por llaves landing_point_id y valor la info de ese
    Agrega a un mapa por llaves country y valores listas de landing de este country
    """
    mp.put(catalog['landing_points_map'],landing_point['landing_point_id'],landing_point)
    lt.addLast(catalog["landing_points_name"],landing_point["landing_point_id"])

    country = landing_point['name'].split(',')
    country = country[-1].lower().strip()
    exists = mp.get(catalog['landing_by_country_map'],country)

    if exists is None: 
        points_list=lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(points_list,landing_point['landing_point_id'])
    else:
        points_list=me.getValue(exists)
        if not lt.isPresent(points_list,landing_point['landing_point_id']):
            lt.addLast(points_list,landing_point['landing_point_id'])

    mp.put(catalog["landing_by_country_map"],country,points_list)

def addCable(catalog, cable):

    origin = cable['origin']
    ori_couple = mp.get(catalog['landing_points_map'],origin)
    ori_coor = me.getValue(ori_couple)

    destination = cable['destination']
    des_couple = mp.get(catalog['landing_points_map'],destination)
    des_coor = me.getValue(des_couple)

    distance = haversine (float(ori_coor['latitude']),float(ori_coor['longitude']),float(des_coor['latitude']),float(des_coor['longitude']))

    name_ori = formatVertex(cable['origin'],cable['cable_name'])
    name_des = formatVertex(cable['destination'],cable['cable_name'])

    addJoint(catalog,name_ori)
    addJoint(catalog,name_des)

    addConnection(catalog, name_ori, name_des, distance)
    
    addLandingFamily(catalog,cable['origin'],name_ori) 
    addLandingFamily(catalog,cable['destination'],name_des) 

def addLandingConnection(catalog):
    landing_points_list=mp.keySet(catalog["same_landing_point_map"])

    for landing_point in lt.iterator(landing_points_list):
        cable_couple=mp.get(catalog["same_landing_point_map"],landing_point)
        cable_names=me.getValue(cable_couple)
        previous_cable=None
        for cable in lt.iterator(cable_names):
            if previous_cable!=None:
                origin= cable
                destination= previous_cable
                addConnection(catalog,origin,destination,0.1)
                
            previous_cable=cable
        #Cerrar el ciclo al unir el primero con el ultimo
        cable = lt.firstElement(cable_names)
        origin=cable
        destination=previous_cable
        addConnection(catalog,origin,destination,0.1)

def addCountryPoint(catalog, country):
    if country['CountryName'] != "":
        countryname = country['CountryName']+'-'+country['CapitalName']
        addJoint(catalog, countryname)

def addCountryPoint(catalog, country):
    if country['CountryName'] != "":
        countryname = country['CountryName']+'-'+country['CapitalName']
        addJoint(catalog, countryname)

def addCountry(catalog,country):
    mp.put(catalog["countries"],country["CountryName"],country)
    lt.addLast(catalog["countries_name"],country)

def addCountryConnections(catalog,country):
    country_lat = country["CapitalLatitude"]
    country_lon = country["CapitalLongitude"]

    countries_couple = mp.get(catalog['landing_by_country_map'],country['CountryName'].lower())

    if countries_couple is not None:
        countries_list = me.getValue(countries_couple)

        for landingpoint in lt.iterator(countries_list):
            info_couple = mp.get(catalog['landing_points_map'],landingpoint)
            info = me.getValue(info_couple)

            landing_lat = info['latitude']
            landing_lon = info['longitude']

            distance = haversine(float(country_lat),float(country_lon),float(landing_lat),float(landing_lon))

            family_couple = mp.get(catalog['same_landing_point_map'],landingpoint)
            family = me.getValue(family_couple)

            for cable in lt.iterator(family):
                addConnection(catalog, cable, country['CountryName']+'-'+country['CapitalName'],distance)
    else: 
        minimum = 1000000 
        landind_ward = None
        landing_points = mp.keySet(catalog['landing_points_map'])
        for landing_point in lt.iterator(landing_points):
            info_couple = mp.get(catalog['landing_points_map'],landing_point)
            info = me.getValue(info_couple)

            landing_lat = info['latitude']
            landing_lon = info['longitude']

            distance = haversine(float(country_lat),float(country_lon),float(landing_lat),float(landing_lon))

            if distance < minimum:
                minimum = distance
                landind_ward = landing_point
        
        family_couple = mp.get(catalog['same_landing_point_map'],landind_ward)
        family = me.getValue(family_couple)
        for cable in lt.iterator(family):
            addConnection(catalog, cable, country['CountryName']+'-'+country['CapitalName'],minimum)


# Funciones para creacion de datos

def formatVertex(origin, name):
    format = origin + '-' + name
    return format

def addJoint(catalog, vertex):
    if not gr.containsVertex(catalog['graph'],vertex):
        gr.insertVertex(catalog['graph'],vertex)

def addConnection(catalog, origin, destination, distance):
    edge = gr.getEdge(catalog['graph'],origin,destination)
    if edge is None:
        gr.addEdge(catalog['graph'],origin, destination,distance)

def addLandingFamily(catalog,landing_point,format_name):

    same_landing=mp.get(catalog["same_landing_point_map"],landing_point)
    if same_landing is None: 
        cables_list=lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(cables_list,format_name)
    else:
        cables_list=me.getValue(same_landing)
        if not lt.isPresent(cables_list,format_name):
            lt.addLast(cables_list,format_name)
    mp.put(catalog["same_landing_point_map"],landing_point,cables_list)


# Funciones de consulta

def graphSize(graph):
    return gr.numVertices(graph)

def connectionsSize(graph):
    return gr.numEdges(graph)

def countrySize(catalog):
    return lt.size(catalog["countries_name"])

def lastCountry(catalog):
    lastCountry=lt.lastElement(catalog["countries_name"])
    return lastCountry

def firstLandingPoint(catalog):
    firstLanding=lt.firstElement(catalog["landing_points_name"])
    
    couple=mp.get(catalog["landing_points_map"],firstLanding)

    landing_info=me.getValue(couple)

    return landing_info

# Funciones utilizadas para comparar elementos dentro de un grafo

def compareJointId(stop, keyvaluestop):
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop >stopcode):
        return 1
    else:
        return -1

# Funciones de ordenamiento

# Funciones para hacer calculos 

def haversine(lat1,lon1,lat2,lon2):
    radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

