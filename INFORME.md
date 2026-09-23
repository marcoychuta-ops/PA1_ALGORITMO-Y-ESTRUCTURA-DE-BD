# PA1 – Evaluación aplicada sobre estructuras lineales estáticas

**Curso:** 30710 – Algoritmo y Estructura de Datos Basados en Inteligencia Artificial
**Cobertura temática:** Sesiones 1 a 4 – Datos y algoritmos; clasificaciones; estructuras estáticas y dinámicas; arreglos unidimensionales; operaciones; ordenamiento; eficiencia; matrices; matrices especiales.
**Modalidad:** Grupal (4 integrantes; máximo 5)

---

## Actividad 1. Análisis del problema y selección de estructura

### 1.1 Diferencia entre estructura estática y estructura dinámica

| Aspecto | Estructura estática | Estructura dinámica |
|---|---|---|
| Tamaño | Fijo desde su creación; no cambia en tiempo de ejecución | Crece o se reduce durante la ejecución |
| Ejemplos | Arreglos (vectores), matrices | Listas enlazadas, pilas, colas, árboles |
| Ubicación de los datos | Contiguos en memoria | Dispersos; se enlazan con referencias/punteros |
| Acceso | Directo por índice: `v[i]` en tiempo O(1) | Recorrido desde un nodo inicial |
| Costo de inserción/eliminación | Requiere desplazamiento de elementos | Reasignación de enlaces |

- **Estática:** la cantidad de posiciones se define al momento de declararla (por ejemplo, un arreglo de 10 enteros). Una vez creada, esa capacidad no cambia.
- **Dinámica:** la estructura se adapta a los datos (por ejemplo, una lista enlazada agrega nodos según se necesite).

### 1.2 Por qué, para esta primera etapa, conviene usar arreglos y matrices

1. **El tamaño del problema es conocido y estable:** la institución trabaja con un conjunto definido de talleres y con 4 aulas × 5 bloques horarios; no se espera que la cantidad de datos cambie abruptamente.
2. **Acceso directo y rápido:** el índice permite obtener cualquier posición en tiempo constante, ideal para consultas puntuales (¿cuántos inscritos tiene el taller 5?).
3. **Recorrido sencillo para totales y máximos:** las matrices permiten sumar filas y columnas con ciclos simples y bien estructurados.
4. **Bajo sobrecoste:** no hay gasto en punteros ni gestión de memoria dinámica, lo que facilita el análisis del costo de los algoritmos (eficiencia, tema de la sesión 4).
5. **Coherencia con la etapa del sistema:** la *primera etapa* trabaja únicamente con estructuras lineales estáticas; las dinámicas quedarán para etapas posteriores cuando los datos crezcan de forma impredecible.

### 1.3 Dato, algoritmo y estructura de datos en la solución

- **Dato:** cada valor sin procesar, por ejemplo *28* (cantidad de inscritos del taller 1) o *15* (ocupación del aula 2 en el bloque 0).
- **Estructura de datos:** la forma en que se **organizan y relacionan** los datos para manipularlos. Aquí: un **vector unidimensional** para los inscritos por taller y una **matriz de 4×5** para la ocupación de aulas por bloque horario.
- **Algoritmo:** la secuencia finita de pasos que procesa esos datos con esa estructura, por ejemplo: *encontrar el mayor*, *insertar un valor en una posición*, *ordenar de menor a mayor*, *sumar cada fila (total por aula)*.

Relación en la solución planteada: los **datos** (inscritos y ocupaciones) se almacenan en **estructuras estáticas** (vector y matriz) y se transforman mediante **algoritmos** (búsqueda de extremos, inserción con desplazamiento, ordenamiento burbuja y recorrido completo de la matriz) hasta entregar la información pedida (ordenes, totales y celda con mayor ocupación).

---

## Actividad 2. Modelado y operaciones con vectores

Vector de inscritos por taller:

```
[28, 15, 34, 21, 19, 40, 12, 26]
```

### 2.1 Representación gráfica con índices y valores

```
        Vector INSCRITOS (n = 8)

  Índice:   0    1    2    3    4    5    6    7   |  8     9
         ┌────┬────┬────┬────┬────┬────┬────┬────┬─┬──────┬──────┐
  Valor: │ 28 │ 15 │ 34 │ 21 │ 19 │ 40 │ 12 │ 26 │ │ libre│ libre│
         └────┴────┴────┴────┴────┴────┴────┴────┴─┴──────┴──────┘
          ▲                                          ▲
          │                                          │
   primero (v[0])                            capacidad reservada (10)
                                               para futuros talleres
```

