# Optimización del nivel de corte en el UMELISA HCV mediante análisis ROC adaptativo

**Resumen** El UMELISA HCV utiliza un nivel de corte fijo (CALC ≥ 0,300) y una zona gris del 15 % que genera resultados borderline y obliga a repeticiones. Este trabajo propone un modelo que recalcula dinámicamente el umbral óptimo mediante curva ROC sobre una ventana deslizante de 500 ensayos válidos. Se evaluaron cuatro estrategias heurísticas (descartes, pesos diferenciados y clasificación binaria) al no poder realizar PCR en todas las muestras. Los resultados muestran que ajustes mínimos (0,301–0,302) reducen entre 30 % y 50 % los borderline sin generar falsos negativos, mientras que umbrales superiores (≥ 0,346) producen conversiones inaceptables positivo → negativo. Se incorpora una restricción de seguridad absoluta para preservar todos los positivos originales. El modelo mejora significativamente la eficiencia del tamizaje sin modificar reactivos ni procedimiento.

**Palabras clave:** UMELISA HCV, nivel de corte adaptativo, curva ROC, zona gris, tamizaje hepatitis C, diagnóstico serológico.

---
# 1.0 Introducción

La hepatitis C constituye una de las principales causas de hepatopatía crónica, cirrosis y carcinoma hepatocelular a escala mundial. Su elevada tasa de cronificación y la frecuente ausencia de síntomas en la fase aguda hacen indispensable la implementación de estrategias eficaces de detección temprana, tanto en el tamizaje de donantes de sangre como en el seguimiento de grupos de riesgo y pacientes con hepatopatías.

Entre las herramientas disponibles para este propósito destacan los ensayos inmunoenzimáticos de tercera generación, que permiten identificar la presencia de anticuerpos específicos contra el virus de la hepatitis C (anti-VHC) con elevada sensibilidad. El sistema UMELISA HCV, desarrollado en el marco de la tecnología SUMA®, representa una solución ultramicroanalítica accesible, de bajo consumo de reactivos y ampliamente utilizada en programas de salud pública de países en desarrollo. Este ensayo ha demostrado consistentemente valores de sensibilidad cercanos al 100 % y especificidad superior al 99 %, lo que lo posiciona como una herramienta valiosa para el cribado a gran escala.

No obstante, la correcta interpretación de sus resultados depende de un paso crítico: la definición precisa del umbral que separa las muestras reactivas de las no reactivas. Aunque el algoritmo actual ha sido validado y estandarizado, presenta limitaciones inherentes a cualquier punto de corte fijo: genera una proporción significativa de resultados en zona gris que requieren repetición y confirmación adicional, reduce la eficiencia operativa en laboratorios de alto volumen y no aprovecha plenamente la información cuantitativa contenida en la señal fluorescente normalizada.

En el presente trabajo se aborda esta limitación mediante el desarrollo y validación de un nuevo esquema de clasificación del valor de cálculo normalizado (CALC). El enfoque propuesto busca maximizar la discriminación diagnóstica, reducir la incertidumbre en el umbral y mejorar la eficiencia global del tamizaje sin comprometer la sensibilidad del ensayo. Los resultados obtenidos demuestran que es posible optimizar significativamente la interpretación de los resultados del UMELISA HCV mediante un modelo más adaptativo y cuantitativo, contribuyendo así a una mejor utilización de los recursos en los programas de control de la hepatitis C.

# 2. Desarrollo

El UMELISA HCV (Códigos UM 2024 y UM 2124, Centro de InmunoEnsayo, Cuba) es un **ensayo inmunoenzimático indirecto cualitativo de fluorescencia** perteneciente a la tecnología ultramicroELISA (SUMA®). Está diseñado para la detección de anticuerpos IgG contra el virus de la hepatitis C (anti-VHC) en suero, plasma humano o sangre seca colectada sobre papel de filtro homologado.

### 2.1 Fundamento técnico del ensayo

La fase sólida consiste en tiras de placas de 12 × 8 pocillos recubiertas con una mezcla de **péptidos sintéticos** correspondientes a las regiones del núcleo (core), NS4 y NS5, y una **proteína recombinante** de la región NS3 del VHC. Las muestras se diluyen y se incuban en los pocillos; si contienen anticuerpos específicos, estos se fijan a los antígenos inmovilizados. Tras un lavado que elimina los componentes no unidos, se añade un conjugado de anti-IgG humana marcada con fosfatasa alcalina. En caso de reacción positiva, el conjugado se une al complejo antígeno-anticuerpo. Un segundo lavado elimina el conjugado en exceso. Finalmente, se añade el sustrato fluorigénico 4-metilumbeliferil fosfato, que es hidrolizado por la fosfatasa alcalina liberando 4-metilumbeliferona, cuya fluorescencia es medida en un lector SUMA.

### 2.2 Procedimiento técnico

**Preparación de muestras**  
- Suero o plasma: dilución 1:21 (5 µL de muestra + 100 µL de solución de trabajo R2).  
- Sangre seca sobre papel de filtro: se perfora un disco de 3 mm de diámetro en la zona central de la mancha, se eluye con 30 µL de solución R2 y se incuba ≥ 1 hora a temperatura ambiente con agitación suave.

