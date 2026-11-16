# Guía de Sustentación Oral y Defensa Técnica — Métodos Numéricos
**Universidad Externado de Colombia — Pregrado en Ciencia de Datos**  
**Proyecto Integrador: Métodos Numéricos (Fase 3 — Entrega Final)**  
**Artículo Base:** *Derivative-free optimal multiple-root finding family of iterative methods*, J. H. Jerezano, F. I. Chicharro, N. Garrido-Sáez (*Computational and Applied Mathematics*, 2026)  
**Equipo:** Ailyn Sofía Gómez Rodríguez, Julián Steven Duarte, Julián Camilo Jiménez Rodríguez  
**Docente:** Edwin Fernando Muñoz Chipatecua  
**Duración Total Estimada:** 12 Minutos (Video / Defensa Oral)

---

## 1. Distribución de la Exposición y Cronograma (Aprox. 12 Minutos)

Para asegurar una participación equitativa y demostrar dominio conceptual colectivo según los criterios de la rúbrica institucional (Sección 8.5), la sustentación se organiza diapositiva por diapositiva con tiempos rigurosamente asignados:

| Diapositiva | Integrante Responsable | Tiempo | Objetivo Pedagógico y Técnico |
| :--- | :--- | :---: | :--- |
| **1. Portada** | Ailyn Sofía Gómez | 20 s | Presentar al equipo, el docente, el artículo base y el marco del proyecto. |
| **2. El Problema** | Ailyn Sofía Gómez | 1 min | Explicar la multiplicidad $m>1$, por qué Newton clásico presenta convergencia lineal con factor $(m-1)/m$, y el costo de la derivada en Newton modificado. |
| **3. Familia M1/M2** | Ailyn Sofía Gómez | 1 min 30 s | Explicar el algoritmo predictor-corrector, las condiciones del Teorema 2, las funciones $M_1$ y $M_2$, y advertir sobre absorción numérica ($w_k=x_k$) y rama principal en $\mathbb{C}$. |
| **4. Kung-Traub** | Ailyn Sofía Gómez | 1 min | Justificar la saturación de la cota óptima ($d=3 \implies p=4$) bajo el Teorema 2 y aclarar que el índice $\mathcal{I}\approx 1.587$ es una medida teórica que no garantiza menor tiempo CPU. |
| **5. Dinámica compleja** | Julián Steven Duarte | 1 min 15 s | Mostrar el plano visual en $[-2,2]^2$, explicar la raíz superatractora ($R'(1)=0$) y señalar que con $\beta=0.01$ una mayor proporción de puntos alcanza convergencia en la malla examinada. |
| **6. Implementación** | Julián Steven Duarte | 1 min | Explicar la precisión de 150 dígitos en `mpmath`, el criterio dual estricto, y el mecanismo exacto de absorción en precisión finita ($w_k=x_k$). |
| **7. Resultados** | Julián Camilo Jiménez | 1 min 30 s | Presentar la tabla de resultados, aclarar que $1+3k+1$ aplica a M1/M2, y justificar que 5 pasos en $g_1$ frente a 7 del artículo se debe a una tolerancia menos estricta ($10^{-25}$ vs $10^{-200}$). |
| **8. ACOC y $g_3$** | Julián Camilo Jiménez | 1 min | Explicar el hallazgo crucial en $g_3$ ($m=4$) como terminación por criterio dual y no convergencia plena, y aclarar que el ACOC de 8.81 es un efecto transitorio en pocas iteraciones. |
| **9. Broyden** | Julián Camilo Jiménez | 1 min | Mostrar la extensión $2\times 2$, destacando que Broyden actualiza el Jacobiano en $O(n^2)$ sin derivadas pero sigue resolviendo sistemas lineales densos en $O(n^3)$. |
| **10. Ciencia de Datos** | Julián Camilo Jiménez | 40 s | Conectar con puntos estacionarios $\nabla L=\mathbf{0}$, autovalores nulos en la Hessiana y la cautela de que una Hessiana singular no implica necesariamente multiplicidad $m>1$. |
| **11. Conclusiones** | Julián Camilo Jiménez | 50 s | Concluir con rigor acotado a las observaciones, señalar la limitación de conocer $m$, plantear el trabajo futuro y abrir la sesión de preguntas. |

---

## 2. Guion Borrador Completo de Sustentación

### Bloque 1: Planteamiento, Métodos y Fundamentación Teórica
**Ponente:** Ailyn Sofía Gómez Rodríguez  
**Tiempo estimado:** 3:50 minutos  
**Diapositivas:** 1 a 4

> *(Diapositiva 1 — 20 s)*  
> *"¡Buenos días a todos! Bienvenidos a la sustentación de la fase final de nuestro proyecto integrador en Métodos Numéricos. Nuestro trabajo se titula 'Familia Óptima Libre de Derivadas para Raíces Múltiples', basado en el artículo científico de Jerezano, Chicharro y Garrido-Sáez (2026). El equipo está integrado por Julián Duarte, Julián Jiménez y quien les habla, Ailyn Gómez, bajo la tutoría del profesor Edwin Fernando Muñoz.*
> 
> *(Diapositiva 2 — 1 min)*  
> *En análisis numérico y ciencia de datos, resolver $g(x)=0$ se complica severamente cuando la raíz $\alpha$ posee multiplicidad $m > 1$. En estos casos, la función y sus derivadas hasta el orden $m-1$ se anulan simultáneamente. Para una raíz de multiplicidad $m > 1$, el método de Newton clásico presenta una convergencia estrictamente lineal, con un factor asintótico de error $C = \frac{m-1}{m}$. Por ejemplo, si $m=2$, en cada paso el error solo se reduce a la mitad. Aunque el método de Newton modificado restaura el orden cuadrático ($p=2$), requiere conocer y evaluar la derivada analítica $g'(x)$, la cual resulta computacionalmente muy costosa o inaccesible en modelos complejos.*
> 
> *(Diapositiva 3 — 1 min 30 s)*  
> *Para resolver esta limitación, el artículo de Jerezano et al. (2026) formula un esquema predictor-corrector de dos pasos sin derivadas. El algoritmo introduce una perturbación cuadrática adaptativa $w_k = x_k + \beta [g(x_k)]^2$, evalúa la pendiente secante $D_k = g[w_k, x_k]$, y calcula el punto intermedio $y_k$.*
> 
> *El paso corrector evalúa la variable $t_k = (g(y_k)/g(x_k))^{1/m}$ mediante una función de peso $H(t)$. De acuerdo con el Teorema 2 del artículo, para alcanzar orden cuatro se requieren cuatro condiciones: $H(0)=1$, $H'(0)=1$, $H''(0)=4$ y $|H'''(0)| < \infty$. Analizamos las dos variantes del artículo:*
> - *M1 (polinomial cuadrática): $H_1(t) = 1 + t + 2t^2$, donde $H_1'''(0) = 0 < \infty$.*
> - *M2 (racional): $H_2(t) = \frac{1-t}{1-2t}$, con $H_2'''(0) = 24 < \infty$ y un polo en $t = 1/2$.*
> 
> *Es crucial notar que en la implementación práctica, la condición $\beta \neq 0$ no evita que $w_k = x_k$ ocurra por absorción numérica de la perturbación. Asimismo, la variable $t_k$ se calcula mediante la rama principal del logaritmo complejo para permitir potencias con base negativa en etapas transitorias, reconociendo el corte de rama sobre el semieje real negativo.*
> 
> *(Diapositiva 4 — 1 min)*  
> *La conjetura de Kung-Traub (1974) establece que el orden de convergencia máximo para un método multipaso sin memoria con $d$ evaluaciones funcionales es $p \le 2^{d-1}$. Como este esquema realiza exactamente 3 evaluaciones de función ($g(x_k), g(w_k), g(y_k)$) y cero derivadas ($d=3$), la cota teórica es $p \le 4$. Bajo las condiciones del Teorema 2, la familia alcanza orden cuatro y satura la cota de Kung-Traub, con un índice de eficiencia computacional teórico $\mathcal{I} = 4^{1/3} \approx 1.587$, frente a $1.414$ de Newton modificado. Precisamos con rigor que este índice es una medida teórica; no implica necesariamente menores tiempos de ejecución en una implementación concreta. Doy la palabra a Julián Duarte."*

---

### Bloque 2: Estabilidad Dinámica, Metodología y Criterios Numéricos
**Ponente:** Julián Steven Duarte  
**Tiempo estimado:** 2:15 minutos  
**Diapositivas:** 5 a 6

> *(Diapositiva 5 — 1 min 15 s)*  
> *"Muchas gracias, Ailyn. Para estudiar la estabilidad de los métodos, el artículo analiza el comportamiento en el plano complejo sobre el polinomio cuadrático canónico con raíz doble $p(z) = (z-1)^2$ ($m=2$). Esto genera un operador racional de punto fijo $z_{k+1} = R(z, \beta)$. En la raíz $z^* = 1$, la derivada analítica vale exactamente cero ($R'(1, \beta) = 0$), lo que clasifica a la raíz como un punto fijo superatractor, garantizando convergencia local de orden superior en su vecindad.*
> 
> *En nuestra experimentación, construimos una malla computacional de $350 \times 350$ puntos en el dominio acotado $[-2, 2] \times [-2, 2]$ con un límite de 30 iteraciones. Observamos que con $\beta = 0.01$ una mayor proporción de puntos alcanza el criterio de convergencia en la malla examinada, según los resultados obtenidos, mientras que con $\beta = 1.0$ aumentan los puntos que no logran converger dentro de 30 pasos. Es importante subrayar con rigor científico que esta exploración visual delimita cuencas numéricas finitas bajo parámetros específicos, sin constituir una caracterización analítica completa de los conjuntos de Fatou y Julia.*
> 
> *(Diapositiva 6 — 1 min)*  
> *Pasando a la metodología computacional, configuramos `mpmath` en Python con aritmética de alta precisión fijada en 150 dígitos decimales (`dps = 150`) para evitar redondeos prematuros.*
> 
> *Para detener las iteraciones, implementamos un criterio de parada dual estricto: exigimos simultáneamente que el paso $|\Delta x_k| = |x_{k+1}-x_k| < 10^{-25}$ y que el residuo $|g(x_{k+1})| < 10^{-25}$.*
> 
> *Un aporte técnico fundamental de nuestra auditoría fue identificar el mecanismo de absorción numérica en precisión finita: como la perturbación es cuadrática en el residuo, cuando $\beta g(x_k)^2$ es tan pequeña que, al sumarse a $x_k$, la aritmética produce el mismo valor representable, el código detecta la igualdad exacta $w_k = x_k$. En lugar de recurrir a parches artificiales, el algoritmo captura esta condición y detiene controladamente la corrida clasificándola como `Estancamiento w=x` por imposibilidad de formar la secante. A continuación, Julián Jiménez expondrá los resultados y el análisis comparativo."*

---

### Bloque 3: Resultados, Benchmarks, Sistemas, Ciencia de Datos y Cierre
**Ponente:** Julián Camilo Jiménez Rodríguez  
**Tiempo estimado:** 5:00 minutos  
**Diapositivas:** 7 a 11

> *(Diapositiva 7 — 1 min 30 s)*  
> *"Gracias, Julián. Proyectamos en la Diapositiva 7 los resultados obtenidos en las corridas deterministas con 150 dígitos y tolerancia $10^{-25}$. Como indica la nota inferior, mostramos casos representativos; el archivo CSV adjunto conserva todas las corridas completas.*
> 
> *Para el problema $g_1$ (polinomio de Van der Waals con raíz doble en $1.75$ y semilla $1.9$), M1 alcanza el criterio dual en 5 iteraciones con un error absoluto de $1.32\times 10^{-35}$ y residuo de $10^{-72}$, superando en pasos a Newton modificado y Steffensen (que requirieron 8 iteraciones).*
> 
> *Aclaramos que el conteo $1+3k+1$ evaluaciones corresponde específicamente a M1 y M2: evalúa $g(x_0)$ al inicio, $3$ funciones en cada uno de los $k$ pasos, y una llamada de comprobación final $g(x_{\mathrm{final}})$ ejecutada explícitamente tras salir del ciclo. En cuanto a la comparación con el artículo, en $g_1$ M1 satisface nuestro criterio dual en 5 iteraciones, frente a las 7 reportadas en el artículo. Esta diferencia no demuestra una mayor eficiencia algorítmica: obedece a que usamos 150 dígitos y una tolerancia de $10^{-25}$, menos estricta que los $10^{-200}$ con 4000 dígitos del artículo.*
> 
> *(Diapositiva 8 — 1 min)*  
> *En la Diapositiva 8 presentamos el hallazgo técnico más importante del proyecto: el comportamiento en el polinomio $g_3$ ($m=4$, raíz $\alpha=3$). Cerca de $x=3$, el polinomio se comporta como $g_3(x) \approx -80(x-3)^4$. Por la potencia cuarta, un error de $10^{-18}$ genera un residuo del orden de $10^{-72}$. El paso se contrae por debajo de $10^{-59}$ y cumple el criterio operativo dual en 3 iteraciones. Sin embargo, al medir la distancia real a $\alpha=3$, el error absoluto es de $10^{-18} > 10^{-25}$. Con honestidad técnica, no clasificamos esto como convergencia plena, sino como `Criterio dual; error > TOL`, distinguiendo entre la parada operativa y la exactitud efectiva.*
> 
> *Asimismo, evaluamos el orden experimental ACOC: en la raíz simple $x^3-x-2=0$, Newton arrojó $\mathrm{ACOC} \approx 2.0000$ y la secante $\mathrm{ACOC} \approx 1.6162$, muy cercano al orden teórico de la razón áurea ($1.6180$). No obstante, en raíces múltiples bajo pocas iteraciones (3 a 5 pasos), las variaciones transitorias distorsionan el cociente logarítmico (arrojando por ejemplo 8.81 en M1), lo cual confirma que el ACOC es un diagnóstico local asintótico y no demuestra un orden superior a cuatro.*
> 
> *(Diapositiva 9 — 1 min)*  
> *Como experimento complementario vinculado a la Semana 9 del curso, abordamos un sistema no lineal $2\times 2$. Newton multivariable resolvió el sistema en 5 iteraciones con residuo de $10^{-15}$, pero necesitó evaluar 20 derivadas Jacobianas. Por su parte, el método secante de Broyden alcanzó la misma precisión en 10 iteraciones sin derivadas analíticas. Es fundamental precisar que Broyden actualiza el Jacobiano mediante una corrección de rango uno de costo $O(n^2)$, pero la resolución de los sistemas lineales densos continúa teniendo un costo de orden $O(n^3)$ en cada iteración.*
> 
> *(Diapositiva 10 — 40 s)*  
> *En Ciencia de Datos, el entrenamiento en Machine Learning busca puntos estacionarios donde $\nabla L(\boldsymbol{\theta}) = \mathbf{0}$. En regiones mal condicionadas, la matriz Hessiana puede presentar autovalores cercanos a cero, lo que dificulta ciertos métodos de optimización. Estos escenarios motivan el estudio de puntos críticos degenerados, aunque una Hessiana singular no implica necesariamente una raíz de multiplicidad $m>1$. Los métodos estudiados ofrecen una valiosa referencia teórica para investigar algoritmos que aprovechen multiplicidad, cuya aplicación a pérdidas de alta dimensión requerirá extensiones y validaciones adicionales.*
> 
> *(Diapositiva 11 — 50 s)*  
> *Para concluir: implementamos una familia de métodos cuyo orden teórico es cuatro y que alcanza la cota de Kung-Traub bajo las condiciones establecidas por el artículo. En la malla y el límite de iteraciones examinados, $\beta=0.01$ mostró un comportamiento de convergencia más favorable que $\beta=1.0$. Reconocemos como limitación central que el método asume conocida la multiplicidad exacta $m$. Como trabajo futuro, planteamos diseñar estimadores dinámicos de $m$ y explorar extensiones libres de derivadas para optimización en mayores dimensiones. Agradecemos al profesor Edwin Muñoz por su acompañamiento y abrimos la sesión de preguntas. ¡Muchas gracias!"*

---

## 3. Matriz de Defensa Técnica Frente al Docente

Para defender con exactitud cada diapositiva ante posibles preguntas incisivas:

1. **Sobre Newton y raíces múltiples (Diapositiva 2):**  
   *Pregunta:* ¿Por qué Newton pierde el orden cuadrático?  
   *Respuesta:* No es solo que $g'(x)\to 0$, sino que en la expansión de Taylor alrededor de la raíz de multiplicidad $m$, $g(x) \approx \frac{g^{(m)}(\alpha)}{m!}(x-\alpha)^m$ y $g'(x) \approx \frac{g^{(m)}(\alpha)}{(m-1)!}(x-\alpha)^{m-1}$. Su cociente da $\frac{1}{m}(x-\alpha)$, produciendo el error $x_{k+1}-\alpha = \frac{m-1}{m}(x_k-\alpha)$, lo que demuestra formalmente la convergencia lineal con constante asintótica $(m-1)/m$.

2. **Sobre la condición $\beta \neq 0$ y la absorción (Diapositiva 3 y 6):**  
   *Pregunta:* ¿Por qué ocurrió `Estancamiento w=x` si $\beta \neq 0$?  
   *Respuesta:* Porque $\beta \neq 0$ garantiza $w_k \neq x_k$ en el cuerpo de los números reales continuos $\mathbb{R}$, pero en aritmética de punto flotante de precisión finita (incluso con 150 dígitos en `mpmath`), cuando el residuo decae a órdenes como $10^{-80}$ o $10^{-100}$, la perturbación $\beta g(x_k)^2$ es menor que la resolución relativa de representación de $x_k$. Al sumarse, la mantisa finita produce el mismo valor representable ($w_k == x_k$).

3. **Sobre la optimalidad de Kung-Traub (Diapositiva 4):**  
   *Pregunta:* ¿El orden cuatro es intrínseco o condicional?  
   *Respuesta:* Es condicional. Bajo las hipótesis del Teorema 2 ($H(0)=1, H'(0)=1, H''(0)=4$ y $|H'''(0)|<\infty$) y asumiendo convergencia local en una vecindad de la raíz, la familia satura la cota de Kung-Traub ($p=4$ con $d=3$).

4. **Sobre la dinámica compleja y el parámetro $\beta$ (Diapositiva 5):**  
   *Pregunta:* ¿Demostraron que $\beta=0.01$ es globalmente óptimo o que $\beta=1.0$ produce caos?  
   *Respuesta:* No. Nuestra conclusión se restringe estrictamente a la malla de $350\times 350$ en $[-2,2]^2$ y al umbral de 30 iteraciones: observamos que con $\beta=0.01$ una mayor proporción de puntos converge dentro de la cota fijada frente a $\beta=1.0$. No se afirma caos ni se determinan conjuntos formales de Julia.

5. **Sobre la diferencia de iteraciones en $g_1$ frente al artículo (Diapositiva 7):**  
   *Pregunta:* ¿Su método es más rápido porque tomó 5 iteraciones en vez de 7?  
   *Respuesta:* No demuestra superioridad algorítmica. La diferencia se explica porque usamos 150 dígitos y una tolerancia de $10^{-25}$, mientras que los autores emplearon 4000 dígitos y una tolerancia de $10^{-200}$. Nuestro criterio se cumple antes en la trayectoria.

6. **Sobre el hallazgo en $g_3$ ($m=4$) (Diapositiva 8):**  
   *Pregunta:* ¿Por qué la corrida no se clasifica como convergida si cumplió $|\Delta x|<10^{-25}$ y $|g|<10^{-25}$?  
   *Respuesta:* Porque cerca de $x=3$, $g_3(x)\approx -80(x-3)^4$. Un error de $10^{-18}$ genera un residuo de $10^{-72}$ y pasos de $10^{-60}$. Cumple operativamente el criterio dual, pero la distancia real a la raíz supera la tolerancia establecida. Clasificarlo como `Criterio dual; error > TOL` evita falsos positivos de precisión.

7. **Sobre el ACOC atípico de 8.81 (Diapositiva 8):**  
   *Pregunta:* ¿Un ACOC de 8.81 significa orden 8?  
   *Respuesta:* No. El estimador ACOC es una aproximación asintótica. Cuando un método converge en 3 o 4 pasos, la drástica contracción en pocas iteraciones distorsiona el cociente logarítmico, produciendo un valor espurio transitorio que no representa el orden real.

8. **Sobre el método de Broyden (Diapositiva 9):**  
   *Pregunta:* ¿Broyden reduce la complejidad total a $O(n^2)$?  
   *Respuesta:* No. Broyden actualiza la aproximación del Jacobiano en $O(n^2)$ y evita calcular $n^2$ derivadas parciales, pero en cada iteración continúa resolviendo un sistema lineal denso, cuyo costo sigue siendo $O(n^3)$.

9. **Sobre la conexión con Ciencia de Datos (Diapositiva 10):**  
   *Pregunta:* ¿Una Hessiana singular implica multiplicidad $m>1$ en el gradiente?  
   *Respuesta:* No necesariamente. En Machine Learning, una Hessiana con autovalores cercanos a cero genera regiones planas que dificultan la optimización, motivando el estudio de puntos críticos degenerados. Sin embargo, una Hessiana singular no demuestra por sí sola que el gradiente tenga una raíz de multiplicidad superior; la analogía es conceptual respecto a las zonas de aplanamiento local.
