# Guía de Sustentación Oral y Defensa Técnica — Métodos Numéricos
**Universidad Externado de Colombia — Pregrado en Ciencia de Datos**  
**Proyecto Integrador: Métodos Numéricos (Fase 3 — Entrega Final)**  
**Artículo Base:** *Derivative-free optimal multiple-root finding family of iterative methods*, J. H. Jerezano, F. I. Chicharro, N. Garrido-Sáez (*Computational and Applied Mathematics*, 2026)  
**Equipo:** Ailyn Sofía Gómez Rodríguez, Julián Steven Duarte, Julián Camilo Jiménez Rodríguez  
**Docente:** Edwin Fernando Muñoz Chipatecua  
**Duración Total Estimada:** 12 Minutos (Video / Defensa Oral)

---

## 1. Cronograma y Distribución de Roles por Diapositiva (Total: 12 Minutos)

Para asegurar una participación equitativa y demostrar dominio conceptual colectivo según los criterios de la rúbrica institucional (Sección 8.5), la exposición se organiza diapositiva por diapositiva con tiempos y roles calibrados:

| Diapositiva | Título en Pantalla | Ponente | Tiempo | Mensaje Central y Acción |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Portada | Ailyn Sofía Gómez | **20 s** | Presentación institucional del equipo, docente, artículo base y objetivo general. |
| **2** | El Problema: Raíces Múltiples y Régimen de Newton | Ailyn Sofía Gómez | **1 min** | Multiplicidad $m>1$, convergencia lineal de Newton con factor $(m-1)/m$, costo de $g'(x)$. |
| **3** | Familia Libre de Derivadas (Jerezano et al., 2026) | Ailyn Sofía Gómez | **1 min 30 s** | Algoritmo predictor-corrector, Teorema 2, fórmulas M1/M2, nota de absorción y logaritmo. |
| **4** | Conjetura y Optimalidad de Kung-Traub | Ailyn Sofía Gómez | **1 min** | Saturación de la cota $p\le 2^{d-1}$ ($d=3 \implies p=4$), índice $\mathcal{I}\approx 1.587$ como medida teórica. |
| **5** | Estabilidad y Dinámica Compleja en $\mathbb{C}$ | Julián Steven Duarte | **1 min 15 s** | Gráfica en $[-2,2]^2$, raíz superatractora $R'(1)=0$, comparación de $\beta=0.01$ vs $\beta=1.0$. |
| **6** | Metodología Computacional y Precisión Finita | Julián Steven Duarte | **1 min** | `mpmath` a 150 dígitos, criterio dual estricto, detección de absorción ($w_k == x_k$). |
| **7** | Resultados Experimentales y Contraste | Julián Camilo Jiménez | **1 min 30 s** | Tabla de resultados, conteo $1+3k+1$ en M1/M2, justificación de 5 iteraciones en $g_1$ vs 7 del paper. |
| **8** | Hallazgo en $g_3$ ($m=4$) y Validación de ACOC | Julián Camilo Jiménez | **1 min** | Error $> \mathrm{TOL}$ en $g_3$ por contracción de potencia 4, ACOC canónico vs distorsión transitoria (8.81). |
| **9** | Extensión a Sistemas No Lineales $2\times 2$ (Broyden) | Julián Camilo Jiménez | **1 min** | Tabla $2\times 2$, Broyden actualiza Jacobiano en $O(n^2)$ sin derivadas pero resuelve en $O(n^3)$. |
| **10** | Conexión con Ciencia de Datos y Optimización | Julián Camilo Jiménez | **40 s** | Puntos estacionarios $\nabla L=\mathbf{0}$, autovalores nulos de Hessiana y rigor conceptual de la analogía. |
| **11** | Conclusiones y Trabajo Futuro | Julián Camilo Jiménez | **50 s** | Conclusiones acotadas, limitación de conocer $m$, trabajo futuro y apertura de preguntas. |

---

## 2. Guion Verbal Adaptado Diapositiva por Diapositiva

### Bloque 1: Planteamiento, Métodos y Fundamentación Teórica
**Ponente:** Ailyn Sofía Gómez Rodríguez  
**Tiempo total del bloque:** 3:50 minutos  
**Diapositivas:** 1, 2, 3 y 4