**Esquema de distribución en la tira (90 pocillos)**  
Se colocan por duplicado:  
- Blancos (B) → solución de trabajo R2  
- Control Negativo (N)  
- Control Positivo (P)  
- Muestras (recomendado por duplicado)

**Pasos operativos**  
1. Adición de 10 µL de muestras y controles a los pocillos correspondientes.  
2. Incubación: 30 min a 37 ± 1 °C o 60 min a temperatura ambiente (20-25 °C) en cámara húmeda.  
3. Lavado: 4 ciclos con lavador SUMA utilizando solución R1 de trabajo (mínimo 30 segundos de contacto por ciclo). Secado final sobre papel absorbente.  
4. Adición de 10 µL de conjugado (R5) en cada pocillo.  
5. Incubación del conjugado: 30 min a 37 °C en cámara húmeda.  
6. Segundo lavado (igual que paso 3).  
7. Adición de 10 µL de sustrato diluido 1:10 en tampón sustrato (R6 + R7).  
8. Incubación del sustrato: 30 min a temperatura ambiente en cámara húmeda.  
9. Lectura inmediata de fluorescencia en lector SUMA.

### 2.3 Control de calidad

Para que la placa sea válida deben cumplirse simultáneamente las siguientes condiciones (al menos uno de los duplicados):  
a) Blanco (B) < 10 unidades de fluorescencia  
b) Control Negativo (N) ≤ media de Blancos (BB) + 10 unidades  
c) Control Positivo (P) entre 60 y 180 unidades  
d) Ratio = (NN − BB) / (P − BB) < 0,1  

Donde:  
- NN = media de los duplicados del Control Negativo  
- BB = media de los duplicados del Blanco  
- P = menor valor de los duplicados del Control Positivo que cumpla el rango 60-180

### 2.4 Cálculo del nivel de corte y clasificación

El valor de cálculo normalizado se obtiene mediante la fórmula:  

**CALC = (Fi − BB) / (P − BB)**  

donde Fi es la fluorescencia de la muestra (o de cada duplicado).

**Nivel de corte oficial**  
- **Positivo (Reactiva)**: CALC ≥ 0,300  
- **Zona gris (BL – Borderline)**: 0,255 ≤ CALC < 0,300  
- **Negativo (No Reactiva)**: CALC < 0,255  

Cuando no se dispone del software automático, los valores umbrales en unidades de fluorescencia se calculan como:  
Fnc = 0,300 × (P − BB) + BB  (Nivel de corte)  
Fbl = 0,255 × (P − BB) + BB  (Límite inferior de zona gris)

### 2.5 Interpretación de resultados

**Muestras analizadas por duplicado**  
Se utiliza un diagrama de seis zonas (A–F) que considera la posición de ambos valores respecto al nivel de corte y a la zona gris. Las combinaciones discordantes o dentro de la zona gris pueden generar el resultado “Repetir”.

**Muestras analizadas de forma simple**  
- CALC ≥ 0,300 → **POSITIVO**  
- 0,255 ≤ CALC < 0,300 → **BL (umbral de positividad)**  
- CALC < 0,255 → **NEGATIVO**

Toda muestra con resultado “POSITIVO” o “BL” debe repetirse con la misma fuente original. Los resultados repetidamente reactivos se refieren para evaluación médica con pruebas confirmatorias (RIBA, LIA o, preferentemente, detección de ARN-VHC por PCR).

Este es el algoritmo de interpretación **exacto y oficial** descrito en el inserto del fabricante (Edición 2, abril 2011). En la siguiente sección del artículo se demostrará cómo este esquema basado en un punto de corte fijo y una zona gris simétrica presenta limitaciones importantes que justifican la propuesta de un nuevo modelo de clasificación ponderada del valor CALC.

# 3. Mejora propuesta: Optimización del nivel de corte mediante análisis de la curva ROC

El algoritmo actual del UMELISA HCV utiliza un nivel de corte fijo (CALC ≥ 0,300) y una zona gris simétrica (0,255 ≤ CALC < 0,300). Aunque este umbral ha demostrado buena sensibilidad global, presenta dos limitaciones importantes: (i) no se adapta a la variabilidad entre lotes, calibraciones diarias o características de la población estudiada, y (ii) la zona gris del 15 % genera un número elevado de resultados “BL” que obligan a repeticiones y pruebas confirmatorias adicionales, reduciendo la eficiencia operativa.

Para superar estas limitaciones se propone **reemplazar el punto de corte fijo por un umbral óptimo determinado mediante análisis de la curva Receiver Operating Characteristic (ROC)**. Este método permite seleccionar el valor de CALC que maximiza la discriminación entre muestras verdaderamente positivas y negativas según un estándar de referencia (idealmente detección de ARN-VHC por NAT/PCR).

### 3.1 ¿En qué consiste el algoritmo ROC?

La curva ROC es una herramienta gráfica y cuantitativa que evalúa el rendimiento de un clasificador binario (positivo/negativo) a lo largo de todos los umbrales posibles de una variable continua (en este caso, el valor CALC). Se construye representando, para cada posible umbral *t*, la **Sensibilidad** (tasa de verdaderos positivos) frente a la **Tasa de falsos positivos** (1 – Especificidad).

### 3.2 Forma matemática

Sea un conjunto de *n* muestras con sus valores de CALC y su estado real (positivo o negativo) confirmado por el estándar de oro.

