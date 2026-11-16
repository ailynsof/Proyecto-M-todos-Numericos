# Guía de Sustentación Oral y Defensa Técnica — Métodos Numéricos
**Universidad Externado de Colombia — Pregrado en Ciencia de Datos**  
**Proyecto Integrador: Métodos Numéricos (Fase 3 — Entrega Final)**  
**Artículo Base:** *Derivative-free optimal multiple-root finding family of iterative methods*, J. H. Jerezano, F. I. Chicharro, N. Garrido-Sáez (*Computational and Applied Mathematics*, 2026)  
**Equipo:** Ailyn Sofía Gómez Rodríguez, Julián Steven Duarte, Julián Camilo Jiménez Rodríguez  
**Docente:** Edwin Fernando Muñoz Chipatecua  
**Duración Total Estimada:** 12 a 15 Minutos (Video / Defensa Oral)

---

## 1. Distribución de la Exposición y Roles del Equipo (12 a 15 Minutos)

Para asegurar una participación equitativa y demostrar dominio conceptual colectivo según los criterios de la rúbrica institucional (Sección 8.5), la sustentación se estructura en tres bloques temporales coordinados:

| Integrante | Bloque Temático | Diapositivas | Tiempo Estimado | Puntos Clave a Desarrollar |
| :--- | :--- | :---: | :---: | :--- |
| **Ailyn Sofía Gómez Rodríguez** | **Bloque 1:** Planteamiento, Métodos y Optimalidad de Kung-Traub | Diapositivas 1 a 4 | 3.5 – 4.5 min | Definición de multiplicidad $m \ge 2$; pérdida de convergencia cuadrática en Newton estándar ($p=1$); formulación del predictor-corrector libre de derivadas de Jerezano et al. (2026); condiciones completas del Teorema 2 ($H(0)=1, H'(0)=1, H''(0)=4, |H'''(0)|<\infty$); definición correcta de $M_1$ y $M_2(t)=\frac{1-t}{1-2t}$; conjetura de Kung-Traub e índice de eficiencia teórica ($\mathcal{I} = 4^{1/3} \approx 1.587$). |
| **Julián Steven Duarte** | **Bloque 2:** Estabilidad Dinámica, Metodología y Criterios Numéricos | Diapositivas 5 a 6 | 4.0 – 4.5 min | Operador racional de punto fijo $R(z,\beta)$ sobre $p(z)=(z-1)^2$; condición de punto fijo superatractor ($R'(1)=0$); análisis numérico del parámetro $\beta \in \{0.01, 1.0\}$ sobre malla en $\mathbb{C}$; uso riguroso de la rama principal del logaritmo complejo $\operatorname{Ln}(z)=\ln|z|+i\operatorname{Arg}(z)$ con $\operatorname{Arg}(z)\in(-\pi,\pi]$ (reconociendo el corte de rama); criterio de parada dual estricto ($|\Delta x_k|<10^{-25}$ y $|g(x_{k+1})|<10^{-25}$); y diagnóstico del estancamiento por absorción en precisión finita ($w_k == x_k$). |
| **Julián Camilo Jiménez Rodríguez** | **Bloque 3:** Resultados, Benchmarks, Sistemas, Ciencia de Datos y Cierre | Diapositivas 7 a 11 | 4.5 – 5.5 min | Demostración en Python con `mpmath` a 150 dígitos; análisis honesto de la tabla de resultados; conteo transparente de evaluaciones ($1+3k+1$); distinción crítica en $g_3$ ($m=4$) entre terminación por criterio dual y exactitud efectiva (\texttt{Criterio dual; error > TOL}); validación y cautela diagnóstica del ACOC; experimento complementario multidimensional $2\times 2$ (Newton multivariable vs. Broyden); conexiones reales con optimización y paisajes de pérdida en Ciencia de Datos; limitaciones (conocimiento previo de $m$) y trabajo futuro. |

---

## 2. Guion Borrador Completo de Sustentación

### Bloque 1: Planteamiento, Métodos y Fundamentación Teórica
**Ponente:** Ailyn Sofía Gómez Rodríguez  
**Tiempo sugerido:** 3:30 – 4:30 minutos  
**Diapositivas asociadas:** 1 a 4

> *"¡Buenos días a todos! Bienvenidos a la sustentación final de nuestro proyecto integrador en Métodos Numéricos. En computación científica y ciencia de datos, resolver ecuaciones no lineales de la forma $g(x) = 0$ es un problema fundamental. Sin embargo, surge una patología matemática severa cuando la raíz buscada $\alpha$ posee multiplicidad conocida $m > 1$.*
> 
> *En este escenario, tanto la función como sus primeras $m-1$ derivadas se anulan en la raíz ($g'(x) \to 0$). Al evaluar el método de Newton clásico, el denominador tiende a cero, perdiendo su convergencia cuadrática y degradándose a un régimen estrictamente lineal ($p=1$), con una razón asintótica de error $C = \frac{m-1}{m}$. Aunque el método de Newton modificado recupera el orden cuadrático multiplicando el paso por $m$, exige calcular la derivada analítica $g'(x)$, la cual resulta computacionalmente inviable o muy costosa en modelos complejos.*
> 
> *Para resolver esta dificultad, basamos nuestro trabajo en el artículo científico de Jerezano, Chicharro y Garrido-Sáez (2026), publicado en Computational and Applied Mathematics. Los autores proponen una familia de dos pasos de tipo predictor-corrector que alcanza orden de convergencia cuatro sin evaluar derivadas analíticas, utilizando una perturbación cuadrática adaptativa $w_k = x_k + \beta [g(x_k)]^2$ y una diferencia dividida secante $g[w_k, x_k]$.*
> 
> *Desde el punto de vista teórico, la conjetura de Kung-Traub (1974) establece que ningún método iterativo multipaso sin memoria con $d$ evaluaciones funcionales por ciclo puede superar un orden $p \le 2^{d-1}$. La familia de Jerezano et al. evalúa exactamente tres funciones escalares ($g(x_k), g(w_k), g(y_k)$) y cero derivadas ($d=3$), alcanzando la cota óptima $p = 2^{3-1} = 4$.*
> 
> *De acuerdo con el Teorema 2 del artículo, para garantizar este orden cuatro, la función de peso $H(t)$ debe satisfacer cuatro condiciones rigurosas: $H(0)=1$, $H'(0)=1$, $H''(0)=4$ y $|H'''(0)|<\infty$. En nuestro proyecto estudiamos e implementamos sus dos variantes principales:*
> - *Variante $M_1$ (polinomial cuadrática): $H_1(t) = 1 + t + 2t^2$, donde $H_1'''(0) = 0 < \infty$.*
> - *Variante $M_2$ (racional): $H_2(t) = \frac{1-t}{1-2t}$, con $H_2'''(0) = 24 < \infty$ y polo en $t = 1/2$.*
> 
> *Ambas variantes alcanzan un índice de eficiencia computacional teórico $\mathcal{I} = 4^{1/3} \approx 1.587$, que supera teóricamente al valor $\mathcal{I} = 2^{1/2} \approx 1.414$ de Newton modificado y Steffensen. Doy paso a mi compañero Julián Duarte para explicar la estabilidad y la metodología computacional."*

---

### Bloque 2: Estabilidad Dinámica, Metodología y Criterios Numéricos
**Ponente:** Julián Steven Duarte  
**Tiempo sugerido:** 4:00 – 4:30 minutos  
**Diapositivas asociadas:** 5 a 6

> *"Muchas gracias, Ailyn. Para comprender el papel del parámetro libre $\beta$, el artículo analiza la dinámica en el plano complejo $\mathbb{C}$ sobre el polinomio cuadrático canónico con raíz doble $p(z) = (z-1)^2$ ($m=2$). Al aplicar el esquema, se obtiene un operador racional de punto fijo $z_{k+1} = R(z, \beta)$. En la raíz exacta $z^* = 1$, la derivada analítica del operador vale exactamente cero ($R'(1, \beta) = 0$), lo que demuestra formalmente que la raíz es un punto fijo superatractor, garantizando convergencia local de orden superior en su vecindad.*
> 
> *En nuestra experimentación, construimos una malla computacional uniforme de $350 \times 350$ puntos en el dominio acotado $[-2, 2] \times [-2, 2]$. Al contrastar $\beta = 0.01$ (propuesto en el artículo) frente a $\beta = 1.0$, observamos que una perturbación moderada ($\beta=0.01$) genera una cuenca de convergencia regular y amplia, mientras que perturbaciones mayores multiplican los puntos que no logran converger dentro de 30 iteraciones. Aclaramos con rigor que esta exploración delimita cuencas numéricas efectivas, sin constituir una caracterización matemática formal completa de los conjuntos de Fatou y Julia.*
> 
> *En cuanto a la metodología computacional en Python, implementamos tres decisiones técnicas indispensables:*
> 1. *Rama principal del logaritmo complejo: En el predictor, la variable intermedia es $t_k = (g(y_k)/g(x_k))^{1/m}$. En etapas transitorias, el cociente entre funciones puede tomar valores negativos o complejos. Para evaluar la raíz sin incurrir en errores de dominio real (`ValueError`), utilizamos la rama principal: $t_k = \exp\left(\frac{1}{m}\operatorname{Log}\left(\frac{g(y_k)}{g(x_k)}\right)\right)$, con $\operatorname{Arg}(z) \in (-\pi, \pi]$. Reconocemos que esta convención aporta un cálculo univaluado bien definido, asumiendo la discontinuidad del corte de rama sobre el semieje real negativo.*
> 2. *Criterio de parada dual estricto: En raíces múltiples, el residuo decae aproximadamente como $|x-\alpha|^m$. Por ejemplo, en $g_3(x) \approx -80(x-3)^4$, un residuo de $10^{-68}$ se produce con un error en $x$ de $10^{-18}$. Si evaluáramos solo el residuo, el método se detendría prematuramente creyendo haber alcanzado alta precisión. Por ello, exigimos obligatoriamente la conjunción dual: el paso $|\Delta x_k| = |x_{k+1}-x_k| < 10^{-25}$ Y el residuo $|g(x_{k+1})| < 10^{-25}$.*
> 3. *Detección de absorción numérica en mantisa finita: La perturbación $w_k = x_k + \beta g(x_k)^2$ disminuye cuadráticamente con el residuo. Bajo los 150 dígitos configurados en `mpmath`, cuando el residuo es del orden de $10^{-80}$ a $10^{-100}$, la cantidad sumada resulta demasiado pequeña para modificar la representación numérica de $x_k$. Nuestro código evalúa directamente si $w_k == x_k$ y detiene controladamente la corrida clasificándola como `Estancamiento w=x`, evitando divisiones por cero indeterminadas en la secante sin introducir parches artificiales.*
> 
> *A continuación, Julián Jiménez presentará los resultados experimentales, el contraste con el artículo y las aplicaciones en Ciencia de Datos."*

---

### Bloque 3: Resultados, Benchmarks, Sistemas, Ciencia de Datos y Cierre
**Ponente:** Julián Camilo Jiménez Rodríguez  
**Tiempo sugerido:** 4:30 – 5:30 minutos  
**Diapositivas asociadas:** 7 a 11

> *"Gracias, Julián. Voy a proyectar y analizar los resultados consolidados de nuestras corridas experimentales en Python con `mpmath` a 150 dígitos decimales sobre los tres problemas deterministas del artículo:*
> 1. *$g_1$: Polinomio cúbico de Van der Waals, con raíz doble en $\alpha=1.75$.*
> 2. *$g_2$: Ley de Planck al cubo, con raíz triple positiva en $\alpha \approx 4.96511423$.*
> 3. *$g_3$: Polinomio característico de grado 9, con raíz cuádruple en $\alpha=3.0$.*
> 
> *Como observamos en el Cuadro comparativo, para $g_1$ con semilla $1.9$, el método M1 converge en 5 iteraciones alcanzando un residuo de $5.26\times 10^{-72}$ y un error absoluto de $1.32\times 10^{-35}$, superando en velocidad de reducción del residuo a Newton modificado y Steffensen (que requirieron 8 iteraciones).*
> 
> *Realizamos además una auditoría transparente del conteo de evaluaciones funcionales: cada iteración de M1 y M2 ejecuta exactamente 3 llamadas ($g(x_k), g(w_k), g(y_k)$). Nuestro solucionador registra $g(x_0)$ al inicio y ejecuta una llamada adicional $g(x_{\mathrm{final}})$ al salir del ciclo para registrar de forma independiente el residuo de parada, totalizando $1+3k+1$ evaluaciones ($17$ llamadas en 5 iteraciones). En métodos interrumpidos, como KK en $g_1$, se auditan estrictamente las llamadas ejecutadas antes de detectar la anulación del denominador (15 evaluaciones).*
> 
> *Un hallazgo metodológico fundamental ocurrió con el polinomio $g_3$ ($m=4$, semilla $2.8$): nuestra implementación detiene el algoritmo en 3 iteraciones porque el paso se reduce a $5.62\times 10^{-60}$ y el residuo a $10^{-68}$, cumpliendo operativamente la tolerancia dual de $10^{-25}$. Sin embargo, al contrastar frente a la raíz exacta $\alpha=3$, el error absoluto es de $3.71\times 10^{-18}$, superior a la tolerancia. El residuo colapsó por la potencia cuarta, no porque el iterado haya alcanzado una precisión de 25 dígitos. Con total honestidad técnica, no calificamos esta corrida como un éxito de convergencia superior frente a las 5 iteraciones del artículo, sino que la clasificamos formalmente como `Criterio dual; error > TOL`, distinguiendo entre la parada operativa y la exactitud efectiva.*
> 
> *Respecto al orden computacional ACOC: validamos pedagógicamente el estimador sobre la raíz simple de $x^3-x-2=0$, obteniendo exactamente los órdenes teóricos esperados (Newton $\to 2.0000$, Secante $\to 1.6162$). Sin embargo, en raíces múltiples bajo pocas iteraciones (3 a 5 pasos), los efectos transitorios producen valores sobreestimados (como $8.81$), lo que nos permite concluir que el ACOC es una herramienta diagnóstica asintótica y no una prueba concluyente en regímenes breves.*
> 
> *Como experimento complementario alineado con la Semana 9 del curso, extendimos el estudio a sistemas no lineales $2\times 2$. Newton multivariable resolvió el sistema en 5 iteraciones con residuo de $10^{-15}$, pero requirió evaluar 20 derivadas parciales Jacobianas. En contraste, el método secante de Broyden alcanzó la misma precisión en 10 iteraciones con cero derivadas analíticas, evidenciando el compromiso computacional entre número de iteraciones y costo por evaluación que fundamenta los esquemas sin derivadas.*
> 
> *En Ciencia de Datos, el entrenamiento de modelos busca puntos críticos $\nabla L(\boldsymbol{\theta}) = \mathbf{0}$. En paisajes de pérdida mal condicionados con valles planos o puntos de ensilladura degenerados, la matriz Hessiana posee autovalores cercanos a cero, asemejándose a multiplicidades analíticas donde los algoritmos convencionales se ralentizan drásticamente. Las familias estudiadas ofrecen un marco teórico para diseñar futuros optimizadores de orden superior libres de derivadas.*
> 
> *Como principal limitación, destacamos que estos métodos asumen conocida la multiplicidad exacta $m$, la cual rara vez se conoce a priori en problemas reales. Como trabajo futuro, proponemos diseñar estimadores dinámicos de $m$ durante las primeras iteraciones y estudiar extensiones para optimización estocástica.*
> 
> *Agradecemos al profesor Edwin Muñoz por sus valiosas retroalimentaciones durante el semestre. Quedamos a su entera disposición para la sesión de preguntas. ¡Muchas gracias!"*

---

## 3. Modificaciones Metodológicas Clave Incorporadas (Defensa Técnica)

Para sustentar con solvencia académica las decisiones adoptadas en el proyecto y responder a las exigencias de la rúbrica de excelencia:

### A. Criterio de Parada Dual Estricto
* **Fundamento:** En raíces de multiplicidad $m>1$, el residuo se amortigua como $g(x) \approx \frac{g^{(m)}(\alpha)}{m!} (x-\alpha)^m$. Si $m=4$, una distancia de $10^{-7}$ ya genera un residuo de $10^{-28}$. Un criterio basado únicamente en residuo detendría la iteración lejos de la raíz.
* **Implementación:** Conjunción lógica obligatoria:
  $$|\Delta x_k| = |x_{k+1}-x_k| < 10^{-25} \quad \wedge \quad |g(x_{k+1})| < 10^{-25}.$$
* **Aporte crítico:** Distinción explícita en la tabla entre convergencia efectiva a la tolerancia y terminación anticipada por contracción residual en $g_3$ (\texttt{Criterio dual; error > TOL}).

### B. Diagnóstico Riguroso de la Absorción Numérica ($w_k == x_k$)
* **Fundamento:** La perturbación secante es cuadrática en el residuo: $w_k = x_k + \beta [g(x_k)]^2$. En precisión finita de mantisa fija (incluso con 150 dígitos en `mpmath`), cuando $|g(x_k)|$ decae a escalas como $10^{-80}$ o $10^{-100}$, la cantidad $\beta g(x_k)^2$ resulta menor que la resolución relativa de representación de $x_k$.
* **Manejo:** Se evalúa la igualdad computacional `w == x` antes de formar el cociente secante. Si se cumple, el código aborta de forma controlada y clasifica el estado como `Estancamiento w=x`, evitando divisiones por cero no controladas y diagnosticando una limitación de hardware frente a la escala de la perturbación.

### C. Evaluación Analítica Univaluada en $\mathbb{C}$ mediante Rama Principal
* **Fundamento:** En el predictor-corrector, $t_k = (g(y_k)/g(x_k))^{1/m}$. En etapas transitorias previas a la convergencia, el cociente entre funciones puede tomar valores negativos o complejos. En la aritmética real ($\mathbb{R}$), potencias con base negativa y exponentes pares ($m=2, 4$) arrojan errores de dominio.
* **Implementación:** Se utiliza la rama principal del logaritmo complejo:
  $$t_k = \exp\left(\frac{1}{m} \operatorname{Log}\left(\frac{g(y_k)}{g(x_k)}\right)\right), \quad \text{con } \operatorname{Log}(z) = \ln|z| + i \operatorname{Arg}(z), \quad \operatorname{Arg}(z) \in (-\pi, \pi].$$
* **Rigor matemático:** Se reconoce que la rama principal es analítica y univaluada en el plano complejo cortado $\mathbb{C} \setminus (-\infty, 0]$, garantizando estabilidad computacional mientras se asume la discontinuidad propia del corte de rama sobre el semieje real negativo.

### D. Verificación Formal de las Cuatro Condiciones del Teorema 2
* **Condiciones teóricas:** Para alcanzar orden cuatro en el sentido de Kung-Traub, el Teorema 2 del artículo base exige:
  $$H(0)=1, \quad H'(0)=1, \quad H''(0)=4, \quad \text{y} \quad |H'''(0)| < \infty.$$
* **Verificación de variantes:**
  - **M1:** $H_1(t) = 1 + t + 2t^2 \implies H_1(0)=1, H_1'(0)=1, H_1''(0)=4, H_1'''(0) = 0 < \infty$.
  - **M2:** $H_2(t) = \frac{1-t}{1-2t} \implies H_2'(t) = \frac{1}{(1-2t)^2}, H_2''(t) = \frac{4}{(1-2t)^3}, H_2'''(t) = \frac{24}{(1-2t)^4}$. Evaluando en cero: $H_2(0)=1, H_2'(0)=1, H_2''(0)=4, H_2'''(0) = 24 < \infty$, con polo en $t=1/2$. Ambas cumplen plenamente el teorema.

---

## 4. Banco Estratégico de Preguntas Difíciles del Docente y Cómo Responderlas

### P1. ¿Por qué el método de Newton clásico pierde su orden cuadrático ante una raíz múltiple?
* **Respuesta:**  
  En una raíz $\alpha$ de multiplicidad $m > 1$, la expansión en serie de Taylor de $g(x)$ inicia en grado $m$:  
  $$g(x) = \frac{g^{(m)}(\alpha)}{m!} (x-\alpha)^m + \mathcal{O}((x-\alpha)^{m+1}), \quad g'(x) = \frac{g^{(m)}(\alpha)}{(m-1)!} (x-\alpha)^{m-1} + \mathcal{O}((x-\alpha)^m).$$  
  El cociente de paso de Newton resulta:  
  $$\frac{g(x)}{g'(x)} \approx \frac{\frac{1}{m!} (x-\alpha)^m}{\frac{1}{(m-1)!} (x-\alpha)^{m-1}} = \frac{1}{m} (x-\alpha).$$  
  Sustituyendo en la fórmula del iterado:  
  $$x_{k+1} - \alpha = (x_k - \alpha) - \frac{1}{m}(x_k - \alpha) = \frac{m-1}{m}(x_k - \alpha).$$  
  El error decae linealmente con constante asintótica $C = \frac{m-1}{m} < 1$. Por ejemplo, si $m=2$, el error solo se reduce a la mitad por paso ($C=0.5$). Al multiplicar el paso por $m$ (Newton modificado), se cancela este factor lineal y se restaura el orden cuadrático ($p=2$).

### P2. ¿Qué establece la conjetura de Kung-Traub y qué significa que el método sea óptimo?
* **Respuesta:**  
  La conjetura de H. T. Kung y J. F. Traub (1974) postula que un método iterativo multipaso sin memoria que utiliza $d$ evaluaciones funcionales por iteración tiene un orden de convergencia máximo $p \le 2^{d-1}$.  
  En la familia de Jerezano et al., cada paso evalúa exactamente 3 funciones escalares ($g(x_k), g(w_k), g(y_k)$) y ninguna derivada ($d=3$). Por tanto, la cota máxima teórica es $p \le 2^{3-1} = 4$.  
  Como los autores demuestran teóricamente que el esquema alcanza orden 4 bajo las condiciones sobre $H(t)$, el método satura la cota superior, siendo **óptimo en el sentido de Kung-Traub**, con un índice de eficiencia computacional teórico $\mathcal{I} = 4^{1/3} \approx 1.587$, superior al $\mathcal{I} = 2^{1/2} \approx 1.414$ de los métodos de orden 2.

### P3. ¿Por qué en la tabla M1 converge en 5 iteraciones para $g_1$ mientras el artículo reporta 7?
* **Respuesta:**  
  La diferencia obedece estrictamente a las condiciones operativas de parada fijadas en ambos experimentos. En nuestro trabajo establecimos una tolerancia práctica de $10^{-25}$ con precisión de 150 dígitos decimales en `mpmath`, mientras que los autores en el artículo emplearon Matlab con 4000 dígitos decimales y una tolerancia extrema de $|x_{k+1}-x_k| + |g(x_k)| < 10^{-200}$.  
  Como nuestro umbral de parada se alcanza antes en la trayectoria de contracción, el método reporta menos iteraciones. Esta diferencia valida el comportamiento del método bajo nuestra configuración, pero no demuestra una superioridad algorítmica sobre los resultados del artículo.

### P4. ¿Por qué en $g_3$ ($x_0=2.8$) clasificaron el estado como "Criterio dual; error > TOL" en lugar de Convergió?
* **Respuesta:**  
  Porque en raíces de multiplicidad alta ($m=4$), el polinomio localmente se comporta como $g_3(x) \approx -80(x-3)^4$. Cuando el iterado se encuentra a una distancia de $3.71\times 10^{-18}$ de la raíz exacta, su residuo ya colapsa a $1.52\times 10^{-68}$ y el paso consecutivo a $10^{-60}$.  
  Aunque el algoritmo satisface operativamente la tolerancia dual impuesta ($10^{-25}$ tanto en paso como en residuo), el error absoluto real frente a $\alpha=3.0$ sigue siendo del orden de $10^{-18}$, es decir, mayor que $10^{-25}$. Por transparencia y rigor científico, no calificamos la corrida como una convergencia efectiva a la precisión esperada, sino como una terminación anticipada por contracción residual extrema.

### P5. ¿Por qué el ACOC arrojó valores atípicos como 8.81 en $M_1$ o 5.91 en KK?
* **Respuesta:**  
  El estimador ACOC de Cordero y Torregrosa requiere que el método se encuentre en su **régimen asintótico terminal** y que se disponga de suficientes iteraciones consecutivas sin perturbación por escala de máquina.  
  En métodos de orden 4 que convergen en apenas 3 a 5 iteraciones, el paso pasa abruptamente de $10^{-3}$ a $10^{-9}$ y a $10^{-35}$. En las últimas iteraciones, las diferencias sucesivas son tan drásticas que los cocientes logarítmicos del ACOC sufren distorsiones transitorias numéricas.  
  Validamos formalmente la rutina en el problema de raíz simple $x^3-x-2=0$, donde Newton arrojó exactamente $\mathrm{ACOC} \to 2.0000$ y la secante $\mathrm{ACOC} \to 1.6162$, demostrando que la implementación es correcta y que las lecturas en raíces múltiples son efectos transitorios propios de la rápida contracción en pocas iteraciones.

### P6. ¿Por qué ocurre "Estancamiento w=x" en M2 para $g_1$ y $g_2$?
* **Respuesta:**  
  La perturbación adaptativa secante se define como $w_k = x_k + \beta [g(x_k)]^2$. En la 4.ª iteración de $g_1$ con M2, el residuo es de $1.24\times 10^{-101}$, lo que genera una perturbación $\beta g(x)^2 \approx 1.5\times 10^{-204}$.  
  Bajo la precisión configurada de 150 dígitos decimales, una cantidad del orden de $10^{-204}$ resulta demasiado pequeña para modificar la representación numérica de $x_k$ (absorción en punto flotante). Computacionalmente se produce la igualdad exacta $w_k == x_k$, anulando el denominador $w_k - x_k$ de la secante. Nuestro código detecta esta igualdad y detiene el proceso con un diagnóstico honesto de limitación de mantisa, a pesar de que la aproximación ya poseía un error absoluto minúsculo de $2.03\times 10^{-50}$.

### P7. ¿Qué se concluye de los planos dinámicos en el plano complejo y por qué no se puede afirmar caos?
* **Respuesta:**  
  El análisis demuestra que para el polinomio cuadrático canónico $p(z)=(z-1)^2$, la raíz $z^*=1$ es un punto fijo superatractor ($R'(1)=0$), lo que garantiza convergencia local acelerada.  
  En la exploración visual sobre la malla de $350\times 350$, observamos que con $\beta=0.01$ la cuenca de atracción converge rápidamente, mientras que con $\beta=1.0$ aumenta la proporción de puntos que no convergen dentro del límite de 30 iteraciones. Sin embargo, no afirmamos la existencia de caos ni una caracterización formal de conjuntos de Julia porque se trata de un experimento numérico sobre una malla discretizada finita y acotada; los puntos no convergidos simplemente no alcanzaron la cota en 30 iteraciones.

### P8. ¿Cómo conecta este proyecto con Ciencia de Datos y Machine Learning?
* **Respuesta:**  
  En aprendizaje de máquinas, el entrenamiento de modelos consiste en optimizar una función de pérdida buscando puntos estacionarios donde el gradiente se anula: $\nabla L(\boldsymbol{\theta}) = \mathbf{0}$.  
  En arquitecturas profundas o modelos con colinealidad, los paisajes de pérdida contienen valles planos degenerados y puntos de ensilladura donde la matriz Hessiana (el Jacobiano del gradiente) tiene autovalores nulos o casi nulos. Esto reproduce de manera análoga el comportamiento de una raíz múltiple ($g'(x)\approx 0$), provocando que optimizadores estándar se estanquen.  
  Aunque aclaramos que nuestro proyecto resuelve problemas escalares unidimensionales con multiplicidad conocida y no constituye una aplicación directa inmediata a redes neuronales, aporta el fundamento conceptual sobre cómo las formulaciones libres de derivadas de orden superior permiten superar zonas de aplanamiento sin calcular costosas matrices de derivadas.