| Índice | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| **Valor** | 28 | 15 | 34 | 21 | 19 | 40 | 12 | 26 | libre | libre |

> El arreglo se declara con **capacidad fija 10** (8 talleres actuales + 2 de margen). Es estático: si no queda espacio libre, la inserción no es posible y el algoritmo debe indicar «vector lleno».

### 2.2 Algoritmo para encontrar el valor mayor y el menor

```pseudocode
ALGORITMO MayorMenor(lista, n)
1. SI n = 0 ENTONCES
2.    REPORTAR "vector vacío"
3.    TERMINAR
4. FIN SI
5. mayor  <- lista[0]
6. menor  <- lista[0]
7. PARA i DESDE 1 HASTA n - 1 HACER
8.    SI lista[i] > mayor ENTONCES
9.       mayor <- lista[i]
10.       posMayor <- i
11.    FIN SI
12.    SI lista[i] < menor ENTONCES
13.       menor <- lista[i]
14.       posMenor <- i
15.    FIN SI
16. FIN PARA
17. REPORTAR mayor, posMayor, menor, posMenor
FIN ALGORITMO
```

**Aplicado al vector:**

- **Mayor:** 40 en la posición (índice) **5**.
- **Menor:** 12 en la posición (índice) **6**.

**Costo:** se recorre una sola vez el vector ⇒ **O(n)** comparaciones en ambos casos (aquí 7 comparaciones).

```mermaid
flowchart LR
  A[Inicio: mayor=lista[0], menor=lista[0]] --> B{i < n?}
  B -- Sí --> C[lista[i] > mayor?]
  C -- Sí --> D[mayor = lista[i]]
  C -- No --> E[lista[i] < menor?]
  D --> E
  E -- Sí --> F[menor = lista[i]]
  E -- No --> G[i = i + 1]
  F --> G
  G --> B
  B -- No --> H[REPORTAR mayor y menor]
```

### 2.3 Algoritmo para insertar un nuevo valor en una posición indicada por el usuario

```pseudocode
ALGORITMO Insertar(lista, n, capacidad, posicion, valor)
1. SI n >= capacidad ENTONCES
2.    REPORTAR "vector lleno: no hay espacio para un nuevo taller"
3.    TERMINAR
4. FIN SI
5. SI posicion < 0 O posicion > n ENTONCES
6.    REPORTAR "posición inválida (permitida: 0 a " + n + ")"
7.    TERMINAR
8. FIN SI
9. PARA i DESDE n - 1 HASTA posicion PASO -1 HACER   ' desplazamiento a la derecha
10.    lista[i + 1] <- lista[i]
11. FIN PARA
12. lista[posicion] <- valor
13. n <- n + 1
14. REPORTAR lista
FIN ALGORITMO
```

**Explicación paso a paso:** primero se valida que haya espacio (capacidad 10) y que la posición sea válida; después se desplazan hacia la derecha todos los elementos desde la última posición hasta la pedida; finalmente se coloca el valor en el lugar indicado y el tamaño aumenta en 1. Si no hay espacio, el algoritmo responde «vector lleno» (la estructura es estática y no redimensiona).

### 2.4 Ordenamiento de menor a mayor y su costo

Se propone el **ordenamiento burbuja con bandera** (mejora clásica del burbuja):

```pseudocode
ALGORITMO OrdenarBurbuja(lista, n)
1. intercambiado <- VERDADERO
2. pasada <- 1
3. MIENTRAS intercambiado Y pasada < n HACER
4.    intercambiado <- FALSO
5.    PARA i DESDE 0 HASTA n - pasada - 1 HACER
6.       SI lista[i] > lista[i + 1] ENTONCES
7.          INTERCAMBIAR lista[i], lista[i + 1]
8.          intercambiado <- VERDADERO
9.       FIN SI
10.    FIN PARA
11.    pasada <- pasada + 1
12. FIN MIENTRAS
13. REPORTAR lista
FIN ALGORITMO
```

**Resultado con el vector del caso:**

```
Antes:  [28, 15, 34, 21, 19, 40, 12, 26]
Después: [12, 15, 19, 21, 26, 28, 34, 40]
```

**Costo aproximado (explicado de forma sencilla):**

| Caso | Qué ocurre | Comparaciones (n = 8) | Notación |
|---|---|---|---|
| **Mejor caso** (ya ordenado) | La primera pasada no detecta ningún intercambio y la bandera detiene el ciclo | 7 | **O(n)** |
| **Peor caso** (orden inverso) | Se comparan todos los pares posibles en todas las pasadas | 28 = 8·7/2 | **O(n²)** |