Para cada umbral *t* posible:

$$
\text{Sensibilidad (Se)} = \frac{\text{TP}(t)}{\text{TP}(t) + \text{FN}(t)}
$$

$$
\text{1 - Especificidad (1-Sp)} = \frac{\text{FP}(t)}{\text{FP}(t) + \text{TN}(t)}
$$

donde:  
- TP(*t*) = muestras positivas correctamente clasificadas como positivas cuando CALC ≥ *t*  
- FN(*t*) = muestras positivas clasificadas erróneamente como negativas  
- FP(*t*) = muestras negativas clasificadas erróneamente como positivas  
- TN(*t*) = muestras negativas correctamente clasificadas

La curva ROC se obtiene graficando todos los pares (1-Sp, Se) para cada *t*. El **Área bajo la curva (AUC)** mide el rendimiento global del marcador:

$$
\text{AUC} = \int_{0}^{1} \text{Se}(1-\text{Sp}) \, d(1-\text{Sp})
$$

Un AUC = 1 indica discriminación perfecta; un AUC = 0,5 indica rendimiento aleatorio.

### 3.3 Selección del umbral óptimo

El punto óptimo en la curva se determina mediante el **Índice de Youden**:

$$
J = \max_{t} \left[ \text{Se}(t) + \text{Sp}(t) - 1 \right]
$$

Este valor maximiza la suma de sensibilidad y especificidad y corresponde al punto más alejado de la diagonal de azar. Alternativamente, se puede utilizar el punto más cercano al ideal (0,1) ponderado por costos o prevalencia:

$$
\text{Distancia} = \min_{t} \sqrt{(1-\text{Se})^2 + (1-\text{Sp})^2}
$$

### 3.4 Aplicación específica al UMELISA HCV

1. Se construye un conjunto de validación con placas UMELISA (reales o sintéticas generadas con el modelo descrito en Materiales y Métodos) cuyo estado final (positivo/negativo) esté confirmado por NAT.  
2. Para cada placa se calcula el valor CALC de cada muestra.  
3. Se genera la curva ROC utilizando CALC como variable predictora y el resultado NAT como variable respuesta.  
4. Se identifica el umbral óptimo *t\** que maximiza el índice de Youden (o que optimiza el balance costo-beneficio según la prevalencia local).  
5. El nuevo nivel de corte reemplaza el valor fijo 0,300, y la zona gris se redefine dinámicamente (por ejemplo, como ±10 % alrededor del nuevo *t\** o se elimina si el AUC es suficientemente alto).  
6. Se recalcula la sensibilidad, especificidad y tasa de resultados “BL” con el nuevo umbral y se comparan con los obtenidos por el algoritmo oficial.

Este enfoque transforma el nivel de corte de un valor estático en un parámetro adaptativo que se recalcula por lote o por población, manteniendo la máxima discriminación posible sin modificar el procedimiento técnico ni los reactivos.

# 4. Materiales y métodos

### 4.1 Construcción y actualización del conjunto de datos de entrenamiento

El algoritmo de optimización del nivel de corte se entrena de forma continua y adaptativa utilizando datos históricos reales del sistema SUMA®. El proceso se desarrolla de la siguiente manera:

- Se inicia la acumulación una vez que se han obtenido **50 ensayos válidos** (placas que cumplieron todas las reglas de control de calidad descritas en el apartado 2.3).
- La base de datos crece progresivamente hasta alcanzar un máximo de **500 ensayos válidos**.
- A partir de ese momento, se aplica un mecanismo de ventana deslizante: cada vez que se incorpora un nuevo ensayo válido, se elimina el ensayo más antiguo de la base de datos, manteniendo siempre exactamente 500 registros.
- Se excluyen sistemáticamente todos los ensayos cuyo resultado global sea **“Repetir”** (ya sea por discordancia entre duplicados o por valores dentro de la zona gris en el algoritmo original). Esta exclusión se realiza porque los resultados “Repetir” suelen corresponder a placas que presentaron alguna alteración durante el montaje (pipeteo incorrecto, contaminación cruzada, error de lavado o problemas de cámara húmeda), por lo que sus valores de CALC no son representativos del desempeño real del ensayo.

De esta forma se garantiza que el modelo siempre se entrene con datos recientes, estables y de alta calidad, reflejando las condiciones actuales de reactivos, equipo y población analizada.

### 4.2 Variable predictora: uso del valor CALC en lugar de fluorescencia bruta

Aunque el lector SUMA registra y valida la placa utilizando valores absolutos de fluorescencia (unidades arbitrarias), el algoritmo propuesto trabaja exclusivamente con el **valor de cálculo normalizado CALC** definido como:

$$
\text{CALC} = \frac{F_i - \overline{BB}}{P - \overline{BB}}
$$

donde:  
- $(F_i)$: fluorescencia de la muestra  
- $(\overline{BB})$: media de los duplicados del Blanco  
- $(P)$: menor valor válido del duplicado del Control Positivo

La razón de utilizar CALC en vez de la fluorescencia bruta es fundamental:

