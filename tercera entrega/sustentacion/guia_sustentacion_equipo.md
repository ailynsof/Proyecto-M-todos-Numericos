# Guía de Sustentación Oral y Defensa Técnica — Métodos Numéricos
**Universidad Externado de Colombia — Pregrado en Ciencia de Datos**  
**Proyecto Integrador: Métodos Numéricos (Fase 3 — Entrega Final)**  
**Artículo Base:** *Derivative-free optimal multiple-root finding family of iterative methods*, J. H. Jerezano, F. I. Chicharro, N. Garrido-Sáez (*Computational and Applied Mathematics*, 2026)  
**Equipo y Roles:**
- **Sección 1 (El Artículo Base y Fundamentos):** Ailyn Sofía Gómez Rodríguez (Diapositivas 1 a 4) — ~4:00 min
- **Sección 2 (Nuestra Metodología y Desarrollo):** Julián Steven Duarte (Diapositivas 5 a 6) — ~3:30 min
- **Sección 3 (Resultados, Comparación y Conclusiones):** Julián Camilo Jiménez Rodríguez (Diapositivas 7 a 11) — ~5:00 min  
**Duración Total del Video:** 12 a 13 Minutos (dentro del rango requerido de 10 a 15 min)

---

## Estructura General y Cronograma por Diapositiva

```
[00:00 - 04:00] SECCIÓN 1: EL PAPER INICIAL Y FUNDAMENTOS TEÓRICOS (Ailyn Sofía Gómez)
  ├── Diapositiva 1: Portada y Presentación (0:30 min)
  ├── Diapositiva 2: El Problema de las Raíces Múltiples y Régimen de Newton (1:10 min)
  ├── Diapositiva 3: Familia Libre de Derivadas de Jerezano et al. (2026) (1:20 min)
  └── Diapositiva 4: Conjetura y Optimalidad de Kung-Traub (1:00 min)

[04:00 - 07:30] SECCIÓN 2: LO NUESTRO — METODOLOGÍA, ESTABILIDAD Y CRITERIOS (Julián Steven Duarte)
  ├── Diapositiva 5: Dinámica Compleja y Planos de Estabilidad en C (1:45 min)
  └── Diapositiva 6: Metodología Computacional, Parada Dual y Precisión Finita (1:45 min)

[07:30 - 12:30] SECCIÓN 3: RESULTADOS, COMPARACIÓN Y CIERRE (Julián Camilo Jiménez)
  ├── Diapositiva 7: Resultados Experimentales y Contraste con el Artículo (1:30 min)
  ├── Diapositiva 8: Análisis Crítico en g3 (m=4) y Validación de ACOC (1:10 min)
  ├── Diapositiva 9: Extensión Multidimensional 2x2 — Broyden vs Newton (0:50 min)
  ├── Diapositiva 10: Conexión con Ciencia de Datos y Optimización (0:45 min)
  └── Diapositiva 11: Conclusiones, Limitaciones y Trabajo Futuro (0:45 min)
```

---

# GUION VERBAL DIAPOSITIVA POR DIAPOSITIVA (LO QUE DEBE DECIR CADA INTEGRANTE)

---

## SECCIÓN 1: EL PAPER INICIAL Y FUNDAMENTOS TEÓRICOS
**Ponente:** Ailyn Sofía Gómez Rodríguez  
**Tiempo estimado:** 00:00 a 04:00 (4:00 min)  
**Diapositivas:** 1 a 4

---

### Diapositiva 1: Portada y Presentación
* **Tiempo asignado:** 0:30 min (00:00 – 00:30)
* **Lo que debe decir Ailyn:**
> *"Buenos días, profesor Edwin y compañeros. Bienvenidos a la sustentación de la fase final de nuestro proyecto integrador en Métodos Numéricos, titulado: **'Familia Óptima Libre de Derivadas para Raíces Múltiples'**.*
> 
> *Nuestro trabajo se fundamenta en el artículo científico de J. H. Jerezano, F. I. Chicharro y N. Garrido-Sáez, publicado en 2026 en la revista Computational and Applied Mathematics.*
> 
> *La exposición está dividida en tres secciones: primero presentaré los fundamentos y la propuesta del artículo base; luego mi compañero Julián Duarte expondrá nuestra metodología, la estabilidad y el manejo numérico; y finalmente Julián Jiménez presentará los resultados experimentales, la comparación honesta frente al artículo y las conclusiones en Ciencia de Datos. Comencemos con el problema."*

