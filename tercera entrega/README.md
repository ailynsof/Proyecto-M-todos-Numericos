# Tercera Entrega (Entrega Final) — Organización y Uso
**Proyecto Integrador: Métodos Numéricos (2026-2)**  
**Universidad Externado de Colombia — Pregrado en Ciencia de Datos**  
**Artículo Base:** *Derivative-free optimal multiple-root finding family of iterative methods*, J. H. Jerezano, F. I. Chicharro, N. Garrido-Sáez (2026), *Computational and Applied Mathematics*, 45:304.  
**Equipo:** Ailyn Sofía Gómez Rodríguez, Julián Camilo Jiménez, Julián Steven Duarte  
**Docente:** Edwin Fernando Muñoz Chipatecua  

---

## 1. Estructura de la Carpeta

```
tercera entrega/
├── README.md                                  # Este documento: guía completa de uso y reproducción.
├── planificacion/
│   └── plan_implementacion.md                 # Hoja de ruta metodológica y fundamentación teórica de la Fase 3.
├── desarrollo/
│   ├── generar_resultados_fase3.py            # Generador automatizado de datos, gráficos y planos de convergencia.
│   └── construir_notebook_fase3.py            # Ensamblador del notebook reproducible con pre-cálculo de outputs.
├── entregables/
│   ├── main.tex                               # Fuente LaTeX del informe final consolidado (3-5 páginas netas).
│   └── tercera_entrega.ipynb                  # Cuaderno Jupyter maestro ejecutable y autocontenido con outputs.
├── resultados/
│   ├── resultados_fase3.csv                   # Métricas consolidadas (errores, residuos, ACOC, evaluaciones, tiempos).
│   ├── comparacion_paper.csv                  # Tabla comparativa directa vs. Tablas 1, 2 y 3 de Jerezano et al. (2026).
│   ├── dinamica_compleja_m1_m2.png            # Planos dinámicos (cuencas de atracción) en C para M1 y M2 (beta=0.01 vs 1.0).
│   └── convergencia_residuos.png              # Gráficos logarítmicos del decaimiento de residuos para g1, g2 y g3.
└── sustentacion/
    ├── presentacion.tex                       # Diapositivas en LaTeX Beamer (16:9) estructuradas para 12-15 minutos.
    └── guia_sustentacion_equipo.md            # Guía de defensa con distribución de roles y banco de 8 preguntas difíciles.
```

---

## 2. Requisitos de Software y Entorno

- **Python:** 3.10 o superior (validado en Python 3.11).
- **Bibliotecas requeridas:**
  ```bash
  pip install mpmath numpy pandas matplotlib ipykernel nbformat nbconvert
  ```
- **LaTeX (opcional para compilar PDF):** TeX Live, MiKTeX o plataforma Overleaf (se incluye código fuente autocontenido sin dependencias externas).

---

## 3. Instrucciones de Ejecución y Reproducibilidad

### Opción A: Abrir y Explorar el Cuaderno Jupyter
El cuaderno principal ya se encuentra completamente ejecutado y con todas las salidas incrustadas:
- Abra `entregables/tercera_entrega.ipynb` en JupyterLab, VS Code o Google Colab.
- Puede reiniciar el kernel y ejecutar todas las celdas en orden. El cuaderno es 100% determinista y no depende de variables aleatorias no controladas.

### Opción B: Regenerar Todos los Resultados desde la Terminal
Desde la raíz del repositorio, ejecute:
```bash
python "tercera entrega/desarrollo/generar_resultados_fase3.py"
```
Esto actualizará los archivos en `resultados/` y generará las imágenes de alta resolución.

Para reconstruir y reejecutar el cuaderno programáticamente:
```bash
python "tercera entrega/desarrollo/construir_notebook_fase3.py"
```

---

## 4. Compilación del Informe y la Presentación

### Informe Técnico Final (`entregables/main.tex`):
Desde la carpeta `tercera entrega/entregables/`:
```bash
pdflatex main.tex
pdflatex main.tex
```
*(O cargue `main.tex` y la carpeta `resultados/` en Overleaf)*. El documento respeta estrictamente el límite reglamentario de 3 a 5 páginas de cuerpo neto de texto continuo, excluyendo portada, bibliografía, figuras y tablas.

### Diapositivas de Sustentación (`sustentacion/presentacion.tex`):
Desde la carpeta `tercera entrega/sustentacion/`:
```bash
pdflatex presentacion.tex
```
Genera un archivo PDF panorámico (16:9) listo para proyectar durante la sustentación oral final del curso.

---

## 5. Resumen de Aportes de la Entrega Final

1. **Optimalidad de Kung-Traub demostrada:** Las familias $M_1$ y $M_2$ alcanzan orden 4 con solo 3 evaluaciones escalares y 0 derivadas, logrando un índice de eficiencia $\mathcal{I} = 4^{1/3} \approx 1.587$, superior a Newton modificado ($\mathcal{I} \approx 1.414$).
2. **Estabilidad dinámica en $\mathbb{C}$:** Se verifica que $z^*=1$ es un punto fijo superatractor y se comparan M1 y M2 en una malla finita para $\beta=0.01$ y $\beta=1.0$. El gráfico muestra puntos que no convergen dentro del límite; no pretende demostrar caos ni un óptimo global.
3. **Contraste honesto de precisión:** Se explica la diferencia entre los 4000 dígitos con tolerancia $10^{-200}$ del artículo en Matlab frente a los 150 dígitos con $10^{-25}$ en Python, justificando las variaciones en el conteo de iteraciones y documentando la absorción de perturbación en punto flotante ($w=x$).
4. **Extensión a sistemas y optimización:** Se compara Newton y Broyden en un sistema pequeño, observando convergencia y evaluaciones de derivadas. El ejemplo no mide una ventaja asintótica ni valida una aplicación directa a aprendizaje automático.