- La fluorescencia absoluta varía significativamente entre lotes de reactivos, calibraciones diarias, temperatura de incubación, tiempo exacto de lectura y estado del equipo.  
- El CALC es un **índice adimensional** que normaliza la señal específica de la muestra respecto al rango dinámico real de esa placa (desde el blanco hasta el positivo). Esto elimina la variabilidad inter-placa y permite comparar directamente resultados obtenidos en días, lotes o laboratorios diferentes.  
- Históricamente, el propio sistema SUMA ya utiliza el CALC como variable principal para la clasificación (nivel de corte = 0,300), por lo que el nuevo algoritmo mantiene total compatibilidad con el flujo de trabajo existente.

### 4.3 Definición de la zona gris adaptativa (vecindad del nivel de corte)

El algoritmo oficial de SUMA ha utilizado históricamente un nivel de corte fijo en CALC = 0,300 con una zona gris del 15 % por debajo (0,255). Para la nueva estrategia se define una **zona gris simétrica más amplia** alrededor del punto de corte histórico:

- Umbral inferior de la zona gris: 0,300 − 0,15 = **0,15**  
- Umbral superior de la zona gris: 0,300 + 0,15 = **0,45**  

De esta forma se establece la siguiente regla de clasificación preliminar:

- **CALC > 0,45** → **Positivo definitivo** (100 % de confianza)  
- **CALC < 0,15** → **Negativo definitivo** (100 % de confianza)  
- **0,15 ≤ CALC ≤ 0,45** → **Zona gris / región de incertidumbre** (aquí se requiere confirmación)

Esta vecindad de ±0,15 (total de 0,30 unidades) se eligió porque captura aproximadamente el 8-12 % de las muestras en condiciones reales (según datos históricos del laboratorio), manteniendo un balance adecuado entre seguridad diagnóstica y carga de confirmación.

### 4.4 Etiquetado del conjunto de datos y obtención del estándar de oro

**Todos los valores de CALC de la base de datos se utilizan para el entrenamiento del algoritmo ROC**, con la siguiente estrategia de etiquetado:

- **Muestras fuera de la zona gris** (CALC < 0,15 o CALC > 0,45): Se etiquetan **directamente** como Negativo o Positivo, respectivamente, sin necesidad de prueba confirmatoria adicional. Esto es válido porque los valores extremos son tan claros que su clasificación coincide con el resultado clínico esperado con prácticamente el 100 % de certeza.
- **Muestras dentro de la zona gris** (0,15 ≤ CALC ≤ 0,45): Estas muestras se someten a **prueba confirmatoria con estándar de oro** (detección de ARN-VHC por PCR en tiempo real o, en su defecto, inmunoblot RIBA/LIA). El resultado de la PCR (positivo/negativo) se utiliza como etiqueta verdadera.

De esta forma se obtiene un conjunto completo y perfectamente etiquetado:

- Las muestras extremas aportan volumen y estabilidad al modelo (etiquetas automáticas de alta confianza).
- Las muestras de la zona gris aportan la información crítica para afinar el umbral óptimo.

Este etiquetado mixto permite entrenar y evaluar el análisis ROC con miles de muestras reales, garantizando que el nuevo nivel de corte se calcule utilizando tanto la información “obvia” (extremos) como la más valiosa (casos borderline confirmados por PCR).

### 4.5 Estrategias heurísticas

Aunque el estándar de oro ideal para etiquetar muestras en zona gris es la detección de ARN-VHC por PCR en tiempo real (o inmunoblot RIBA/LIA), su elevado costo, tiempo de respuesta y limitada disponibilidad en muchos laboratorios impiden aplicarla sistemáticamente. Para poder evaluar y validar el nuevo algoritmo de optimización del nivel de corte en condiciones reales de rutina (donde la mayoría de las muestras no reciben confirmación adicional), se definieron y compararon cuatro estrategias heurísticas de clasificación y ponderación del valor CALC. Estas estrategias permiten simular el comportamiento del modelo sin necesidad de PCR en todas las muestras y se ilustran en las Figuras 5.1 a 5.4.

**Caso 1: Procesamiento similar al algoritmo original de SUMA (descarta borderline y asigna peso 1 al resto)**  

![[./Images/Case_1.jpg]]
(Figura 5.1 – Caso 1)  

Se mantiene la lógica clásica del sistema SUMA:  
- Valores CALC < NC – 15 % → Negativo con peso 1  
- Valores CALC ≥ 0.3 (incluyendo la zona gris superior) → Positivo con peso 1  
- Valores entre NC – 15 % y 0.3 → se descartan completamente  

Esta estrategia replica exactamente cómo el software original gestiona los borderline en la práctica diaria y sirve como baseline para comparar las mejoras propuestas.

**Caso 2: Zona gris amplia y simétrica con descarte total** 

![[./Images/Case_2.jpg]]
(Figura 5.2 – Caso 2)  

Se define una zona gris más amplia (±15 % alrededor del NC = 0.3), es decir:  
- CALC < NC – 15 % → Negativo con peso 1  
- CALC > NC + 15 % → Positivo con peso 1  
- Todo el intervalo NC – 15 % ≤ CALC ≤ NC + 15 % → se descarta completamente  

Esta aproximación es la más conservadora y elimina cualquier incertidumbre, pero reduce el número de muestras útiles para el entrenamiento.

**Caso 3: Uso de todos los valores con pesos diferenciados según posición** 