---

### Diapositiva 2: 1. El Problema: Raíces Múltiples y Régimen de Newton
* **Tiempo asignado:** 1:10 min (00:30 – 01:40)
* **Lo que debe decir Ailyn:**
> *"En computación científica, resolver ecuaciones no lineales $g(x) = 0$ es un problema clásico. Sin embargo, surge una dificultad severa cuando la raíz $\alpha$ tiene multiplicidad $m > 1$, es decir, cuando se anulan la función y sus primeras $m-1$ derivadas simultáneamente.*
> 
> *En este escenario, el método de Newton estándar pierde su velocidad cuadrática. Es crucial aclarar que esto no ocurre únicamente porque la derivada tienda a cero, sino porque, bajo una raíz de multiplicidad $m$, el método de Newton clásico presenta una convergencia estrictamente lineal, gobernada por el factor asintótico de error $(m-1)/m$. Por ejemplo, en una raíz doble con $m=2$, en cada iteración el error solo se reduce a la mitad.*
> 
> *La solución teórica clásica es el método de Newton modificado, que multiplica el paso por $m$ y recupera el orden cuadrático ($p=2$). No obstante, este método exige conocer analíticamente y evaluar en cada paso la derivada $g'(x)$. En modelos complejos, redes neuronales o funciones de caja negra en Ciencia de Datos, calcular derivadas analíticas es computacionalmente inviable o sumamente costoso. Por ello, el artículo base plantea un objetivo central: diseñar métodos de alto orden que no requieran evaluar derivadas."*

---

### Diapositiva 3: 2. Familia Libre de Derivadas (Jerezano et al., 2026)
* **Tiempo asignado:** 1:20 min (01:40 – 03:00)
* **Lo que debe decir Ailyn:**
> *"Para resolver esta limitación, Jerezano, Chicharro y Garrido-Sáez propusieron en 2026 una familia iterativa de dos pasos de tipo predictor-corrector que aprovecha el conocimiento de $m$ sin calcular derivadas.*
> 
> *Como vemos en el bloque izquierdo de la diapositiva, el algoritmo primero aproxima la derivada mediante una pendiente secante $D_k = g[w_k, x_k]$, donde el nodo auxiliar introduce una perturbación cuadrática adaptativa: $w_k = x_k + \beta [g(x_k)]^2$, con $\beta \neq 0$. Con esto calcula el predictor $y_k$.*
> 
> *En el segundo paso, se evalúa la variable intermedia $t_k = (g(y_k)/g(x_k))^{1/m}$ y se aplica una función de peso $H(t)$. De acuerdo con el Teorema 2 del artículo, para garantizar orden de convergencia cuatro se deben satisfacer rigurosamente cuatro condiciones: $H(0)=1$, $H'(0)=1$, $H''(0)=4$ y que su tercera derivada en cero sea finita: $|H'''(0)| < \infty$.*
> 
> *En nuestro proyecto implementamos las dos variantes estudiadas por los autores:*
> - *M1, de ponderación polinomial cuadrática: $H_1(t) = 1 + t + 2t^2$, donde $H_1'''(0) = 0 < \infty$.*
> - *M2, de ponderación racional: $H_2(t) = \frac{1-t}{1-2t}$, con $H_2'''(0) = 24 < \infty$ y un polo en $t = 1/2$.*
> 
> *Destacamos dos notas de implementación indispensables: primero, en precisión finita, la condición $\beta \neq 0$ no evita que $w_k = x_k$ ocurra por absorción numérica de la perturbación. Y segundo, para evaluar la potencia fraccionaria $t_k$ cuando el cociente toma valores negativos en etapas transitorias, utilizamos la rama principal del logaritmo complejo con argumento en $(-\pi, \pi]$, asumiendo la discontinuidad del corte de rama sobre el semieje real negativo."*

---