---

#### Diapositiva 1: Portada
* **Tiempo:** 20 segundos
* **Texto en pantalla:** *Título del proyecto, integrantes, docente, pregrado e institución.*
* **Guion verbal:**
> *"¡Buenos días a todos! Bienvenidos a la sustentación de la fase final de nuestro proyecto integrador en Métodos Numéricos. Nuestro trabajo se titula 'Familia Óptima Libre de Derivadas para Raíces Múltiples', basado en el artículo científico de Jerezano, Chicharro y Garrido-Sáez publicado en 2026. El equipo está conformado por Julián Steven Duarte, Julián Camilo Jiménez y quien les habla, Ailyn Sofía Gómez, bajo la tutoría del profesor Edwin Fernando Muñoz Chipatecua."*

---

#### Diapositiva 2: 1. El Problema: Raíces Múltiples y Régimen de Newton
* **Tiempo:** 1 minuto (0:20 a 1:20)
* **Texto en pantalla:** *Definición de multiplicidad $m>1$, colapso lineal de Newton con razón $(m-1)/m$, y costo de Newton modificado.*
* **Guion verbal:**
> *"Al resolver ecuaciones no lineales $g(x)=0$, surge una patología matemática severa cuando la raíz buscada $\alpha$ posee multiplicidad conocida $m > 1$. En estos puntos, tanto la función como sus primeras $m-1$ derivadas se anulan simultáneamente.
> 
> Es un error común asumir que el método de Newton clásico falla únicamente porque la derivada tiende a cero; la razón matemática de fondo es que, para una raíz de multiplicidad $m > 1$, Newton clásico presenta una convergencia estrictamente lineal, gobernada por el factor asintótico de error $C = \frac{m-1}{m}$. Por ejemplo, si la multiplicidad es dos, en cada paso el error solo se reduce a la mitad.
> 
> Aunque el método de Newton modificado recupera el orden cuadrático multiplicando el paso por $m$, exige calcular analíticamente la derivada $g'(x)$. En modelos complejos de ciencia de datos, esta derivada suele ser computacionalmente prohibitiva o analíticamente inaccesible, lo que motiva el diseño de esquemas libres de derivadas."*

---

#### Diapositiva 3: 2. Familia Libre de Derivadas (Jerezano et al., 2026)
* **Tiempo:** 1 minuto 30 segundos (1:20 a 2:50)
* **Texto en pantalla:** *Ecuaciones del predictor-corrector, condiciones del Teorema 2, funciones M1 y M2, notas de implementación.*
* **Guion verbal:**
> *"Para superar esta barrera, Jerezano, Chicharro y Garrido-Sáez propusieron en 2026 un esquema predictor-corrector de dos pasos sin derivadas. Primero introducen una perturbación cuadrática adaptativa $w_k = x_k + \beta [g(x_k)]^2$, aproximan la pendiente mediante la diferencia dividida secante $D_k = g[w_k, x_k]$, y construyen el punto intermedio $y_k$.
> 
> El paso corrector evalúa la variable $t_k = (g(y_k)/g(x_k))^{1/m}$ a través de una función de peso $H(t)$. De acuerdo con el Teorema 2 del artículo, para alcanzar orden de convergencia cuatro se deben satisfacer rigurosamente cuatro condiciones: $H(0)=1$, $H'(0)=1$, $H''(0)=4$ y $|H'''(0)| < \infty$.
> 
> En nuestro proyecto implementamos las dos variantes estudiadas por los autores:
> - M1, de ponderación polinomial cuadrática: $H_1(t) = 1 + t + 2t^2$, donde su tercera derivada en cero es $0 < \infty$.
> - M2, de ponderación racional: $H_2(t) = \frac{1-t}{1-2t}$, cuya tercera derivada en cero es $24 < \infty$ y presenta un polo en $t = 1/2$.
> 
> Destacamos una precisión metodológica clave: en la implementación práctica, la condición $\beta \neq 0$ no garantiza por sí sola que $w_k \neq x_k$, ya que en precisión finita puede ocurrir absorción numérica de la perturbación. Asimismo, para evaluar la potencia fraccionaria $t_k$ cuando el cociente toma valores negativos en etapas transitorias, utilizamos la rama principal del logaritmo complejo, reconociendo el corte de rama sobre el semieje real negativo."*