En cristiano: cada pasada «hace flotar» el mayor valor hacia el final. Si la lista ya está ordenada, basta una pasada para confirmarlo (barato). Si está en orden inverso, hay que comparar y mover casi todos los pares posibles: al duplicar los datos, el costo se cuadruplica (por eso se dice «cuadrático»).

---

## Actividad 3. Matrices y recorrido completo de datos

### 3.1 Matriz propuesta para el caso (4 filas × 5 columnas)

Cada **fila = un aula**, cada **columna = un bloque horario**; el valor es la cantidad de estudiantes ocupando el aula en ese bloque.

| Aula \ Bloque | **0** (7:00) | **1** (8:00) | **2** (9:00) | **3** (10:00) | **4** (11:00) |
|---|---|---|---|---|---|
| **0 – Aula 1** | 10 | 12 | 8 | 15 | 9 |
| **1 – Aula 2** | 7 | 9 | 11 | 6 | 10 |
| **2 – Aula 3** | 12 | 8 | 14 | 9 | 7 |
| **3 – Aula 4** | 6 | 5 | 9 | 8 | 11 |

```
             Columnas (bloques horarios)
             j=0   j=1   j=2   j=3   j=4
           ┌─────┬─────┬─────┬─────┬─────┐
  i=0 (A1) │ 10  │ 12  │  8  │ 15  │  9  │
           ├─────┼─────┼─────┼─────┼─────┤
  i=1 (A2) │  7  │  9  │ 11  │  6  │ 10  │
           ├─────┼─────┼─────┼─────┼─────┤
  i=2 (A3) │ 12  │  8  │ 14  │  9  │  7  │
           ├─────┼─────┼─────┼─────┼─────┤
  i=3 (A4) │  6  │  5  │  9  │  8  │ 11  │
           └─────┴─────┴─────┴─────┴─────┘
 Filas i: 0..3 (aulas)     Columnas j: 0..4 (bloques)
```

### 3.2 Algoritmo: total de estudiantes por aula (suma de filas)

```pseudocode
ALGORITMO TotalPorAula(m, F, C)
1. PARA i DESDE 0 HASTA F - 1 HACER
2.    total <- 0
3.    PARA j DESDE 0 HASTA C - 1 HACER
4.       total <- total + m[i][j]
5.    FIN PARA
6.    REPORTAR "Aula " + i + ": " + total
7. FIN PARA
FIN ALGORITMO
```

**Resultados:** Aula 0 = **54**, Aula 1 = **43**, Aula 2 = **50**, Aula 3 = **39** (total general 186).

### 3.3 Algoritmo: total de estudiantes por horario (suma de columnas)

```pseudocode
ALGORITMO TotalPorHorario(m, F, C)
1. PARA j DESDE 0 HASTA C - 1 HACER
2.    total <- 0
3.    PARA i DESDE 0 HASTA F - 1 HACER
4.       total <- total + m[i][j]
5.    FIN PARA
6.    REPORTAR "Bloque " + j + ": " + total
7. FIN PARA
FIN ALGORITMO
```

**Resultados:** Bloque 0 = **35**, Bloque 1 = **34**, Bloque 2 = **42**, Bloque 3 = **38**, Bloque 4 = **37**.

### 3.4 Algoritmo: celda con mayor ocupación

```pseudocode
ALGORITMO CeldaMaxima(m, F, C)
1. maxValor <- m[0][0]
2. maxFila  <- 0
3. maxCol   <- 0
4. PARA i DESDE 0 HASTA F - 1 HACER
5.    PARA j DESDE 0 HASTA C - 1 HACER
6.       SI m[i][j] > maxValor ENTONCES
7.          maxValor <- m[i][j]
8.          maxFila  <- i
9.          maxCol   <- j
10.       FIN SI
11.    FIN PARA
12. FIN PARA
13. REPORTAR maxValor, maxFila, maxCol
FIN ALGORITMO
```

**Resultado:** mayor ocupación = **15** en la celda **(fila 0, columna 3)** → Aula 1, bloque 10:00.

### 3.5 Por qué esta actividad requiere recorrer varias posiciones

- Los datos están **distribuidos en todas las celdas**: no existe una sola casilla que responda «¿quién tiene más ocupación?» ni «¿cuántos hay por bloque?»; la respuesta es **la suma o comparación de todos los valores**.
- Totales por aula: cada fila tiene 5 valores ⇒ hay que visitar las 4×5 = **20 celdas**.
- Totales por horario: cada columna se construye con 4 valores de filas distintas ⇒ de nuevo hay que cruzar todas las filas.
- Celda máxima: en el peor caso el máximo puede estar en **cualquier** posición, así que hay que comparar las 20 celdas.
- Costo: siempre **O(F × C)** = O(4 × 5) = O(20) ⇒ es un recorrido **completo** (por eso se llama «recorrer toda la matriz»). Con doble ciclo `PARA fila` / `PARA columna` se garantiza que ninguna posición quede sin visitar.