### Diapositiva 4: 3. Conjetura y Optimalidad de Kung-Traub
* **Tiempo asignado:** 1:00 min (03:00 – 04:00)
* **Lo que debe decir Ailyn:**
> *"La relevancia teórica de esta familia se explica mediante la célebre conjetura de Kung y Traub de 1974. Esta conjetura establece que un método iterativo multipaso sin memoria que realiza $d$ evaluaciones funcionales por ciclo puede alcanzar un orden de convergencia máximo acotado por $p \le 2^{d-1}$.*
> 
> *En la familia propuesta, cada ciclo realiza exactamente 3 evaluaciones de función ($g(x_k)$, $g(w_k)$ y $g(y_k)$) y cero derivadas ($d=3$). Por tanto, la cota teórica es $2^{3-1} = 4$. Al cumplir las hipótesis del Teorema 2, la familia alcanza orden cuatro y satura la cota de Kung-Traub, considerándose un método óptimo.*
> 
> *En la tabla de la derecha comparamos los índices de eficiencia computacional teórica, dados por $\mathcal{I} = p^{1/d}$. La familia M1 y M2 alcanza un índice de $4^{1/3} \approx 1.587$, superando notablemente al $1.414$ de Newton modificado y Steffensen modificado.*
> 
> *Hacemos una precisión conceptual rigurosa: el índice de Kung-Traub es una medida teórica basada en orden y evaluaciones; no implica necesariamente menores tiempos de ejecución en CPU en una implementación concreta. Con esto cerramos la fundamentación del paper y doy paso a mi compañero Julián Duarte para explicar nuestra metodología y aportes."*

---

## SECCIÓN 2: LO NUESTRO — METODOLOGÍA, ESTABILIDAD Y CRITERIOS
**Ponente:** Julián Steven Duarte  
**Tiempo estimado:** 04:00 a 07:30 (3:30 min)  
**Diapositivas:** 5 y 6

---

### Diapositiva 5: 4. Estabilidad y Dinámica Compleja en $\mathbb{C}$ (Sección 3)
* **Tiempo asignado:** 1:45 min (04:00 – 05:45)
* **Lo que debe decir Julián Duarte:**
> *"Muchas gracias, Ailyn. Entrando en nuestra sección metodológica, el primer desafío fue comprender cómo afecta el parámetro libre $\beta$ a la estabilidad del método. Siguiendo la Sección 3 del artículo, analizamos el comportamiento en el plano complejo sobre el polinomio cuadrático canónico con raíz doble: $p(z) = (z-1)^2$, donde $m=2$.*
> 
> *Al aplicar el esquema iterativo a este polinomio, se obtiene un operador racional de punto fijo $z_{k+1} = R(z, \beta)$. En la raíz exacta $z^* = 1$, la derivada del operador vale exactamente cero: $R'(1, \beta) = 0$. Esto demuestra formalmente que la raíz es un punto fijo superatractor, lo que garantiza convergencia local de orden superior en una vecindad de la solución.*
> 
> *Para contrastar empíricamente la estabilidad, programamos una malla computacional uniforme de $350 \times 350$ puntos en el dominio acotado $[-2, 2] \times [-2, 2]$ con un límite de 30 iteraciones, comparando M1 y M2 bajo dos valores: $\beta = 0.01$ (recomendado por los autores) y $\beta = 1.0$ (ensayado en nuestra experimentación).*
> 
> *Como observamos en las figuras generadas por nuestro código, con $\beta = 0.01$ una mayor proporción de puntos alcanza el criterio de convergencia en la malla examinada, mostrando cuencas homogéneas. En cambio, con $\beta = 1.0$, aumentan visiblemente los puntos oscuros que no convergen dentro de 30 pasos.*
> 
> *Queremos mantener una postura de rigor científico: este ensayo visual delimita cuencas de atracción numéricas finitas bajo una discretización específica; no constituye una demostración formal de caos ni una caracterización analítica completa de los conjuntos de Fatou y Julia."*

---