---

#### Diapositiva 4: 3. Conjetura y Optimalidad de Kung-Traub
* **Tiempo:** 1 minuto (2:50 a 3:50)
* **Texto en pantalla:** *Conjetura de Kung-Traub ($p\le 2^{d-1}$), tabla de índices de eficiencia $\mathcal{I} = p^{1/d}$, precisión conceptual.*
* **Guion verbal:**
> *"La fundamentación teórica de estos métodos se sustenta en la conjetura de Kung y Traub de 1974, la cual establece que un método iterativo multipaso sin memoria con $d$ evaluaciones funcionales por ciclo tiene un orden máximo $p \le 2^{d-1}$.
> 
> En la familia de Jerezano et al., cada paso evalúa exactamente tres funciones escalares ($g(x_k), g(w_k), g(y_k)$) y ninguna derivada ($d=3$). Por tanto, la cota superior teórica es $2^{3-1} = 4$. Bajo las condiciones establecidas en el Teorema 2, la familia alcanza orden cuatro y satura la cota de Kung-Traub, considerándose un método óptimo.
> 
> Como vemos en la tabla comparativa, su índice de eficiencia teórica es $\mathcal{I} = 4^{1/3} \approx 1.587$, que supera al $1.414$ de Newton modificado y Steffensen. Es fundamental precisar con rigor que este índice es una medida teórica basada en evaluaciones por paso; no implica necesariamente menores tiempos de ejecución en CPU en una implementación concreta. A continuación, mi compañero Julián Duarte explicará la dinámica compleja y la metodología computacional."*

---

### Bloque 2: Estabilidad Dinámica, Metodología y Criterios Numéricos
**Ponente:** Julián Steven Duarte  
**Tiempo total del bloque:** 2:15 minutos  
**Diapositivas:** 5 y 6

---

#### Diapositiva 5: 4. Estabilidad y Dinámica Compleja en $\mathbb{C}$ (Sección 3)
* **Tiempo:** 1 minuto 15 segundos (3:50 a 5:05)
* **Texto en pantalla:** *Gráfica `dinamica_compleja_m1_m2.png`, operador $R(z,\beta)$, punto fijo superatractor $R'(1)=0$, efecto de $\beta$.*
* **Guion verbal:**
> *"Muchas gracias, Ailyn. Para comprender el papel del parámetro libre $\beta$, el artículo examina la dinámica en el plano complejo $\mathbb{C}$ sobre el polinomio cuadrático canónico con raíz doble $p(z) = (z-1)^2$, donde $m=2$. Al aplicar el esquema, se obtiene un operador racional de punto fijo $z_{k+1} = R(z, \beta)$. En la raíz exacta $z^* = 1$, la derivada del operador vale exactamente cero ($R'(1, \beta) = 0$), lo que demuestra analíticamente que la raíz es un punto fijo superatractor, garantizando convergencia local de orden superior en su vecindad.
> 
> Como muestra la figura, generamos una malla computacional de $350 \times 350$ puntos en el dominio acotado $[-2, 2] \times [-2, 2]$ con un límite de 30 iteraciones. En la malla examinada, con $\beta = 0.01$ una mayor proporción de puntos alcanza el criterio de convergencia frente al caso con $\beta = 1.0$, donde aumentan los puntos que no convergen dentro de la cota fijada. Aclaramos con total honestidad técnica que este experimento delimita cuencas numéricas finitas bajo una discretización específica; no constituye una demostración de caos ni una caracterización formal exhaustiva de los conjuntos de Fatou y Julia."*

---