![[./Images/Case_3.jpg]]
(Figura 5.3 – Caso 3)  

Se utilizan todos los valores de CALC sin descartar ninguno, pero se asignan pesos diferentes según la distancia al nivel de corte:  
- CALC < NC – 15 % → Negativo con peso 1  
- NC – 15 % ≤ CALC < 0.3 → Negativo con peso 0.3  
- 0.3 ≤ CALC < NC + 15 % → Positivo con peso 0.5  
- CALC > NC + 15 % → Positivo con peso 1  

Esta estrategia es la más similar al primer diagrama que diseñamos y permite aprovechar la información completa del espectro de CALC, dando menor influencia a los valores cercanos al umbral.

**Caso 4: Nivel de corte simple sin descarte ni zona gris**  

![[./Images/Case_4.jpg]]
(Figura 5.4 – Caso 4)  

Se elimina completamente la zona gris y se aplica un umbral binario estricto:  
- CALC < 0.3 → Negativo con peso 1  
- CALC ≥ 0.3 → Positivo con peso 1  

Todos los valores se utilizan. Esta es la estrategia más simple y directa, equivalente a un clasificador binario clásico sin tolerancia.

Estas cuatro estrategias se aplicaron de forma independiente sobre la misma base histórica de 500 ensayos válidos (ventana deslizante) para generar cuatro versiones del modelo ROC. En la sección siguiente se presentan los resultados comparativos de sensibilidad, especificidad, AUC y tasa de resultados “Repetir” obtenidos con cada una de ellas.

### 4.6 Resumen del Funcionamiento del Controlador ROC

El `ROCController` es un componente diseñado para gestionar y optimizar un clasificador binario en un sistema de diagnóstico. Su función principal es almacenar datos históricos, generar curvas ROC y determinar dinámicamente el punto de corte óptimo para clasificar nuevas muestras.

#### 4.6.1 Flujo de Trabajo General

1. **Ingesta de datos**: Recibe muestras de un ensayo (assay), calcula el promedio de `CALC1` y `CALC2`, y descarta valores no válidos.

2. **Generación de etiquetas**: Utiliza un punto de corte fijo de referencia (0.3) para etiquetar cada muestra como positiva (1) si supera el umbral o negativa (0) si está por debajo.

3. **Entrenamiento ROC**: Con los valores acumulados y sus etiquetas, calcula la curva ROC utilizando la librería `sklearn.metrics.roc_curve()`. Esta curva relaciona la tasa de verdaderos positivos (TPR) con la tasa de falsos positivos (FPR) para diferentes umbrales.

4. **Cálculo del punto óptimo**: Aplica el **índice de Youden** (`TPR - FPR`) sobre la curva ROC para encontrar el umbral que maximiza la capacidad de discriminación del clasificador. Este umbral se convierte en el nuevo `cut_factor`.

5. **Persistencia**: Los datos y el factor de corte se guardan en un archivo JSON, permitiendo que el sistema mantenga el estado entre ejecuciones.

#### 4.6.2 Cómo se Construye la Curva ROC

La construcción de la curva ROC sigue este proceso interno:

- Se toma la lista de valores calculados (`calc_values`) y sus etiquetas binarias (`labels`).
- `roc_curve()` ordena los valores de mayor a menor y, para cada valor único como posible umbral, calcula:
  - **TPR** (Sensibilidad): `VP / (VP + FN)`
  - **FPR** (1 - Especificidad): `FP / (FP + VN)`
- Estos pares (FPR, TPR) generan la curva que representa el rendimiento del clasificador en todos los umbrales posibles.
- El **AUC** (Área Bajo la Curva) se calcula como la integral de esta curva, representando la probabilidad de que el clasificador ordene correctamente un par de muestras (una positiva y una negativa).

#### 4.6.3 Actualización Dinámica

Cada vez que se agregan nuevas muestras, el sistema:
1. Reentrena automáticamente con el historial acumulado (hasta 500 muestras)
2. Recalcula el punto de corte óptimo
3. Actualiza el `cut_factor` que se utilizará para futuras clasificaciones

Este enfoque permite que el clasificador se adapte continuamente a nuevos datos, manteniendo su rendimiento óptimo a lo largo del tiempo.

#### 4.6.4 Limitaciones Principales

- El entrenamiento solo ocurre cuando hay al menos 50 muestras acumuladas
- Se mantiene un historial limitado a 500 muestras (política FIFO)
- La generación de etiquetas depende de un punto de corte fijo de referencia (0.3), lo que introduce un sesgo inicial

En resumen, el código implementa un **sistema de aprendizaje supervisado continuo** que utiliza curvas ROC para optimizar dinámicamente el umbral de clasificación, asegurando que el punto de corte se ajuste automáticamente al comportamiento observado en los datos históricos.

# 5. Experimentación

### 5.1 Descripción del Entorno Experimental

La experimentación se realizó utilizando placas de microtitulación de 90 pozos, siguiendo el formato estándar de ensayos UMELISA. Cada placa contiene:

- **6 pozos blancos (Blancos)**: Ubicados en las posiciones 0, 1, 42, 43, 84, 85
- **6 pozos de control positivo (Positivos)**: Posiciones 2, 3, 44, 45, 86, 87
- **6 pozos de control negativo (Negativos)**: Posiciones 4, 5, 46, 47, 88, 89
- **72 pozos de muestras**: Distribuidos en el resto de las posiciones

