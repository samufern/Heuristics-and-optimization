from constraint import *
import csv
import ast
import random

class Parte1:
    def main(self, parking):
        print(parking)
        self.filas, self.columnas, self.plazas_conexion_electrica, self.vehiculos = self.leer_parking_csv(parking)
        dominio = self.vehiculos + ['-']
        self.plazas = []
        problema = Problem()
        for i in range(1, self.filas+1):
            for j in range(1, self.columnas+1):
                plaza = (i, j)
                problema.addVariable(plaza, dominio)
                self.plazas.append(plaza)
        problema.addConstraint(self.plaza_unica_vehiculo, self.plazas)
        problema.addConstraint(self.restriccion_conexion_electrica, self.plazas)
        problema.addConstraint(self.restriccion_TSU_delante, self.plazas)
        problema.addConstraint(self.restriccion_izquierda_derecha, self.plazas)
        soluciones = problema.getSolutions()
        self.archivo_salida(self.columnas, self.filas, soluciones, parking)

    def restriccion_izquierda_derecha(self,*plazas_asignadas):
        diccionario_asignaciones = {clave: valor for clave, valor in zip(self.plazas, plazas_asignadas)}
        for plaza, vehiculo in diccionario_asignaciones.items():
            fila_actual, columna_actual = plaza
            if vehiculo != '-': # Si hay un vehículo en la plaza actual, comprobar las plazas izquierda y derecha
                if fila_actual > 1: # Comprobar la plaza encima (si no es la primera fila)
                    plaza_encima = (fila_actual - 1, columna_actual)
                    if diccionario_asignaciones.get(plaza_encima) != '-':
                        return False  # Hay un vehículo en la plaza izquierda
                if fila_actual < self.filas: # Comprobar la plaza debajo (si no es la última fila)
                    plaza_debajo = (fila_actual + 1, columna_actual)
                    if diccionario_asignaciones.get(plaza_debajo) != '-':
                        return False  # Hay un vehículo en la plaza derecha
        return True  # No se encontró ningún vehículo encima o debajo de otro vehículo

    def restriccion_TSU_delante(self, *plazas_asignadas):
        diccionario_asignaciones = {clave: valor for clave, valor in zip(self.plazas, plazas_asignadas)}
        for plaza, vehiculo in diccionario_asignaciones.items():
            fila_actual, columna_actual = plaza
            if 'TSU' in vehiculo:  # Si el vehículo actual es TSU, buscar un TNU delante en la misma fila
                # Verificar cada plaza delante en la misma fila
                for columna_siguiente in range(columna_actual + 1, max(columna for fila, columna in diccionario_asignaciones.keys()) + 1):
                    plaza_siguiente = (fila_actual, columna_siguiente) # Si la plaza siguiente está en el diccionario y tiene un TNU, devolver False
                    if plaza_siguiente in diccionario_asignaciones and 'TNU' in diccionario_asignaciones[plaza_siguiente]:
                        return False  # Se encontró un TNU delante de un TSU
        return True

    def vehiculo_requiere_conexion(self, vehiculo):
        """Devuelve True si el vehículo tiene congelador, identificado por una 'C' al final."""
        return vehiculo.endswith('C')

    def restriccion_conexion_electrica(self, *plazas_asignadas):
        """Asegura que los vehículos con congelador solo se ubiquen en plazas con conexión eléctrica. """
        diccionario_asignaciones = {clave: valor for clave, valor in zip(self.plazas, plazas_asignadas)}
        for plaza, vehiculo in diccionario_asignaciones.items():
            if plaza in self.plazas_conexion_electrica and "-C" not in vehiculo:
                return False
        return True

    def archivo_salida(self, columnas, filas, soluciones, parking):
        soluciones_max = 5
        with open(parking+".csv", 'w') as archivo:
            archivo.write("Nº Soluciones:"+ str(len(soluciones))+"\n")

            matriz = [['' for _ in range(columnas)] for _ in range(filas)]
            if len(soluciones) > soluciones_max:
                num = [random.randint(0, len(soluciones)-1) for _ in range(soluciones_max)]
                for i in range(len(num)):
                    archivo.write("\n")
                    solucion = soluciones[num[i]]
                    for clave, valor in solucion.items():
                        coordenadas = (clave[0], clave[1])
                        fila = int(coordenadas[0]) - 1
                        columna = int(coordenadas[1]) - 1
                        matriz[fila][columna] = valor
                    for fila in matriz:
                        linea = ", ".join(f'"{valor}"' for valor in fila)
                        # print(linea)
                        archivo.write(linea + '\n')
            else:
                for solucion in soluciones:
                    archivo.write("\n")
                    for clave, valor in solucion.items():
                        coordenadas = (clave[0], clave[1])
                        fila = int(coordenadas[0]) - 1
                        columna = int(coordenadas[1]) - 1
                        matriz[fila][columna] = valor
                    for fila in matriz:
                        linea = ", ".join(f'"{valor}"' for valor in fila)
                        # print(linea)
                        archivo.write(linea + '\n')


    def id_vehiculo(self,vehiculo):
        """Función para extraer el ID del vehículo (o '-' si la plaza está vacía)."""
        return vehiculo.split('-')[0] if vehiculo != '-' else '-'

    def plaza_unica_vehiculo(self, *args):
        """ Función de restricción para asegurar que cada vehículo sea asignado a una plaza única."""
        ids_vehiculos = [self.id_vehiculo(v) for v in args if self.id_vehiculo(v) != '-']
        return len(ids_vehiculos) == len(set(ids_vehiculos)) and len(ids_vehiculos) == len(self.vehiculos)  # Asegurar dos vehículos asignados

    def leer_parking_csv(self, parking):
        with open(parking, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='\n')
            dimensions = next(reader)[0].split('x') # Leer la primera línea para obtener las dimensiones del parking
            filas, columnas = int(dimensions[0]), int(dimensions[1])
            plazas_conexion_electrica = next(reader)[0].split(' ') # Leer la segunda línea para obtener las plazas con conexión eléctrica
            for i in range(len(plazas_conexion_electrica)): # Convertirlas a tuplas para acceder a las coordenadas
                plaza_tupla = ast.literal_eval(plazas_conexion_electrica[i])
                plazas_conexion_electrica[i] = plaza_tupla
            vehiculos = [] # Leer las líneas restantes para obtener información de los vehículos
            for row in reader:
                vehiculos.append(row[0])
            return filas,columnas,plazas_conexion_electrica, vehiculos


p1 = Parte1()