#### Diapositiva 6: 5. Metodología Computacional y Manejo de Patologías
* **Tiempo:** 1 minuto (5:05 a 6:05)
* **Texto en pantalla:** *Precisión de 150 dígitos con mpmath, criterio dual estricto, mecánica exacta de absorción numérica ($w_k = x_k$).*
* **Guion verbal:**
> *"En cuanto a la implementación computacional en Python, fijamos la biblioteca `mpmath` con aritmética de 150 dígitos decimales (`dps = 150`), construyendo las constantes decimales desde texto para evitar sesgos binarios de redondeo.
> 
> Para detener los métodos de forma robusta, diseñamos un criterio de parada dual estricto: exigimos simultáneamente que el paso completado $|\Delta x_k| = |x_{k+1}-x_k| < 10^{-25}$ y que el residuo $|g(x_{k+1})| < 10^{-25}$.
> 
> Un aspecto crítico que descubrimos en la experimentación fue el mecanismo de absorción numérica: la perturbación es cuadrática en el residuo, $\beta [g(x_k)]^2$. Cuando esta perturbación es tan pequeña que, al sumarse a $x_k$, la aritmética de precisión finita produce el mismo valor representable, el código detecta la igualdad computacional $w_k = x_k$. Lejos de esconder este fenómeno o reemplazarlo arbitrariamente por una derivada, nuestro código captura la igualdad y detiene controladamente la corrida clasificándola como `Estancamiento w=x` por imposibilidad de formar la secante. Doy paso a Julián Jiménez para el análisis de resultados."*

---

### Bloque 3: Resultados, Benchmarks, Sistemas, Ciencia de Datos y Cierre
**Ponente:** Julián Camilo Jiménez Rodríguez  
**Tiempo total del bloque:** 5:00 minutos  
**Diapositivas:** 7, 8, 9, 10 y 11

---

#### Diapositiva 7: 6. Resultados Experimentales (150 dígitos, $\mathrm{TOL}=10^{-25}$, $\beta=0.01$)
* **Tiempo:** 1 minuto 30 segundos (6:05 a 7:35)
* **Texto en pantalla:** *Tabla de resultados con paso $|\Delta x_k|$, nota aclaratoria de casos representativos y conteo $1+3k+1$, contraste con el paper.*
* **Guion verbal:**
> *"Gracias, Julián. Proyectamos en la Diapositiva 7 los resultados obtenidos en las corridas deterministas con 150 dígitos y tolerancia $10^{-25}$. Como se indica en la nota, mostramos casos representativos; el archivo CSV adjunto conserva todas las combinaciones completas.
> 
> En el problema $g_1$ (polinomio de Van der Waals con raíz doble en $1.75$ y semilla $1.9$), M1 converge en 5 iteraciones con un error absoluto de $1.32\times 10^{-35}$ y un residuo de $10^{-72}$, superando en pasos a Newton modificado y Steffensen, que requirieron 8 iteraciones.
> 
> Es fundamental transparentar el conteo de evaluaciones: la fórmula $1+3k+1$ aplica específicamente a M1 y M2; corresponde a evaluar $g(x_0)$ al inicio, $3$ funciones en cada uno de los $k$ pasos, y una llamada de comprobación final $g(x_{\mathrm{final}})$ ejecutada explícitamente tras salir del ciclo para registrar el residuo de parada en memoria.
> 
> Respecto a la comparación con el artículo base: en $g_1$, M1 satisface nuestro criterio dual en 5 iteraciones, frente a las 7 reportadas por los autores. Esta diferencia no demuestra una mayor eficiencia algorítmica: obedece a que usamos 150 dígitos y una tolerancia de $10^{-25}$, menos estricta que la cota de $10^{-200}$ con 4000 dígitos empleada en el artículo original."*

---