### Diapositiva 6: 5. Metodología Computacional y Manejo de Patologías
* **Tiempo asignado:** 1:45 min (05:45 – 07:30)
* **Lo que debe decir Julián Duarte:**
> *"Al trasladar la teoría a una implementación ejecutable y reproducible en Python, establecimos un diseño numérico estricto para evitar sesgos y controlar fallos de hardware:*
> 
> *Primero, configuramos la biblioteca `mpmath` con aritmética de 150 dígitos decimales (`dps = 150`), construyendo todas las constantes decimales directamente desde cadenas de texto para erradicar cualquier error de redondeo binario de punto flotante.*
> 
> *Segundo, establecimos un criterio de parada dual estricto: en raíces múltiples, evaluar únicamente el residuo es engañoso, porque el residuo decrece aproximadamente como $(x-\alpha)^m$. Si $m=4$, una distancia moderada de $10^{-7}$ ya produce un residuo minúsculo de $10^{-28}$. Por ello, nuestro solucionador exige simultáneamente dos condiciones:*
> $$|\Delta x_k| = |x_{k+1} - x_k| < 10^{-25} \quad \text{y} \quad |g(x_{k+1})| < 10^{-25}$$
> 
> *Tercero, y este fue uno de nuestros aportes metodológicos más importantes: auditamos el fenómeno de absorción numérica en precisión finita. Como la perturbación es cuadrática en el residuo, cuando $\beta [g(x_k)]^2$ es tan pequeña que, al sumarse a $x_k$, la mantisa de precisión finita produce el mismo valor representable, el código detecta la igualdad computacional $w_k = x_k$.*
> 
> *Si continuáramos, la secante se dividiría por cero ($w_k - x_k = 0$). En lugar de ocultar esto o reemplazarlo artificialmente por una derivada analítica, nuestro algoritmo diagnostica la igualdad y detiene controladamente la corrida clasificándola de forma honesta como `Estancamiento w=x`.*
> 
> *A continuación, mi compañero Julián Jiménez presentará los resultados experimentales, la comparación con el paper y las conclusiones."*

---

## SECCIÓN 3: RESULTADOS, COMPARACIÓN Y CIERRE
**Ponente:** Julián Camilo Jiménez Rodríguez  
**Tiempo estimado:** 07:30 a 12:30 (5:00 min)  
**Diapositivas:** 7 a 11

---

### Diapositiva 7: 6. Resultados Experimentales y Contraste
* **Tiempo asignado:** 1:30 min (07:30 – 09:00)
* **Lo que debe decir Julián Jiménez:**
> *"Muchas gracias, Julián. En la Diapositiva 7 presentamos los resultados consolidados de nuestras corridas experimentales deterministas con 150 dígitos de precisión y tolerancia $10^{-25}$. Como se indica en la nota inferior, mostramos casos representativos; el archivo CSV del repositorio conserva todas las combinaciones completas.*
> 
> *En el problema $g_1$ (polinomio de Van der Waals con raíz doble en $1.75$ y semilla $1.9$), el método M1 converge en solo 5 iteraciones con un error absoluto de $1.32\times 10^{-35}$ y un residuo de $5.26\times 10^{-72}$, superando en número de pasos a Newton modificado y a Steffensen, que requirieron 8 iteraciones.*
> 
> *Queremos transparentar la auditoría en el conteo de evaluaciones: la fórmula $1+3k+1$ aplica específicamente a M1 y M2. Corresponde a evaluar $g(x_0)$ al inicio, $3$ funciones en cada uno de los $k$ pasos internos, y una llamada final de comprobación $g(x_{\mathrm{final}})$ ejecutada explícitamente tras salir del ciclo para registrar el residuo de parada en memoria.*
> 
> *Respecto a la comparación honesta con el artículo base: para $g_1$, M1 satisface nuestro criterio dual en 5 iteraciones, frente a las 7 reportadas por los autores. Queremos ser enfáticos: esta diferencia no demuestra una superioridad algorítmica de nuestra implementación; se debe a que utilizamos una tolerancia práctica de $10^{-25}$ con 150 dígitos, mientras que los autores emplearon una tolerancia extrema de $10^{-200}$ con 4000 dígitos en Matlab. Nuestro criterio operativo se cumple antes en la trayectoria de convergencia.*
> 
> *Asimismo, en M2 observamos `Estancamiento w=x` tras 4 pasos: la perturbación cayó al orden de $10^{-204}$, lo que provocó absorción numérica a pesar de que la aproximación ya poseía un error absoluto minúsculo de $2.03\times 10^{-50}$."*

---