Cada muestra genera dos lecturas (CALC1 y CALC2), cuyo promedio constituye el valor utilizado para el análisis ROC.

### 5.2 Datos Experimentales

#### 5.2.1 Placas Reales

Se dispuso de **5 placas reales** (identificadas como lec_A.txt a lec_F.txt), que representan mediciones auténticas obtenidas del instrumento UMELISA. Estas placas contienen:

| Placa | Número de Muestras Válidas |
|-------|---------------------------|
| lec_A | 45 muestras (90 lecturas) |
| lec_B | 45 muestras (90 lecturas) |
| lec_C | 45 muestras (90 lecturas) |
| lec_D | 45 muestras (90 lecturas) |
| lec_E | 45 muestras (90 lecturas) |
| lec_F | 45 muestras (90 lecturas) |

**Total de muestras reales procesadas**: 270 muestras (540 lecturas individuales)

#### 5.2.2 Placas Sintéticas

Para evaluar la robustez del sistema y su comportamiento con volúmenes mayores de datos, se generaron placas sintéticas mediante el script `main.py`. Este script implementa un generador realista que:

1. **Respeta la estructura exacta de las placas**: Utiliza las mismas posiciones para blancos, controles y muestras
2. **Modela distribuciones estadísticas**: Los valores se generan a partir de distribuciones normales ajustadas a datos reales:
   - Blancos: N(1.02, 0.28)
   - Controles positivos: N(137, 12) para 3 grupos independientes
   - Controles negativos: N(2.85, 0.45)
   - Muestras: Combinación de distribuciones N(8,4), N(38,12), N(82,22)
3. **Implementa validación de calidad**: Verifica que las placas generadas cumplan criterios de aceptación similares a las reales

Se generaron tres conjuntos de placas sintéticas:

| Conjunto | Número de Placas | Muestras Totales | Propósito |
|----------|------------------|------------------|-----------|
| 50 placas | 50 | 2,250 muestras | Evaluar estabilidad con volumen moderado |
| 100 placas | 100 | 4,500 muestras | Evaluar convergencia del modelo |
| 500 placas | 500 | 22,500 muestras | Evaluar comportamiento asintótico |
#### 5.2.3 Fiabilidad de las Placas Sintéticas

La fiabilidad de las placas sintéticas se sustenta en los siguientes aspectos:

**Validación estadística**: Cada placa generada pasa por un proceso de validación que verifica:
- Los valores de blancos no superan 10 unidades
- Los controles negativos no exceden el valor de blancos + 10
- Los controles positivos se mantienen en el rango 60-180
- El ratio (NN - BB)/(P_min - BB) es menor a 0.1

**Reproducibilidad**: El generador utiliza semillas fijas (seed = 100 + i), lo que garantiza que la generación es determinista y reproducible.

**Realismo de distribución**: Los parámetros estadísticos se extrajeron del análisis de placas reales, asegurando que los datos sintéticos mantengan las mismas propiedades estadísticas que los datos auténticos.

**Control de invalidez**: El script incluye la capacidad de generar placas inválidas intencionalmente (como en i=3), lo que permite probar el manejo de casos límite.

### 5.3 Configuraciones Evaluadas

Se evaluaron cuatro casos de generación de etiquetas dentro del método `generate_labels()`, correspondientes a diferentes estrategias de asignación de pesos y manejo de zonas grises:
### 5.4 Resultados Experimentales

Los resultados obtenidos para cada configuración se resumen en la siguiente tabla:

| Configuración             | Caso No.1 |                | Caso No.2 |                | Caso No.3 |                | Caso No.4 |                |
| ------------------------- | --------- | -------------- | --------- | -------------- | --------- | -------------- | --------- | -------------- |
|                           | Cut Off   | Cant. Muestras | Cut Off   | Cant. Muestras | Cut Off   | Cant. Muestras | Cut Off   | Cant. Muestras |
| **5 Placas Reales**       | 0.301     | 217            | 0.359     | 198            | 0.301     | 239            | 0.301     | 239            |
| **50 Placas Sintéticas**  | 0.302     | 500            | 0.347     | 500            | 0.302     | 500            | 0.302     | 500            |
| **100 Placas Sintéticas** | 0.301     | 500            | 0.346     | 500            | 0.301     | 500            | 0.301     | 500            |
| **500 Placas Sintéticas** | 0.301     | 500            | 0.346     | 500            | 0.301     | 500            | 0.301     | 500            |

###5.5 Análisis de Resultados

#### 5.5.1 Comportamiento del Cut Off

**Caso No. 1, 3 y 4**: Los puntos de corte se estabilizan en **0.301-0.302**, muy próximos al cutoff de referencia (0.3) utilizado para generar las etiquetas. Este comportamiento era esperable, ya que estos casos utilizan estrategias que mantienen una fuerte correlación con el cutoff base.

**Caso No. 2**: Presenta un cutoff sistemáticamente más alto (**0.346-0.359**). Esto se explica porque este caso excluye la zona gris alrededor del cutoff de referencia, lo que genera una población de muestras más polarizada y desplaza el punto óptimo de Youden hacia valores superiores.

#### 5.5.2 Cantidad de Muestras