#### Diapositiva 8: 7. Hallazgo en $g_3$ ($m=4$) y Comportamiento del ACOC
* **Tiempo:** 1 minuto (7:35 a 8:35)
* **Texto en pantalla:** *Explicación analítica del colapso de residuo en $g_3$, estado `Criterio dual; error > TOL`, ACOC canónico vs distorsión transitoria.*
* **Guion verbal:**
> *"En la Diapositiva 8 exponemos el hallazgo metodológico más relevante del proyecto: el comportamiento ante raíces de multiplicidad cuatro en el polinomio $g_3$. Cerca de la raíz $\alpha=3$, la función se comporta aproximadamente como $g_3(x) \approx -80(x-3)^4$. Debido a la potencia cuarta, un error de $10^{-18}$ produce un residuo del orden de $10^{-72}$, haciendo que el paso se contraiga por debajo de $10^{-59}$.
> 
> Nuestra implementación detiene el algoritmo a las 3 iteraciones porque cumple formalmente la tolerancia dual de $10^{-25}$. Sin embargo, al contrastar frente a la raíz exacta $\alpha=3$, la distancia real es de $3.71\times 10^{-18} > 10^{-25}$. Con honestidad técnica, no clasificamos esta corrida como un éxito de convergencia superior, sino como `Criterio dual; error > TOL`, distinguiendo la parada operativa de la precisión efectiva.
> 
> Paralelamente, validamos el cálculo de ACOC: en la raíz simple de $x^3-x-2=0$, Newton arrojó $\mathrm{ACOC} \approx 2.0000$ y la secante $\mathrm{ACOC} \approx 1.6162$, muy cercano al orden teórico de la razón áurea ($1.6180$). No obstante, en raíces múltiples bajo pocas iteraciones (3 a 5 pasos), las variaciones transitorias distorsionan el cociente logarítmico (arrojando por ejemplo 8.81 en M1), lo cual demuestra que el ACOC es un diagnóstico local asintótico y no prueba un orden superior a cuatro."*

---

#### Diapositiva 9: 8. Extensión a Sistemas No Lineales $2\times 2$ (Broyden)
* **Tiempo:** 1 minuto (8:35 a 9:35)
* **Texto en pantalla:** *Sistema $2\times 2$, tabla comparativa entre Newton multivariable y Broyden, precisión del costo computacional.*
* **Guion verbal:**
> *"Como experimento complementario vinculado a los temas de la Semana 9 del curso, exploramos la resolución de un sistema no lineal $2\times 2$. Newton multivariable convergió en 5 iteraciones alcanzando un residuo de $10^{-15}$, pero requirió evaluar 20 derivadas parciales Jacobianas. Por su parte, el método secante de Broyden alcanzó la misma precisión en 10 iteraciones sin necesidad de derivadas analíticas.
> 
> Es indispensable precisar la estructura del costo computacional: Broyden actualiza la aproximación del Jacobiano mediante una corrección de rango uno de costo $O(n^2)$ y evita calcular $n^2$ derivadas analíticas, aunque la resolución de los sistemas lineales densos continúa teniendo un costo de orden $O(n^3)$ por iteración. Este ensayo ilustra el compromiso práctico entre número de iteraciones y costo por evaluación que fundamenta los métodos sin derivadas."*

---

#### Diapositiva 10: 9. Conexión con Ciencia de Datos y Optimización
* **Tiempo:** 40 segundos (9:35 a 10:15)
* **Texto en pantalla:** *Condición $\nabla L(\boldsymbol{\theta})=\mathbf{0}$, autovalores nulos en la Hessiana, relevancia conceptual sin sobrestimaciones.*
* **Guion verbal:**
> *"En Ciencia de Datos, el entrenamiento de modelos de Machine Learning consiste en encontrar puntos estacionarios donde el gradiente de pérdida se anula: $\nabla L(\boldsymbol{\theta}) = \mathbf{0}$.
> 
> En regiones mal condicionadas, la matriz Hessiana puede presentar autovalores cercanos a cero, lo que dificulta significativamente ciertos métodos de optimización. Estos escenarios motivan el estudio de puntos críticos degenerados, aunque aclaramos con rigor que una Hessiana singular no implica necesariamente una raíz de multiplicidad $m>1$. Los métodos estudiados ofrecen una valiosa referencia teórica para investigar algoritmos que aprovechen multiplicidad, cuya aplicación a pérdidas de alta dimensión requerirá extensiones y validaciones adicionales."*

---

#### Diapositiva 11: 10. Conclusiones y Trabajo Futuro
* **Tiempo:** 50 segundos (10:15 a 11:05 — dejando ~1 min para margen y cierre)
* **Texto en pantalla:** *Síntesis de aportes, limitación del conocimiento de $m$, trabajo futuro y agradecimientos.*
* **Guion verbal:**
> *"Para concluir: se implementó una familia de métodos cuyo orden teórico es cuatro y que alcanza la cota de Kung-Traub bajo las condiciones establecidas por el artículo. En la malla y el límite de iteraciones examinados, $\beta=0.01$ mostró un comportamiento de convergencia más favorable que $\beta=1.0$. Identificamos y corregimos con transparencia la interpretación en $g_3$ distinguiendo la parada operativa de la precisión real.
> 
> Como principal limitación, destacamos que el método asume conocida la multiplicidad exacta $m$, la cual no se conoce a priori en aplicaciones reales. Como trabajo futuro, planteamos diseñar estimadores adaptativos dinámicos de $m$ durante las etapas iniciales y explorar extensiones libres de derivadas para optimización a gran escala. Agradecemos al docente Edwin Fernando Muñoz por su retroalimentación y abrimos la sesión de preguntas. ¡Muchas gracias!"*

