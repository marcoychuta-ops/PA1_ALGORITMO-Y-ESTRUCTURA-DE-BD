"""
PA1 - Evaluacion aplicada sobre estructuras lineales estaticas
Curso 30710 - Algoritmo y Estructura de Datos Basados en Inteligencia Artificial

Implementacion ejecutable de las Actividades 2, 3 y 4.

Ejecutar desde la raiz del repositorio:
    python codigo/main.py
"""

# ---------------------------------------------------------------------------
# ACTIVIDAD 2 - Vector de inscritos por taller
# ---------------------------------------------------------------------------

CAPACIDAD = 10  # capacidad fija reservada (estructura estatica)


def mostrar_vector(v, n):
    """Representacion grafica del vector con indices y valores."""
    indices = "  i:  " + "  ".join(f"{i:>2}" for i in range(len(v)))
    valores = "  v:  " + "  ".join(f"{x:>2}" for x in v)
    huecos = len(v)
    if n < CAPACIDAD:
        indices += "  " + "  ".join(f"{i:>2}" for i in range(huecos, CAPACIDAD))
        valores += "  " + "  ".join("---" for _ in range(CAPACIDAD - huecos))
    print(indices)
    print(valores)


def mayor_menor(v):
    """Devuelve (mayor, posMayor, menor, posMenor) recorriendo el vector una vez."""
    if not v:
        return None, None, None, None
    mayor = menor = v[0]
    posMayor = posMenor = 0
    for i in range(1, len(v)):
        if v[i] > mayor:
            mayor, posMayor = v[i], i
        if v[i] < menor:
            menor, posMenor = v[i], i
    return mayor, posMayor, menor, posMenor


def insertar(v, posicion, valor, capacidad=CAPACIDAD):
    """Inserta 'valor' en 'posicion' con desplazamiento a la derecha.

    Si no hay espacio libre (n >= capacidad) indica 'vector lleno'.
    """
    n = len(v)
    if n >= capacidad:
        print(f"  -> vector lleno: no hay espacio (capacidad {capacidad})")
        return False
    if posicion < 0 or posicion > n:
        print(f"  -> posicion invalida (permitida: 0 a {n})")
        return False
    v.append(None)  # ocupa la nueva posicion (el arreglo tenia espacio reservado)
    for i in range(n - 1, posicion - 1, -1):
        v[i + 1] = v[i]
    v[posicion] = valor
    print(f"  -> insertado {valor} en la posicion {posicion}")
    return True


def ordenar_burbuja(v):
    """Ordenamiento burbuja con bandera. Devuelve el numero de comparaciones."""
    comparaciones = 0
    n = len(v)
    intercambiado = True
    pasada = 1
    while intercambiado and pasada < n:
        intercambiado = False
        for i in range(0, n - pasada):
            comparaciones += 1
            if v[i] > v[i + 1]:
                v[i], v[i + 1] = v[i + 1], v[i]
                intercambiado = True
        pasada += 1
    return comparaciones


def actividad_2():
    print("=" * 70)
    print("ACTIVIDAD 2 - Modelado y operaciones con vectores")
    print("=" * 70)
    v = [28, 15, 34, 21, 19, 40, 12, 26]
    print("\n2.1 Vector con indices y valores:")
    mostrar_vector(v, len(v))

    mayor, posM, menor, posm = mayor_menor(v)
    print(f"\n2.2 Mayor = {mayor} (indice {posM}) | Menor = {menor} (indice {posm})")
    print("    Costo: una sola pasada => O(n)")

    print("\n2.3 Insercion de un nuevo taller (posicion indicada por el usuario):")
    copia = v[:]
    print(f"    Antes : {copia}")
    insertar(copia, 4, 31)
    print(f"    Despues: {copia}")
    # Demostracion del caso sin espacio (capacidad completa)
    lleno = list(range(CAPACIDAD))
    print("    Prueba con el vector lleno:")
    insertar(lleno, 5, 99)

    print("\n2.4 Ordenamiento de menor a mayor (burbuja con bandera):")
    ya_ordenado = sorted(v)
    c_mejor = ordenar_burbuja(ya_ordenado)          # mejor caso: ya ordenado
    inverso = sorted(v, reverse=True)
    c_peor = ordenar_burbuja(inverso)               # peor caso: orden inverso
    ordenado = v[:]
    c_normal = ordenar_burbuja(ordenado)            # caso del vector del examen
    n = len(v)
    print(f"    Vector original      : {v}")
    print(f"    Ordenado             : {ordenado}")
    print(f"    Mejor caso (ya ordenado): {c_mejor} comparaciones = n-1 = {n - 1}  => O(n)")
    print(f"    Peor caso (inverso)     : {c_peor} comparaciones = n(n-1)/2 = {n * (n - 1) // 2}  => O(n2)")
    print(f"    Este caso               : {c_normal} comparaciones")
    print()