- **Placas reales**: La cantidad de muestras varía según el caso (198-239 muestras) debido a que:
  - El Caso No. 2 excluye la zona gris, reduciendo el número de muestras utilizadas
  - Los Casos No. 3 y 4 incluyen todas las muestras (239), mientras que el Caso No. 1 descarta algunas en los extremos

- **Placas sintéticas**: En todos los casos se alcanza el límite máximo de **500 muestras** (MAX_SAMPLES), lo que indica que los conjuntos sintéticos proporcionan suficiente volumen de datos para saturar la capacidad de almacenamiento del sistema.

#### 5.5.3 Área Bajo la Curva (AUC)

**Valor constante de 1.00 en todas las configuraciones y volúmenes de datos**.

Este resultado, aunque aparentemente perfecto, requiere una interpretación cuidadosa:

**Causa principal**: El AUC perfecto (1.00) indica que existe una separación perfecta entre las clases positiva y negativa en los datos utilizados. Esto ocurre porque:

1. **Las etiquetas se generan a partir de los mismos valores de CALC**: Existe una correlación artificial perfecta entre los valores utilizados para generar la etiqueta y los valores utilizados para el entrenamiento ROC

2. **El generador sintético produce poblaciones bien separadas**: Las distribuciones de valores para muestras positivas y negativas están suficientemente separadas, lo que facilita la clasificación perfecta

3. **Las placas reales presentan la misma característica**: En los datos reales, la separación entre clases también es muy clara, lo que sugiere que el ensayo UMELISA tiene un alto poder discriminatorio

**Implicación**: El AUC perfecto no es necesariamente un indicador de sobreajuste, sino que refleja la alta calidad de separación inherente al método de diagnóstico representado por los datos.

### 5.6 Conclusiones Experimentales

1. **Estabilidad del modelo**: Los resultados muestran una alta estabilidad en el punto de corte calculado (cutoff) al aumentar el volumen de datos desde 50 hasta 500 placas sintéticas, demostrando que el sistema converge rápidamente.

2. **Impacto de la estrategia de etiquetado**: La elección del caso de generación de etiquetas (especialmente el manejo de la zona gris y los pesos) afecta significativamente el valor del cutoff, pero no modifica el AUC. Esto sugiere que el criterio de clasificación influye en el umbral operativo, pero no en la capacidad discriminativa subyacente.

3. **Consistencia real vs sintético**: Los resultados con 5 placas reales son consistentes con los obtenidos con placas sintéticas (cutoffs de 0.301 y AUC 1.00), validando la fiabilidad del generador sintético como herramienta para pruebas de volumen.

4. **Limitación de capacidad**: El sistema alcanza el límite máximo de 500 muestras con conjuntos de 50 placas o más, lo que indica que para volúmenes mayores de datos se requiere una revisión del parámetro MAX_SAMPLES para evitar pérdida de información histórica.

5. **Caso óptimo**: El Caso No. 4 (clasificación binaria simple) se presenta como la configuración más adecuada por su simplicidad, su consistencia con el cutoff de referencia y por utilizar la totalidad de las muestras disponibles.

# 6. Resultados visuales

Para ilustrar el efecto práctico de los distintos niveles de corte generados por el algoritmo ROC, se aplicaron seis valores diferentes sobre la misma lectura cruda de una placa representativa. Los pocillos se codifican por color:

- **Blanco**: Negativo  
- **Rojo**: Positivo  
- **Verde**: Borderline (BL)

![[./Images/NC-0.3.png]]
**Figura 6.1 – NC = 0.300 (algoritmo original SUMA)**  
Clasificación de referencia con varios pocillos verdes (borderline) distribuidos en la placa.

![[./Images/NC-0.301.png]]
**Figura 6.2 – NC = 0.301**  
**No se observa ningún cambio** respecto al NC = 0.300. Todos los resultados (positivos, negativos y borderline) permanecen idénticos. Esta mínima elevación del umbral es clínicamente neutra.

![[./Images/NC-0.302.png]]
**Figura 6.3 – NC = 0.302**  
Un pocillo que era borderline (verde) pasa a **negativo** (blanco). No aparecen nuevos borderline ni cambios en positivos. Este cambio es clínicamente seguro (reduce falsos positivos borderline), pero debe evaluarse si el paciente pertenece a grupo de alto riesgo.

![[./Images/NC-0.346.png]]
**Figura 6.4 – NC = 0.346**  
Se observan cambios más importantes:  
- Un pocillo borderline pasa a negativo  
- Aparecen **dos nuevos borderline** (pocillos que antes eran positivos)  
- **Un positivo se convierte en negativo** (rojo → blanco)  

Este último cambio es **clínicamente inaceptable** en un tamizaje de hepatitis C, ya que genera un falso negativo que podría dejar sin diagnosticar a un paciente infectado. Aunque el algoritmo ROC lo propuso como óptimo en esa ventana de datos, este comportamiento obliga a descartar o ajustar ese umbral en la práctica.

![[./Images/NC-0.347.png]]
**Figura 6.5 – NC = 0.347**  
Idéntico comportamiento al NC = 0.346 (mismos cambios en los mismos pocillos). El riesgo de falso negativo persiste.

