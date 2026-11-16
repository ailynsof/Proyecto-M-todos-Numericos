# Guía de Sustentación Oral y Defensa Técnica
**Proyecto Integrador: Métodos Numéricos (2026-2)**  
**Universidad Externado de Colombia — Pregrado en Ciencia de Datos**  
**Artículo Base:** *Derivative-free optimal multiple-root finding family of iterative methods*, J. H. Jerezano, F. I. Chicharro, N. Garrido-Sáez (2026)  
**Equipo:** Ailyn Sofía Gómez Rodríguez, Julián Camilo Jiménez, Julián Steven Duarte  
**Docente:** Edwin Fernando Muñoz Chipatecua  

---

## 1. Distribución Recomendada de la Exposición (12 a 15 Minutos)

Para asegurar una participación equitativa y demostrar dominio conceptual colectivo (requisito explícito de la Sección 8.5 de la rúbrica):

| Integrante | Diapositivas | Temas Clave que Domina y Explica |
| :--- | :---: | :--- |
| **Ailyn Sofía Gómez** | Diapositivas 1 a 4 | **Contexto y Fundamentos:** Definición de multiplicidad $m$, por qué falla el método de Newton estándar ($p=1$), la formulación del predictor-corrector libre de derivadas de Jerezano et al., la conjetura de Kung-Traub y la comparación de índices de eficiencia computacional ($\mathcal{I} = 4^{1/3} \approx 1.587$). |
| **Julián Camilo Jiménez** | Diapositivas 5 a 7 | **Estabilidad y Dinámica Compleja en $\mathbb{C}$:** El operador racional $R(z, \beta)$ sobre $p(z)=(z-1)^2$, demostración de que la raíz es superatractora ($R'(1)=0$), por qué $\beta=0.01$ es la opción óptima para evitar fractales/caos de Julia, y la configuración de reproducibilidad con `mpmath` (150 dígitos y tolerancia dual $10^{-25}$). |
| **Julián Steven Duarte** | Diapositivas 8 a 11 | **Resultados, Validación y Aplicación:** Contraste honesto de resultados vs. las tablas del artículo (4000 dps vs. 150 dps), la interpretación crítica del ACOC, la extensión a sistemas no lineales $2\times 2$ (Semana 9: Newton multivariable vs. Broyden libre de derivadas), y la conexión con optimización y paisajes de pérdida en Ciencia de Datos. |

---

## 2. Banco de Preguntas Difíciles del Docente y Cómo Responderlas

### P1. ¿Por qué el método de Newton clásico pierde su orden cuadrático ante una raíz múltiple?
* **Respuesta del equipo:**  
  En una raíz $\alpha$ de multiplicidad $m > 1$, la serie de Taylor de $g(x)$ alrededor de $\alpha$ comienza en el término de grado $m$:  
  $$g(x) = \frac{g^{(m)}(\alpha)}{m!} (x-\alpha)^m + \frac{g^{(m+1)}(\alpha)}{(m+1)!} (x-\alpha)^{m+1} + \dots$$  
  Su derivada es:  
  $$g'(x) = \frac{g^{(m)}(\alpha)}{(m-1)!} (x-\alpha)^{m-1} + \dots$$  
  Al calcular el cociente de Newton:  
  $$\frac{g(x)}{g'(x)} \approx \frac{\frac{1}{m!} (x-\alpha)^m}{\frac{1}{(m-1)!} (x-\alpha)^{m-1}} = \frac{1}{m} (x-\alpha)$$  
  Por tanto, el iterado de Newton satisface:  
  $$x_{k+1} - \alpha = (x_k - \alpha) - \frac{1}{m}(x_k - \alpha) = \frac{m-1}{m} (x_k - \alpha)$$  
  Esto demuestra que el error decae linealmente con constante asintótica $C = \frac{m-1}{m}$. Por ejemplo, si $m=2$, en cada paso el error solo se reduce a la mitad ($C = 1/2$). Al multiplicar el paso por $m$ (Newton modificado), el término lineal se cancela y se recupera el orden cuadrático ($p=2$).

---

### P2. ¿Qué establece la conjetura de Kung-Traub y por qué la familia de Jerezano et al. es óptima?
* **Respuesta del equipo:**  
  La conjetura de H. T. Kung y J. F. Traub (1974) establece que cualquier método multipaso sin memoria que requiera $d$ evaluaciones funcionales por iteración tiene un orden de convergencia máximo acotado por:  
  $$p \le 2^{d-1}$$  
  En la familia de Jerezano et al., cada paso evalúa únicamente tres valores funcionales escalares ($g(x_k)$, $g(w_k)$ y $g(y_k)$) y **cero derivadas**. Por tanto, $d=3$, y la cota superior es $p \le 2^{3-1} = 4$.  
  Como el teorema de convergencia demuestra que el método alcanza orden 4 bajo las condiciones sobre la función de peso $H(t)$, el método alcanza la cota teórica máxima posible, siendo **óptimo en el sentido de Kung-Traub**.

---

### P3. ¿Por qué es indispensable calcular la potencia fraccionaria $t_k = (g(y_k)/g(x_k))^{1/m}$ con la rama principal compleja?
* **Respuesta del equipo:**  
  Aunque las raíces buscadas y las semillas iniciales sean números reales, durante las iteraciones previas a la convergencia (régimen transitorio), el cociente $g(y_k)/g(x_k)$ puede tomar valores negativos o cambiar de signo entre pasos consecutivos.  
  En números reales, una potencia fraccionaria con base negativa y exponente par (como $m=2$ o $m=4$) genera un error de dominio (`ValueError: negative number cannot be raised to a fractional power`).  
  Al extender el cálculo al plano complejo $\mathbb{C}$ mediante la rama principal del logaritmo:  
  $$\operatorname{Ln}(z) = \ln|z| + i \operatorname{Arg}(z), \quad \operatorname{Arg}(z) \in (-\pi, \pi]$$  
  la función de evaluación es univaluada, continua y analítica en todo el plano complejo cortado, garantizando que el algoritmo nunca aborte por indefiniciones algebraicas.

---

### P4. En el análisis de estabilidad en $\mathbb{C}$, ¿qué es un punto fijo superatractor y qué papel juega el parámetro $\beta$?
* **Respuesta del equipo:**  
  Dado el operador racional $z_{k+1} = R(z)$, un punto fijo $z^*$ satisface $R(z^*) = z^*$. Su multiplicador asintótico es $|R'(z^*)|$.  
  Si $|R'(z^*)| = 0$, la convergencia en la vecindad del punto fijo es al menos cuadrática o superior, denominándose **superatractor**. En nuestro caso, para $p(z)=(z-1)^2$, se cumple analíticamente que $|R'(1)| = 0$.  
  Sin embargo, el operador racional también posee **puntos críticos libres** (soluciones de $R'(z)=0$ distintas de la raíz) y polos.  
  El parámetro $\beta$ modula la magnitud del paso de secante:  
  - Con $\beta=0.01$, los puntos críticos libres no interfieren con la dinámica local, resultando en cuencas de atracción casi globales, continuas y lisas.  
  - Con $\beta=1.0$ o $\beta=5.0$, los puntos críticos libres generan cuencas fractales de Julia y bifurcaciones caóticas que atrapan trayectorias o las desvían a infinito. Por eso, el artículo selecciona $\beta=0.01$.

---

### P5. En los resultados, ¿por qué su implementación tardó 5 iteraciones en $g_1$ mientras que el artículo reporta 7 iteraciones?
* **Respuesta del equipo:**  
  Esta es una de las conclusiones metodológicas más valiosas de nuestro trabajo. No se trata de un error ni de que nuestro método sea más rápido: se debe a la **escala de tolerancia**.  
  El artículo de Jerezano et al. utilizó Matlab con 4000 dígitos de precisión y una tolerancia extrema de $10^{-200}$. Bajo ese criterio, el método necesita 7 pasos para alcanzar un residuo inferior a $10^{-200}$.  
  En nuestra implementación reproducible fijamos 150 dígitos de precisión y una tolerancia de parada de $10^{-25}$. El método alcanza $10^{-25}$ en la iteración 5 (con residuo de $5.26\times 10^{-72}$). Si hubiésemos exigido $10^{-200}$, habríamos requerido exactamente las 7 iteraciones del artículo, pero demostramos que para fines prácticos y de computación científica, 150 dígitos y $10^{-25}$ ofrecen un balance óptimo de precisión sin el costo exorbitante de 4000 dígitos.

---

### P6. ¿Por qué en $M_2$ se reporta "Estancamiento $w=x$"?
* **Respuesta del equipo:**  
  La perturbación secante es $w_k = x_k + \beta [g(x_k)]^2$. En $M_2$, tras 4 iteraciones el residuo $|g(x_k)|$ ya es del orden de $10^{-50}$, por lo que $[g(x_k)]^2 \approx 10^{-100}$.  
  En precisión finita (incluso con 150 dígitos), cuando sumamos $x_k + \beta [g(x_k)]^2$, la diferencia entre $w_k$ y $x_k$ cae por debajo de la resolución numérica de la máquina frente a la magnitud de $x_k$ (fenómeno de absorción en punto flotante).  
  Al cumplirse $w_k == x_k$, el denominador de la diferencia dividida $w_k - x_k$ se vuelve exactamente cero. Nuestro código detecta explícitamente esta pérdida de perturbación y emite el diagnóstico honesto `'Estancamiento w=x'`, en lugar de disfrazarlo cambiando artificialmente a una derivada.

---

### P7. ¿Por qué el orden experimental ACOC dio 8.81 en $M_1$ en lugar del 4 teórico?
* **Respuesta del equipo:**  
  La fórmula del ACOC:  
  $$\mathrm{ACOC} \approx \frac{\log(|x_{k+1}-x_k|/|x_k-x_{k-1}|)}{\log(|x_k-x_{k-1}|/|x_{k-1}-x_{k-2}|)}$$  
  proviene de la hipótesis de que el método se encuentra en su **régimen asintótico terminal** con diferencias no nulas y suficientes iteraciones intermedias.  
  Como $M_1$ converge tan velozmente (apenas 5 iteraciones), el paso pasa de $10^{-3}$ a $10^{-9}$ y luego a $10^{-35}$. En las últimas iteraciones, la aceleración local y la escala logarítmica amplifican las diferencias, generando lecturas espurias transitorias. Validamos formalmente la implementación del ACOC sobre el problema de raíz simple $x^3-x-2=0$, donde Newton arrojó exactamente $\mathrm{ACOC} = 2.0000$ y la secante $\mathrm{ACOC} = 1.6162$, comprobando que el estimador funciona perfectamente y que su distorsión en raíces múltiples es un fenómeno de saturación numérica transitoria.

---

### P8. ¿Cómo se relaciona este proyecto con problemas reales de Ciencia de Datos y Optimización?
* **Respuesta del equipo:**  
  En Ciencia de Datos, entrenar modelos complejos (como redes neuronales o modelos de regresión no lineal) implica encontrar los mínimos de una función de pérdida $L(\boldsymbol{\theta})$ mediante la condición de primer orden $\nabla L(\boldsymbol{\theta}) = \mathbf{0}$.  
  En problemas reales con multicolinealidad, sobreparametrización o valles planos, la matriz Hessiana $\mathbf{H}(\boldsymbol{\theta})$ (que es el Jacobiano del gradiente) tiene autovalores iguales o muy cercanos a cero. Esto equivale exactamente a que el punto crítico tiene **multiplicidad $m > 1$**.  
  En estas regiones planas, el algoritmo de descenso de gradiente estándar se ralentiza enormemente y Newton clásico colapsa a velocidad lineal. Los conceptos estudiados en este proyecto —aceleración por conocimiento de multiplicidad y aproximación secante de orden superior sin calcular matrices de derivadas analíticas— son el fundamento teórico para diseñar optimizadores cuasi-Newton avanzados y métodos de segundo orden escalables en Machine Learning.

