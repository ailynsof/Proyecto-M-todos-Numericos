# Plan de Implementación y Consolidación — Tercera Entrega (Fase 3)
**Proyecto Integrador: Métodos Numéricos (2026-2)**  
**Universidad Externado de Colombia — Pregrado en Ciencia de Datos**  
**Artículo Base:** *Derivative-free optimal multiple-root finding family of iterative methods*, J. H. Jerezano, F. I. Chicharro, N. Garrido-Sáez (2026)  
**Equipo:** Ailyn Sofía Gómez Rodríguez, Julián Camilo Jiménez, Julián Steven Duarte  
**Docente:** Edwin Fernando Muñoz Chipatecua  

---

## 1. Alcance y Objetivos de la Entrega Final

La Fase 3 corresponde a la etapa culminante del Proyecto Integrador: **consolidación, análisis integral y comunicación científica**.
A partir de los desarrollos aprobados de las Fases 1 y 2, esta entrega final tiene como propósitos:

1. **Presentar la Solución Computacional Definitiva:**
   - Resolver los problemas benchmark univariados ($g_1$: Van der Waals, $g_2$: Ley de Planck al cubo, $g_3$: polinomio característico de $9\times 9$) con control de precisión arbitraria (`mpmath`, 150 dps) y tolerancia estricta ($10^{-25}$).
   - Manejo completo de patologías numéricas: derivada nula, secante nula, pérdida de perturbación por absorción ($w_k == x_k$) y cálculo analítico de potencias fraccionarias con la rama principal compleja.
   - Contraste empírico transparente frente a los resultados reportados en las Tablas 1, 2 y 3 del artículo de Jerezano et al. (2026).

2. **Estabilidad y Dinámica Compleja en $\mathbb{C}$ (Aporte Teórico Central del Artículo):**
   - Implementar el análisis dinámico del operador racional de punto fijo $R(z, \beta)$ sobre polinomios con raíces múltiples (caso $p(z)=(z-1)^2$, $m=2$).
   - Generar los **planos dinámicos (cuencas de atracción)** en una malla del plano complejo, visualizando la convergencia hacia la raíz superatractora $z^*=1$ y los conjuntos caóticos de Julia.
   - Evaluar computacionalmente el efecto del parámetro de aceleración $\beta$, demostrando por qué $\beta=0.01$ es dinámicamente superior a valores grandes ($\beta=1.0, \beta=5.0$) que fragmentan las cuencas e inducen caos.

3. **Extensión a Sistemas No Lineales Multidimensionales (Semana 9):**
   - Demostración numérica de la solución de sistemas $\mathbf{F}(\mathbf{x}) = \mathbf{0}$ en $\mathbb{R}^2$.
   - Análisis comparativo del costo computacional de evaluar y factorizar la matriz Jacobiana $\mathbf{J}(\mathbf{x}) \in \mathbb{R}^{n\times n}$ ($O(n^3)$ en LU) frente a esquemas libres de derivadas basados en diferencias divididas multidimensionales.

4. **Informe Técnico Final en LaTeX:**
   - Cumplimiento riguroso de las directrices de formato de la Universidad: extensión neta entre 3 y 5 páginas de texto continuo (excluyendo portada, bibliografía, tablas y figuras).
   - Lenguaje formal, argumentación técnica sólida y articulación con los fundamentos de optimización en Ciencia de Datos.

5. **Sustentación Oral y Dominio Conceptual del Equipo:**
   - Diapositivas en formato Beamer estructuradas para una presentación de 12 a 15 minutos.
   - Guía de preguntas y respuestas técnicas para garantizar el dominio conceptual pleno de los tres integrantes.

---

## 2. Métodos Implementados y Familias Numéricas

Para una raíz $\alpha$ de multiplicidad conocida $m \ge 1$:

### Familia Propuesta (Jerezano et al., 2026) — Libre de Derivadas de Orden 4:
$$w_k = x_k + \beta [g(x_k)]^2, \quad \beta \in \mathbb{R}\setminus\{0\}$$
$$D_k = g[w_k, x_k] = \frac{g(w_k) - g(x_k)}{w_k - x_k}$$
$$y_k = x_k - m \frac{g(x_k)}{D_k}$$
$$t_k = \left(\frac{g(y_k)}{g(x_k)}\right)^{1/m} = \exp\left(\frac{1}{m} \operatorname{Ln}\left(\frac{g(y_k)}{g(x_k)}\right)\right)$$
$$x_{k+1} = x_k - m H(t_k) \frac{g(x_k)}{D_k}$$