# ---------------------------------------------------------------------------
# ACTIVIDAD 3 - Matriz de ocupacion de aulas (4 filas x 5 columnas)
# ---------------------------------------------------------------------------

MATRIZ = [
    [10, 12, 8, 15, 9],   # Aula 1
    [7, 9, 11, 6, 10],    # Aula 2
    [12, 8, 14, 9, 7],    # Aula 3
    [6, 5, 9, 8, 11],     # Aula 4
]
AULAS = ["Aula 1", "Aula 2", "Aula 3", "Aula 4"]
BLOQUES = ["7:00", "8:00", "9:00", "10:00", "11:00"]


def mostrar_matriz(m):
    ancho = 13
    print(" " * ancho + "".join(f"{('j=' + str(j)):>8}" for j in range(len(m[0]))))
    print(" " * ancho + "".join(f"{BLOQUES[j]:>8}" for j in range(len(m[0]))))
    for i, fila in enumerate(m):
        print(f"  i={i} {AULAS[i]:<7}"[:ancho] + "".join(f"{x:>8}" for x in fila))


def totales_por_aula(m):
    return [sum(fila) for fila in m]


def totales_por_horario(m):
    filas, cols = len(m), len(m[0])
    return [sum(m[i][j] for i in range(filas)) for j in range(cols)]


def celda_maxima(m):
    max_valor, max_fila, max_col = m[0][0], 0, 0
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j] > max_valor:
                max_valor, max_fila, max_col = m[i][j], i, j
    return max_valor, max_fila, max_col


def actividad_3():
    print("=" * 70)
    print("ACTIVIDAD 3 - Matrices y recorrido completo de datos")
    print("=" * 70)
    print("\n3.1 Matriz propuesta (4 aulas x 5 bloques horarios):")
    mostrar_matriz(MATRIZ)

    print("\n3.2 Total de estudiantes por AULA (recorrido de filas):")
    for nombre, total in zip(AULAS, totales_por_aula(MATRIZ)):
        print(f"    {nombre}: {total}")
    print(f"    Total general: {sum(totales_por_aula(MATRIZ))}")

    print("\n3.3 Total de estudiantes por HORARIO (recorrido de columnas):")
    for nombre, total in zip(BLOQUES, totales_por_horario(MATRIZ)):
        print(f"    Bloque {nombre}: {total}")

    valor, fila, col = celda_maxima(MATRIZ)
    print("\n3.4 Celda con mayor ocupacion:")
    print(f"    Valor {valor} en (fila {fila}, columna {col}) "
          f"= {AULAS[fila]}, bloque {BLOQUES[col]}")

    f, c = len(MATRIZ), len(MATRIZ[0])
    print(f"\n3.5 Se recorren todas las celdas: {f}x{c} = {f * c} posiciones => O(F x C)")
    print()


# ---------------------------------------------------------------------------
# ACTIVIDAD 4 - Matrices especiales y decision tecnica
# ---------------------------------------------------------------------------

def actividad_4():
    print("=" * 70)
    print("ACTIVIDAD 4 - Matrices especiales y decision tecnica")
    print("=" * 70)

    cuadrada = [[5, 0, 3],
                [0, 8, 1],
                [2, 0, 4]]
    print("\n4.1 Matriz cuadrada 3x3 (filas = columnas = 3):")
    for fila in cuadrada:
        print("     ", fila)
    print("      Diagonal principal (i = j):", [cuadrada[i][i] for i in range(3)])

    dispersa = [[0, 0, 3, 0, 0],
                [0, 0, 0, 0, 2],
                [5, 0, 0, 0, 0],
                [0, 0, 0, 4, 0]]
    filas, cols = len(dispersa), len(dispersa[0])
    no_ceros = sum(1 for fila in dispersa for x in fila if x != 0)
    celdas = filas * cols
    densidad = no_ceros / celdas

    print("\n4.2 Matriz poco densa (coincidencias entre talleres):")
    for fila in dispersa:
        print("     ", fila)
    print(f"      Densidad = {no_ceros}/{celdas} = {densidad:.0%}  => poco densa")

    tripletas = [(i, j, dispersa[i][j])
                 for i in range(filas) for j in range(cols) if dispersa[i][j] != 0]
    print("\n4.3 Comparacion de memoria (lista de tripletas vs. matriz completa):")
    print(f"      Matriz completa : {celdas} posiciones guardadas")
    print(f"      Poco densa      : {len(tripletas)} tripletas (fila, columna, valor)")
    print(f"      Ahorro          : {celdas - len(tripletas)} posiciones "
          f"({(celdas - len(tripletas)) / celdas:.0%})")
    print("      Decision: se usa la matriz POCO DENSA porque casi todas las")
    print("      combinaciones aula x bloque son cero (datos escasos por naturaleza).")
    print()


if __name__ == "__main__":
    actividad_2()
    actividad_3()
    actividad_4()