---

## Actividad 4. Matrices especiales y decisión técnica

### 4.1 ¿Qué es una matriz cuadrada?

Es la matriz con **la misma cantidad de filas y columnas** (n × n). Ejemplo 3 × 3:

```
┌            ┐
│  5   0   3 │
│  0   8   1 │   3 filas = 3 columnas ⇒ cuadrada
│  2   0   4 │
└            ┘
```

De ella destaca la **diagonal principal**: las posiciones donde `i = j` (5, 8, 4). Es la base para conceptos como matriz identidad, triangular o simétrica.

### 4.2 ¿Qué se entiende por matriz poco densa (dispersa)?

Una matriz **poco densa o dispersa** es aquella en la que **la mayoría de las celdas contienen cero** (u otro valor «vacío»). Se mide con la **densidad**:

```
densidad = celdas distintas de cero / (filas × columnas)
```

Si la densidad es baja (por ejemplo, menor al 30 %), la matriz es poco densa.

Ejemplo con la matriz 4 × 5 del sistema, ahora registrando **coincidencias entre talleres simultáneos**:

```
┌                ┐
│  0   0   3   0   0 │
│  0   0   0   0   2 │     4 valores útiles de 20 celdas
│  5   0   0   0   0 │     densidad = 4/20 = 20 %  ⇒ poco densa
│  0   0   0   4   0 │
└                ┘
```

### 4.3 Ejemplo del caso académico en que conviene la matriz poco densa

**Situación:** la coordinación quiere registrar **en qué bloques dos talleres comparten aula al mismo tiempo**. Como casi todos los talleres usan bloques distintos, casi todas las combinaciones aula × bloque son **0**; solo unas pocas celdas tienen datos reales.

**Solución 1 – matriz completa:** guardar 4 × 5 = **20 posiciones**, de las cuales 16 son ceros.

**Solución 2 – matriz poco densa (lista de tripletas):** guardar solo los valores útiles con su fila y columna:

| Fila | Columna | Valor |
|---|---|---|
| 0 | 2 | 3 |
| 1 | 4 | 2 |
| 2 | 0 | 5 |
| 3 | 3 | 4 |

**Justificación técnica:**

1. **Memoria:** con tripletas se guardan 4 × 3 = 12 valores en lugar de 20; en matrices grandes la diferencia es enorme (una matriz 1000 × 1000 con 5 datos reales pasaría de 1 000 000 de celdas a 15 valores).
2. **Operaciones:** al recorrer solo los datos reales, búsquedas y sumas ignoran los ceros que no aportan información.
3. **Claridad:** distingue claramente «no hay coincidencia» (0 implícito) de «hay dato», evitando cálculos inútiles.
4. **Decisión técnica del equipo:** como esta relación entre talleres es **escasa por naturaleza**, se elige la representación **poco densa**; para la ocupación diaria de aulas (donde casi todas las celdas tienen estudiantes) se mantiene la **matriz completa**, porque allí sí hay datos en casi todas las posiciones.

---

## Conclusiones

1. Las estructuras **estáticas** (vector y matriz) son la elección adecuada para la primera etapa: tamaño conocido, acceso directo por índice y análisis de eficiencia sencillo.
2. Sobre el vector se resolvieron los cuatro pedidos: representación con índices, búsqueda de extremos en O(n), inserción con desplazamiento y validación de capacidad, y ordenamiento burbuja con bandera en O(n) / O(n²).
3. La matriz 4 × 5 permitió calcular totales por fila (aula), totales por columna (horario) y la celda máxima mediante **recorrido completo** O(F × C).
4. La **densidad** es el criterio técnico para elegir entre matriz completa y poco densa: se usa la dispersa cuando la mayoría de las celdas son cero.

> **Video de exposición:** agregar aquí el enlace de YouTube (se sube como «no listado», con cámaras prendidas de todos los integrantes).

# WILMER JAMENER GUEVARA RAMOS
# JAVIER ALONSO GALLEGOS RODRIGUEZ
# JOSEP ANTONIO FONG MILONES 
# MARCO YCHUTA SALDIVAR 
# GENESIS PALOMA LUCIA CHUQUI ALLCA
> **Integrantes:** completar los nombres en `README.md`.
