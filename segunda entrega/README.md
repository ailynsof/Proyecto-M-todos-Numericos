# Segunda entrega - organizacion y uso

## Estructura

- `entregables/segunda_entrega.ipynb`: metodos, experimentos, tabla y graficas.
- `entregables/main.tex`: informe completo en un unico archivo fuente.
- `planificacion/plan_implementacion.md`: alcance, metodos, criterios y flujo de trabajo.
- `resultados/resultados_fase2.csv`: comparacion de M1, M2, Newton, Steffensen y KK.
- `resultados/sensibilidad_beta.csv`: barrido de beta para M1 y M2.
- `desarrollo/ejecutar_notebook.py`: ejecuta las celdas y guarda sus salidas.
- `desarrollo/obsoletos/build_notebook_borrador.py`: generador anterior, archivado y no requerido.

Los entregables principales son el notebook y el fuente LaTeX. Los CSV son salidas generadas al ejecutar el notebook.

## Requisitos y ejecucion

Use Python 3.10 o posterior, Jupyter, `mpmath`, `pandas` y `matplotlib`. Abra `entregables/segunda_entrega.ipynb` y ejecute todas las celdas en orden. La configuracion es de 150 digitos, tolerancia 1e-25, maximo 100 iteraciones y beta=0.01. Se fijan explicitamente las semillas iniciales; no hay simulacion aleatoria. La potencia fraccionaria usa la rama principal compleja. Se prueban ademas beta=0.001, 0.01 y 1.0, y una corrida auxiliar en `float64`. El tiempo tabulado es el promedio de 50 ejecuciones por caso.

Desde la raiz del repositorio tambien puede ejecutarse el cuaderno con:

```bash
python3 "segunda entrega/desarrollo/ejecutar_notebook.py"
```

Los archivos CSV se actualizan en `resultados/`. Los tiempos dependen del equipo.

## Compilar el informe

Desde `segunda entrega/entregables/`:

```bash
pdflatex main.tex
```

El PDF de revision ocupa cuatro paginas en total. La guia pide entre tres y cinco paginas para el cuerpo, sin contar portada, bibliografia, figuras ni tablas; revise ese conteo tras compilar en su entorno. El archivo fuente es unico y no depende de un archivo .bib.
