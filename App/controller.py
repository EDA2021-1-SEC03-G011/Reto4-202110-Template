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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo
def initCatalog():
    return model.newCatalog()

# Funciones para la carga de datos
def loadData(catalog,connections,landing_points,countries):

    landing_points = cf.data_dir + landing_points
    input_file_landing = csv.DictReader(open(landing_points, encoding='utf-8'))

    for landing_point in input_file_landing:
        model.addLandingPoint(catalog, landing_point)

    connections = cf.data_dir + connections
    input_file_cable = csv.DictReader(open(connections, encoding='utf-8'))
    lastcable = None

    for cable in input_file_cable:
        if lastcable is not None:
            cable['origin'] = cable['\ufefforigin']
            samecable = cable['origin'] == lastcable['destination']
            if not samecable:
                model.addCable(catalog, cable)
        lastcable = cable
    model.addLandingConnection(catalog)



# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def graphSize(graph):
    return model.graphSize(graph)