### Diapositiva 8: 7. Hallazgo en $g_3$ ($m=4$) y Validación de ACOC
* **Tiempo asignado:** 1:10 min (09:00 – 10:10)
* **Lo que debe decir Julián Jiménez:**
> *"La Diapositiva 8 expone el hallazgo técnico más riguroso de nuestro proyecto: la distinción entre parada operativa y precisión efectiva en el polinomio $g_3$ con raíz cuádruple en $\alpha=3$.*
> 
> *Cerca de $x=3$, el polinomio se comporta aproximadamente como $g_3(x) \approx -80(x-3)^4$. Debido a la potencia cuarta, una distancia de apenas $10^{-18}$ a la raíz produce un residuo minúsculo de $10^{-72}$. Por esta razón, el paso consecutivo colapsó por debajo de $10^{-59}$ y el solucionador detuvo la corrida en 3 iteraciones cumpliendo el criterio dual de $10^{-25}$.*
> 
> *Sin embargo, al medir el error absoluto frente a la raíz exacta $\alpha=3$, la distancia real es de $3.71\times 10^{-18}$, que es mayor que $10^{-25}$. Con total integridad técnica, no declaramos esta corrida como un éxito de convergencia superior a las 5 iteraciones del artículo, sino que la clasificamos formalmente como `Criterio dual; error > TOL`, documentando que se trató de una terminación anticipada por contracción residual extrema.*
> 
> *Por otra parte, evaluamos el orden computacional ACOC: primero validamos la rutina en el problema canónico de raíz simple $x^3-x-2=0$, donde Newton arrojó $\mathrm{ACOC} \approx 2.0000$ y la secante $\mathrm{ACOC} \approx 1.6162$, muy cercano al valor teórico de la razón áurea ($1.6180$).*
> 
> *No obstante, en raíces múltiples con 3 a 5 iteraciones, la aceleración transitoria distorsiona el cociente logarítmico, produciendo valores atípicos como 8.81 en M1. Esto confirma que el ACOC es una herramienta diagnóstica asintótica y no una prueba matemática de orden superior a cuatro."*

---

### Diapositiva 9: 8. Extensión a Sistemas No Lineales $2\times 2$ (Broyden)
* **Tiempo asignado:** 0:50 min (10:10 – 11:00)
* **Lo que debe decir Julián Jiménez:**
> *"Como experimento complementario alineado con la Semana 9 del curso, extendimos el análisis a sistemas de ecuaciones no lineales en varias dimensiones resolviendo un sistema $2\times 2$.*
> 
> *Newton multivariable convergió a la raíz en 5 iteraciones con residuo de $10^{-15}$, pero necesitó evaluar 20 derivadas Jacobianas analíticas y resolver 5 sistemas lineales densos. En contraste, el método secante de Broyden alcanzó la misma precisión en 10 iteraciones con cero derivadas analíticas.*
> 
> *Precisamos la estructura del costo computacional: Broyden actualiza la aproximación del Jacobiano mediante una corrección de rango uno con costo $O(n^2)$ y evita calcular $n^2$ derivadas parciales; sin embargo, en cada iteración continúa resolviendo un sistema lineal denso de costo $O(n^3)$. Este ensayo ilustra el compromiso práctico entre número de iteraciones y costo por evaluación que motiva los métodos libres de derivadas."*

---

### Diapositiva 10: 9. Conexión con Ciencia de Datos y Optimización
* **Tiempo asignado:** 0:45 min (11:00 – 11:45)
* **Lo que debe decir Julián Jiménez:**
> *"¿Cómo conecta todo esto con nuestra carrera en Ciencia de Datos? En Machine Learning, entrenar modelos consiste en optimizar una función de pérdida buscando puntos estacionarios donde el gradiente se anula: $\nabla L(\boldsymbol{\theta}) = \mathbf{0}$.*
> 
> *En paisajes de pérdida complejos con valles planos o puntos de ensilladura degenerados, la matriz Hessiana posee autovalores cercanos a cero, lo que dificulta enormemente los algoritmos de optimización estándar basados en gradiente.*
> 
> *Estos escenarios motivan el estudio de puntos críticos degenerados. Sin embargo, aclaramos con rigor que una Hessiana con autovalores nulos no demuestra por sí sola que el gradiente tenga una raíz de multiplicidad $m>1$. Los métodos estudiados ofrecen una valiosa referencia conceptual para explorar algoritmos que aprovechen multiplicidad, cuya aplicación a pérdidas de alta dimensión requerirá formulaciones tensoriales y validaciones adicionales."*

