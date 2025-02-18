import csv
import sys
import time
import heapq  # Importar módulo heapq para la cola de prioridad

class Estado:
    def __init__(self, x, y, energia_restante, pacientes_a_recoger, pacientes_n, pacientes_c):
        self.x = x
        self.y = y
        self.energia_restante = energia_restante
        self.lista_pacientes_a_recoger = pacientes_a_recoger
        self.pacientes_n = pacientes_n
        self.pacientes_c = pacientes_c
        self.padre = None
    def __repr__(self):
        return f"Estado(x={self.x}, y={self.y}, pacientes_en_domicilio={self.lista_pacientes_a_recoger}" \
               f", energia={self.energia_restante}, pacientes_no_contagiosos_en_vehiculo={self.pacientes_n} " \
               f", pacientes_contagiosos_en_vehiculo={self.pacientes_c})"

class Mapa:
    def __init__(self, x, y, valor):
        self.x = x
        self.y = y
        self.valor = valor
    def __repr__(self):
        return f"Mapa(x={self.x}, y={self.y}, valor={self.valor})"



class Parte2:
    def main(self, archivo_mapa, numh):
        start_time = time.time()

        nodos_mapa, lista_pacientes = self.leerMapa(archivo_mapa)
        solucion, trayectoria, nodos_expandidos = self.aStar(nodos_mapa, lista_pacientes, numh)
        end_time = time.time()

        tiempo_total = end_time - start_time
        longitud_plan = len(trayectoria)
        coste_total = sum(estado[2] for estado in trayectoria)  # Aquí asumimos que 'estado[2]' es el coste

        print(solucion)

        # Llamadas a las funciones de generación de archivos
        self.generar_archivo_solucion(trayectoria, "archivo_solucion.txt", nodos_mapa)
        self.generar_archivo_estadisticas(tiempo_total, coste_total, longitud_plan, nodos_expandidos,
                                     "archivo_estadisticas.txt")

    def aStar(self, nodos_mapa, lista_pacientes, numh):
        parking = self.encontrar_nodo_por_valor(nodos_mapa, "P")
        estado_inicial = Estado(parking.x, parking.y, 50, lista_pacientes, 0, 0)
        abierta = []
        # Guardar una tupla con (coste_total, heuristica, coste, id_estado, estado), donde id_estado es un identificador único
        heapq.heappush(abierta, (0, 0, 0, id(estado_inicial), estado_inicial))
        cerrada = set()
        trayectoria = []

        while abierta:
            _, _, _, _, estado_elegido = heapq.heappop(abierta)
            if (estado_elegido.x, estado_elegido.y) in cerrada:
                continue

            cerrada.add((estado_elegido.x, estado_elegido.y))
            trayectoria.append((estado_elegido.x, estado_elegido.y, estado_elegido.energia_restante))

            # Condición de terminación exitosa
            if estado_elegido.x == parking.x and estado_elegido.y == parking.y and \
               estado_elegido.energia_restante >= 0 and \
               estado_elegido.pacientes_n == 0 and \
               estado_elegido.pacientes_c == 0 and \
               len(estado_elegido.lista_pacientes_a_recoger) == 0:
                return "Hay solucion", trayectoria, cerrada

            # Condición de fallo
            if estado_elegido.energia_restante == 0:
                return "No hay solucion", trayectoria, cerrada

            # Generar sucesores y actualizar la lista abierta
            sucesores = self.estadosSucesores(estado_elegido, nodos_mapa)
            for sucesor in sucesores:
                if (sucesor.x, sucesor.y) not in cerrada:
                    heuristica = self.heuristica1(sucesor, nodos_mapa) if numh == 1 else self.heuristica2(sucesor, nodos_mapa)
                    nodo = self.encontrar_nodo_por_coordenadas(nodos_mapa, sucesor.x, sucesor.y)
                    coste = self.calcularCoste(nodo)
                    coste_total = heuristica + coste
                    heapq.heappush(abierta, (coste_total, heuristica, coste, id(sucesor), sucesor))

        return "No hay solucion", trayectoria, cerrada

    def elegirSucesor(self, abierta):
        elegido = abierta[0]
        for elemento in abierta[1:]:
            if elemento[2] < elegido[2] or (elemento[2] == elegido[2] and elemento[0] < elegido[0]):
                elegido = elemento
        return elegido

    def calcularCoste(self, nodo):
        if nodo.valor == "2":
            coste = 2
        elif nodo.valor == "X":
            coste = float('inf')  # Hace intransitable la celda 'X'
        else:
            coste = 1
        return coste

    def heuristica1(self, estado, nodos_mapa):
        nodo_parking = self.encontrar_nodo_por_valor(nodos_mapa, "P")
        distancia_parking = abs(estado.x - nodo_parking.x) + abs(estado.y - nodo_parking.y)

        distancia_minima_pacientes = float('inf')
        distancia_minima_centro = float('inf')
        for paciente in estado.lista_pacientes_a_recoger:
            distancia_paciente = abs(estado.x - paciente.x) + abs(estado.y - paciente.y)
            if distancia_paciente < distancia_minima_pacientes:
                distancia_minima_pacientes = distancia_paciente
            centro = "CC" if paciente.valor == "C" else "CN"
            nodo_centro = self.encontrar_nodo_por_valor(nodos_mapa, centro)
            distancia_centro = abs(estado.x - nodo_centro.x) + abs(estado.y - nodo_centro.y)
            if distancia_centro < distancia_minima_centro:
                distancia_minima_centro = distancia_centro

        energia_requerida = min(distancia_minima_pacientes, distancia_minima_centro) + distancia_parking
        energia_insuficiente = max(0, energia_requerida - estado.energia_restante)

        pacientes_no_atendidos = len(estado.lista_pacientes_a_recoger)
        total_pacientes_vehiculo = estado.pacientes_n + estado.pacientes_c
        ajuste_pacientes_vehiculo = total_pacientes_vehiculo * 2

        ajuste_lejania_centro = 0
        if total_pacientes_vehiculo > 0 and distancia_minima_centro != 0:
            ajuste_lejania_centro = 2 / distancia_minima_centro

        eficiencia_recorrido = 0
        if distancia_minima_pacientes != 0:
            eficiencia_recorrido = 1 / distancia_minima_pacientes

        return energia_insuficiente + distancia_parking + pacientes_no_atendidos + ajuste_pacientes_vehiculo - eficiencia_recorrido - ajuste_lejania_centro

    def heuristica2(self, estado, nodos_mapa):
        total_distancia = 0

        # Obtener la posición del parking
        nodo_parking = self.encontrar_nodo_por_valor(nodos_mapa, "P")

        # Distancia de Manhattan hasta el parking
        distancia_parking = abs(estado.x - nodo_parking.x) + abs(estado.y - nodo_parking.y)

        # Distancia para cada paciente no atendido
        for paciente in estado.lista_pacientes_a_recoger:
            distancia_paciente = abs(estado.x - paciente.x) + abs(estado.y - paciente.y)
            centro = "CC" if paciente.valor == "C" else "CN"
            nodo_centro = self.encontrar_nodo_por_valor(nodos_mapa, centro)
            distancia_centro = abs(paciente.x - nodo_centro.x) + abs(paciente.y - nodo_centro.y)

            total_distancia += distancia_paciente + distancia_centro

        # Considerar pacientes en el vehículo
        total_pacientes_vehiculo = estado.pacientes_n + estado.pacientes_c
        if total_pacientes_vehiculo > 0:
            total_distancia += distancia_parking * 0.5 # Añadir la distancia para volver al parking

        # Ajuste por la eficiencia del trayecto
        ajuste_eficiencia = 1.0
        if estado.lista_pacientes_a_recoger:
            ajuste_eficiencia += 0.1 * len(estado.lista_pacientes_a_recoger)
        if total_pacientes_vehiculo > 0:
            ajuste_eficiencia += 0.1 * total_pacientes_vehiculo

        return total_distancia * ajuste_eficiencia

    def distancia_al_paciente_mas_cercano(self, nodo_actual, nodos):
        nodos_pacientes = [nodo for nodo in nodos if nodo.valor in ['N', 'C']]
        distancia_minima = float('inf')
        for paciente in nodos_pacientes:
            distancia = self.distancia_manhattan_nodos(nodo_actual, paciente)
            if distancia < distancia_minima:
                distancia_minima = distancia
        return distancia_minima if distancia_minima != float('inf') else None

    def distancia_manhattan_nodos(self, nodo1, nodo2):
        return abs(nodo1.x - nodo2.x) + abs(nodo1.y - nodo2.y)

    def agregar_sucesor(self, nodo, estado_actual, sucesores, nodos_mapa):
        if nodo:
            energia = estado_actual.energia_restante - (2 if nodo.valor == "2" else 1)
            pac_n = estado_actual.pacientes_n + (1 if nodo.valor == "N" else 0)
            pac_c = estado_actual.pacientes_c + (1 if nodo.valor == "C" else 0)

            lista_pacientes_actualizada = estado_actual.lista_pacientes_a_recoger.copy()
            if nodo.valor in ["N", "C"]:
                if nodo in lista_pacientes_actualizada:
                    lista_pacientes_actualizada.remove(nodo)

            if nodo.valor == "CC":
                pac_n = estado_actual.pacientes_n
                pac_c = 0
            elif nodo.valor == "CN":
                pac_n = 0
                pac_c = estado_actual.pacientes_c
            elif nodo.valor == "P":
                energia = 50

            sucesores.append(Estado(nodo.x, nodo.y, energia, lista_pacientes_actualizada, pac_n, pac_c))

    def estadosSucesores(self, estado_actual, nodos_mapa):
        sucesores = []
        coordenadas = [(estado_actual.x + 1, estado_actual.y), (estado_actual.x - 1, estado_actual.y),
                       (estado_actual.x, estado_actual.y - 1), (estado_actual.x, estado_actual.y + 1)]

        for x, y in coordenadas:
            nodo = self.encontrar_nodo_por_coordenadas(nodos_mapa, x, y)
            self.agregar_sucesor(nodo, estado_actual, sucesores, nodos_mapa)
            if nodo and nodo.valor in ["N", "C"]:
                nodo.valor = 1

        return sucesores


    def encontrar_nodo_por_coordenadas(self, nodos_mapa, x, y):
        for nodo in nodos_mapa:
            if nodo.x == x and nodo.y == y:
                return nodo
        return None

    def encontrar_nodo_por_valor(self, nodos_mapa, valor):
        for nodo in nodos_mapa:
            if nodo.valor == valor:
                return nodo
        return None


    def leerMapa(self, archivo_mapa):
        nodos_mapa = []
        lista_pacientes = []
        with open(archivo_mapa, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            mapa = [fila for fila in reader]
            for i in range(len(mapa)):
                fila = mapa[i]
                for j in range(len(fila)):
                    valor = mapa[j][i]
                    nodo = Mapa(i, j, valor)
                    if valor in ["N", "C"]:
                        lista_pacientes.append(nodo)
                    nodos_mapa.append(nodo)
        return nodos_mapa, lista_pacientes

    def generar_archivo_solucion(self, trayectoria, nombre_archivo, nodos_mapa):
        with open("parte-2/ASTAR-tests/"+nombre_archivo, "w") as archivo:
            for x, y, energia in trayectoria:
                nodo = self. encontrar_nodo_por_coordenadas(nodos_mapa, x, y)
                valor_celda = nodo.valor if nodo else "Desconocido"
                linea = f"({x},{y}):{valor_celda}:{energia}\n"
                archivo.write(linea)

    def generar_archivo_estadisticas(self, tiempo_total, coste_total, longitud_plan, nodos_expandidos, nombre_archivo):
        with open("parte-2/ASTAR-tests/"+nombre_archivo, "w") as archivo:
            archivo.write(f"Tiempo total: {tiempo_total:.2f} segundos\n")
            archivo.write(f"Coste total: {coste_total}\n")
            archivo.write(f"Longitud del plan: {longitud_plan}\n")
            archivo.write(f"Nodos expandidos: {nodos_expandidos}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python ASTARTraslados.py <path mapa.csv> <num-h>")
    else:
        parte2 = Parte2()
        parte2.main(sys.argv[1], int(sys.argv[2]))