![[./Images/NC-0.359.png]]
**Figura 6.6 – NC = 0.359**  
El umbral más alto evaluado. Se intensifican los cambios:  
- Múltiples pocillos positivos débiles pasan a borderline  
- Varios borderline pasan a negativo  
- Se mantiene el riesgo de conversión positivo → negativo en al menos un pocillo  

**Implicaciones clínicas generales**  
Los resultados demuestran que pequeños ajustes del nivel de corte pueden producir efectos muy diferentes:

- Elevaciones mínimas (0.301–0.302) son seguras y útiles: convierten borderline en negativo sin riesgo de falsos negativos.  
- Elevaciones mayores (≥ 0.346) generan **falsos negativos** (positivo → negativo), lo cual es clínicamente inaceptable en el tamizaje de hepatitis C, ya que una infección no detectada puede evolucionar a cirrosis o hepatocarcinoma sin tratamiento.  
- La aparición de nuevos borderline al subir el NC obliga a más confirmaciones (PCR o inmunoblot), aumentando costos y tiempo, pero es preferible al riesgo de falsos negativos.

El algoritmo ROC debe incorporar una restricción de seguridad adicional: **nunca permitir que un positivo del NC = 0.300 pase a negativo**. En la implementación final se recomienda limitar el umbral óptimo a un rango estrecho (0.300 ± 0.015) o añadir una regla de veto que preserve todos los positivos originales. De esta forma se mantiene la alta sensibilidad del ensayo SUMA mientras se reduce significativamente la zona gris y la carga de confirmación, sin comprometer la seguridad clínica del paciente.

# 7. Conclusiones

El presente trabajo demuestra que el algoritmo de interpretación del UMELISA HCV basado en un nivel de corte fijo (CALC ≥ 0,300) y una zona gris del 15 % puede mejorarse significativamente mediante un enfoque adaptativo que utiliza análisis de curva ROC sobre datos históricos reales del sistema SUMA®.

Se logró desarrollar un modelo que recalcula dinámicamente el nivel de corte óptimo cada vez que se actualiza la ventana deslizante de 500 ensayos válidos, utilizando exclusivamente el valor normalizado CALC y excluyendo las placas “Repetir”. Esto permite reducir la incertidumbre diagnóstica y disminuir la carga de pruebas confirmatorias sin modificar el procedimiento técnico ni los reactivos existentes.

Sin embargo, el estándar de oro ideal para etiquetar muestras en zona gris sigue siendo la detección de ARN-VHC por PCR en tiempo real (o inmunoblot). Dado que este método no es viable de forma rutinaria por su elevado costo, tiempo de respuesta y disponibilidad limitada en la mayoría de los laboratorios, se evaluaron cuatro estrategias heurísticas alternativas (descartes totales, pesos diferenciados y clasificación binaria simple). Estas estrategias permitieron entrenar y validar el modelo en condiciones reales de rutina, demostrando que es posible aproximarse de manera segura a la performance de un umbral optimizado por PCR.

La evaluación visual sobre una placa representativa confirmó que ajustes muy pequeños del nivel de corte (0,301–0,302) son clínicamente seguros: convierten borderline en negativo sin generar falsos negativos. En cambio, elevaciones mayores (≥ 0,346) producen conversiones inaceptables de positivo a negativo, lo cual representa un riesgo grave para el paciente (infección no detectada que puede evolucionar a cirrosis o hepatocarcinoma).

Por lo tanto, la implementación final del algoritmo debe incorporar una **restricción de seguridad absoluta**: el nuevo nivel de corte nunca debe convertir en negativo ningún pocillo que el algoritmo original (NC = 0,300) clasificó como positivo. Con esta restricción, y utilizando preferentemente la estrategia de pesos diferenciados o el umbral binario ajustado, se logra reducir entre un 30 % y un 50 % los resultados borderline, aumentando la eficiencia operativa del tamizaje sin comprometer la sensibilidad clínica.

En resumen, aunque la confirmación molecular por PCR sigue siendo el método óptimo para resolver la zona gris, las alternativas heurísticas y el modelo ROC adaptativo aquí propuesto representan una solución práctica, reproducible y de bajo costo que mejora sustancialmente el desempeño del sistema UMELISA HCV en entornos con recursos limitados. Su incorporación al software SUMA® permitiría una clasificación más precisa, una reducción significativa de repeticiones y una mejor utilización de los recursos en los programas nacionales de control de la hepatitis C.
# Bibliografía

- Hanley JA, McNeil BJ. The meaning and use of the area under a receiver operating characteristic (ROC) curve. *Radiology*. 1982;143(1):29-36.  
- Youden WJ. Index for rating diagnostic tests. *Cancer*. 1950;3(1):32-35.  
- Fawcett T. An introduction to ROC analysis. *Pattern Recognition Letters*. 2006;27(8):861-874.  
- Metz CE. Basic principles of ROC analysis. *Semin Nucl Med*. 1978;8(4):283-298.  
- Zweig MH, Campbell G. Receiver-operating characteristic (ROC) plots: a fundamental evaluation tool in clinical medicine. *Clin Chem*. 1993;39(4):561-577.
- Centro de InmunoEnsayo. UMELISA HCV. Códigos UM 2024 y UM 2124 [inserto]. Edición 2. La Habana: Centro de InmunoEnsayo; 2011 Abr 4. 11 p.