---

### Diapositiva 11: 10. Conclusiones y Trabajo Futuro
* **Tiempo asignado:** 0:45 min (11:45 – 12:30)
* **Lo que debe decir Julián Jiménez:**
> *"Para concluir nuestra sustentación:*
> 1. *Implementamos una familia de métodos de orden teórico cuatro que satura la cota óptima de Kung-Traub bajo las condiciones del Teorema 2, documentando tanto casos de rápida convergencia como estancamientos por precisión finita.*
> 2. *En la dinámica compleja sobre la malla examinada, $\beta=0.01$ mostró una convergencia más favorable y regular que $\beta=1.0$.*
> 3. *Demostramos honestidad técnica al identificar que en raíces cuádruples el residuo colapsa antes que el error, clasificando el estado con transparencia.*
> 
> *Como limitación central, señalamos que estos métodos asumen que la multiplicidad exacta $m$ es conocida a priori. Si se suministra un $m$ erróneo, el orden cuártico se degrada a orden lineal.*
> 
> *Como trabajo futuro, planteamos diseñar estimadores adaptativos dinámicos de $m$ durante las primeras iteraciones y estudiar extensiones libres de derivadas para optimización estocástica.*
> 
> *Agradecemos al profesor Edwin Fernando Muñoz por su retroalimentación durante el semestre. Quedamos a su entera disposición para la sesión de preguntas. ¡Muchas gracias!"*

---

## BANCO ESTRATÉGICO DE RESPUESTAS RÁPIDAS PARA LA SESIÓN DE PREGUNTAS

| Pregunta del Docente | Integrante que responde | Respuesta Técnica Concreta |
| :--- | :---: | :--- |
| **¿Por qué Newton clásico pierde orden cuadrático ante multiplicidad $m$?** | **Ailyn** | Por la expansión de Taylor: cerca de $\alpha$, $g(x)\approx \frac{g^{(m)}(\alpha)}{m!}(x-\alpha)^m$ y $g'(x)\approx \frac{g^{(m)}(\alpha)}{(m-1)!}(x-\alpha)^{m-1}$. El cociente da $\frac{1}{m}(x-\alpha)$, y el error resulta $x_{k+1}-\alpha = \frac{m-1}{m}(x_k-\alpha)$, demostrando convergencia lineal con factor $(m-1)/m$. |
| **¿Por qué se estancó M2 si el parámetro $\beta \neq 0$?** | **Julián Duarte** | $\beta \neq 0$ garantiza $w_k \neq x_k$ en $\mathbb{R}$, pero en aritmética finita de 150 dígitos, cuando el residuo decae a $10^{-86}$, la perturbación cuadrática $\beta g(x_k)^2 \approx 10^{-173}$ es menor que la resolución relativa de $x_k$. Al sumarse, la mantisa produce $w_k == x_k$ por absorción numérica. |
| **¿Por qué no clasificaron como 'Convergió' a $g_3$ si cumplió la tolerancia dual?** | **Julián Jiménez** | Porque cerca de $\alpha=3$, $g_3(x)\approx -80(x-3)^4$. Con un error real de $10^{-18}$, el residuo ya es $10^{-72}$ y el paso $10^{-60}$. Cumple formalmente la cota operativa dual de $10^{-25}$, pero el error frente a la raíz sigue siendo $10^{-18} > 10^{-25}$. Declarar convergencia plena sería un falso positivo metodológico. |
| **¿El ACOC de 8.81 en M1 significa que el método es de orden 8?** | **Julián Jiménez** | No. El ACOC es una aproximación asintótica. Cuando un método converge en 3 o 4 pasos, la aceleración drástica distorsiona los cocientes logarítmicos, produciendo un valor espurio transitorio. Validamos la rutina en raíz simple donde arrojó $2.0000$ (Newton) y $1.6162$ (Secante). |
| **¿Broyden reduce el costo por iteración a $O(n^2)$?** | **Julián Jiménez** | No totalmente. Broyden actualiza la matriz en $O(n^2)$ y evita evaluar $n^2$ derivadas parciales, pero en cada paso continúa resolviendo un sistema lineal denso, cuyo costo sigue siendo $O(n^3)$. |