---

## 3. Matriz Rápida de Defensa Técnica Diapositiva por Diapositiva

Ante cualquier interrupción o pregunta del docente, esta tabla resume la respuesta técnica inmediata:

| Diapositiva | Pregunta Probable del Docente | Respuesta Clave del Equipo |
| :---: | :--- | :--- |
| **2** | ¿Por qué Newton pierde el orden cuadrático? | Por la expansión de Taylor: el cociente $g(x)/g'(x) \approx \frac{1}{m}(x-\alpha)$, produciendo un error $x_{k+1}-\alpha = \frac{m-1}{m}(x_k-\alpha)$, lo que prueba analíticamente convergencia lineal con razón $(m-1)/m$. |
| **3** | ¿Por qué se estancó $M_2$ si $\beta \neq 0$? | $\beta \neq 0$ garantiza $w_k \neq x_k$ en $\mathbb{R}$, pero en aritmética finita de 150 dígitos, cuando el residuo decae a $10^{-86}$, $\beta g(x_k)^2$ es menor que la resolución relativa de $x_k$, produciendo $w_k == x_k$ por absorción. |
| **4** | ¿El orden 4 es incondicional? | No; depende de que se cumplan las hipótesis del Teorema 2 ($H(0)=1, H'(0)=1, H''(0)=4, |H'''(0)|<\infty$) y de convergencia en una vecindad local de la raíz. |
| **5** | ¿Demostraron que $\beta=1.0$ produce caos? | No. Es una observación acotada a la malla finita de $350\times 350$ en $[-2,2]^2$ donde en 30 iteraciones no convergieron; no constituye una demostración analítica de caos ni de conjuntos de Julia. |
| **6** | ¿Por qué el criterio dual es indispensable? | Porque en raíces múltiples el residuo decae como $(x-\alpha)^m$. En $m=4$, un error de $10^{-7}$ ya da residuo de $10^{-28}$. Evaluar solo residuo genera paradas falsas lejos de la raíz. |
| **7** | ¿M1 es superior al artículo porque tomó 5 pasos vs 7? | No. La diferencia se explica por las tolerancias de parada: usamos $10^{-25}$ con 150 dígitos, mientras que el artículo empleó $10^{-200}$ con 4000 dígitos. Nuestro criterio se satisface antes. |
| **8** | ¿Por qué $g_3$ no se clasifica como Convergió? | Porque cerca de $\alpha=3$, $g_3 \approx -80(x-3)^4$. Con error de $10^{-18}$, el residuo ya es $10^{-72}$ y el paso $10^{-60}$. Cumple el criterio dual operativo pero el error real supera $10^{-25}$. |
| **8** | ¿El ACOC de 8.81 significa orden 8? | No. El ACOC es una aproximación asintótica. Con 3 a 5 iteraciones drásticas, las variaciones transitorias distorsionan el cociente logarítmico, produciendo un valor espurio transitorio. |
| **9** | ¿Broyden reduce la complejidad total a $O(n^2)$? | No. Broyden actualiza el Jacobiano en $O(n^2)$ y evita evaluar derivadas, pero en cada paso continúa resolviendo un sistema lineal denso de orden $O(n^3)$. |
| **10** | ¿Una Hessiana singular prueba multiplicidad $m>1$? | No necesariamente. Una Hessiana mal condicionada señala direcciones planas degeneradas en la pérdida, pero no demuestra formalmente multiplicidad en el gradiente. La analogía es conceptual. |
| **11** | ¿Cuál es la limitación central del artículo? | Asumir que la multiplicidad $m$ se conoce a priori de manera exacta. Si se suministra un $m$ erróneo, el orden cuártico colapsa a orden lineal. |
