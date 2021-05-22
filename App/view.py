"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

connections = 'connections.csv'
landing_points = 'landing_points.csv'
countries = 'countries.csv'

def printMenu():
    print("Bienvenido")
    print("1- Inicializar el catalogo")
    print("2- Cargar información en el catálogo")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.initCatalog()

    elif int(inputs[0]) == 2:
        controller.loadData(catalog,connections,landing_points,countries)
        lastCountry=controller.lastCountry(catalog)
        firstLanding=controller.firstLandingPoint(catalog)
        print("Cantidad total de vertices:" , controller.graphSize(catalog['connections']))
        print("Cantidad total de arcos: ",controller.connectionsSize(catalog["connections"]))
        print("Cantidad de paises: ", controller.countrySize(catalog))
        print("\nLanding Point: ", firstLanding["landing_point_id"])
        print("Ubicación: ", firstLanding["name"])
        print("Latitud: ",firstLanding["latitude"])
        print("Longitud: ",firstLanding["longitude"])
        print("\nPais: ",lastCountry["CountryName"])
        print("Población: ",lastCountry["Population"])
        print("Usuarios de internet : ",lastCountry["Internet users"])
    elif int(inputs[0])==3:
        landing1=input("Escriba el nombre de la primera ciudad ")
        landing2=input("Escriba el nombre de la segunda ciudad ")
        
    else:
        sys.exit(0)
sys.exit(0)