- **Variante $M_1$ (Ponderación polinomial cuadrática):** $H_1(t) = 1 + t + 2t^2$.
- **Variante $M_2$ (Ponderación racional):** $H_2(t) = \frac{1-t}{1-2t}$.
- **Optimalidad de Kung-Traub:** Orden $p = 2^{d-1} = 2^{3-1} = 4$ con $d=3$ evaluaciones funcionales ($g(x_k), g(w_k), g(y_k)$) por iteración. Índice de eficiencia $\mathcal{I} = 4^{1/3} \approx 1.587$.

### Métodos de Comparación (Líneas Base del Curso y Competidores):
1. **Newton Modificado (Semana 9):**
   $$x_{k+1} = x_k - m \frac{g(x_k)}{g'(x_k)}$$
   Requiere $g(x_k)$ y $g'(x_k)$; orden cuadrático $p=2$.
2. **Steffensen Modificado (Traub, 1964):**
   $$w_k = x_k + \beta g(x_k), \quad x_{k+1} = x_k - m \frac{g(x_k)}{g[w_k, x_k]}$$
   Libre de derivadas; orden cuadrático $p=2$.
3. **Método KK (Kumar et al., 2020):**
   Esquema predictor-corrector de orden 4 sin derivadas reportado en el artículo:
   $$w_k = x_k + \beta g(x_k), \quad y_k = x_k - m \frac{g(x_k)}{g[w_k, x_k]}$$
   $$x_{k+1} = y_k - \frac{(m+2)t_k}{1 - 2t_k} \frac{g(x_k)}{g[w_k, x_k] + 2g[w_k, y_k]}$$

---

## 3. Dinámica Compleja y Planos de Estabilidad

Dado el polinomio cuadrático canónico con raíz doble $p(z) = (z-1)^2$ ($m=2$), los operadores racionales asociados a $M_1$ y $M_2$ son:
- Para $M_1$:
  $$R_1(z, \beta) = \frac{N_{10}(z, \beta)}{3\beta z^3 - 3\beta z^2 + 3\beta z \dots}$$
- Para $M_2$:
  $$R_2(z, \beta) = -\frac{\beta^2 z^7 - 6\beta^2 z^6 + 15\beta^2 z^5 - 20\beta^2 z^4 + 15\beta^2 z^3 - 6\beta^2 z^2 + \beta^2 z - 4}{-\beta z^3 + 3\beta z^2 - 3\beta z + \beta + 2\beta z^3 - 3\beta z^2 + 3\beta z - \beta + 2}$$

En ambos casos, la raíz $z^* = 1$ es un **punto fijo superatractor** ($R'(1) = 0$). Sin embargo, la presencia de puntos críticos libres y polos produce bifurcaciones y cuencas fractales de Julia cuando $\beta$ se aleja de cero. El notebook generará matrices de convergencia en el plano complejo $z \in [-2, 2] \times [-2, 2]$ para comparar el tamaño y regularidad de las cuencas de atracción bajo $\beta=0.01$ frente a $\beta=1.0$.

---

## 4. Estructura de Entregables de la Fase 3

- `tercera entrega/entregables/tercera_entrega.ipynb`: Cuaderno Jupyter maestro ejecutable y autocontenido.
- `tercera entrega/entregables/main.tex`: Informe científico final en LaTeX de 4 a 5 páginas netas de cuerpo.
- `tercera entrega/sustentacion/presentacion.tex`: Diapositivas Beamer para la sustentación presencial/virtual.
- `tercera entrega/sustentacion/guia_sustentacion_equipo.md`: Preguntas clave de examen y argumentación técnica.
- `tercera entrega/resultados/`: Archivos CSV de resultados consolidados y figuras en alta definición.
- `tercera entrega/README.md`: Guía de reproducibilidad paso a paso.

