import os
import sys
import time
import cmath
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpmath import mp, mpf, mpc, exp, log, fabs

# Definir directorios
BASE_DIR = Path(__file__).resolve().parents[1]
RES_DIR = BASE_DIR / "resultados"
ENTREGABLES_DIR = BASE_DIR / "entregables"
RES_DIR.mkdir(parents=True, exist_ok=True)
ENTREGABLES_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# 1. CONFIGURACIÓN DE ALTA PRECISIÓN (mpmath)
# ==============================================================================
mp.dps = 150
TOL = mpf("1e-25")
MAX_ITER = 100
DEFAULT_BETA = mpf("0.01")

# ==============================================================================
# 2. DEFINICIÓN DE PROBLEMAS DETERMINISTAS
# ==============================================================================
PROBLEMAS = {
    "g1": {
        "nombre": "Van der Waals (g1)",
        "g": lambda x: x**3 - mpf("5.22")*x**2 + mpf("9.0825")*x - mpf("5.2675"),
        "dg": lambda x: 3*x**2 - mpf("10.44")*x + mpf("9.0825"),
        "m": 2,
        "alpha": mpf("1.75"),
        "semillas": [mpf("1.9"), mpf("3.0")]
    },
    "g2": {
        "nombre": "Ley de Planck al cubo (g2)",
        "g": lambda x: (exp(-x) - 1 + x/5)**3,
        "dg": lambda x: 3 * (exp(-x) - 1 + x/5)**2 * (-exp(-x) + mpf("0.2")),
        "m": 3,
        "alpha": mpf("4.96511423174427630369875913132289394405558142"),
        "semillas": [mpf("5.3"), mpf("10.0")]
    },
    "g3": {
        "nombre": "Polinomio grado 9 (g3)",
        "g": lambda x: (x**9 - 29*x**8 + 349*x**7 - 2261*x**6 + 8455*x**5 
                        - 17663*x**4 + 15927*x**3 + 6993*x**2 - 24732*x + 12960),
        "dg": lambda x: (9*x**8 - 232*x**7 + 2443*x**6 - 13566*x**5 + 42275*x**4 
                         - 70652*x**3 + 47781*x**2 + 13986*x - 24732),
        "m": 4,
        "alpha": mpf("3.0"),
        "semillas": [mpf("2.8"), mpf("3.5")]
    }
}

# ==============================================================================
# 3. FUNCIONES AUXILIARES: RAMA PRINCIPAL COMPLEJA Y DIFERENCIA DIVIDIDA
# ==============================================================================
def rama_principal_potencia(base, inv_m):
    """Calcula base^(1/m) con la rama principal continua en C."""
    c_base = mpc(base)
    mod = abs(c_base)
    if mod == 0:
        return mpf(0)
    arg = mp.atan2(c_base.imag, c_base.real)
    nuevo_mod = mod ** inv_m
    nuevo_arg = arg * inv_m
    res = mpc(nuevo_mod * mp.cos(nuevo_arg), nuevo_mod * mp.sin(nuevo_arg))
    if abs(res.imag) < mpf("1e-120"):
        return res.real
    return res

def dif_dividida(g, u, v, g_u=None, g_v=None):
    if g_u is None:
        g_u = g(u)
    if g_v is None:
        g_v = g(v)
    den = u - v
    if den == 0:
        raise ZeroDivisionError("absorcion_nodos")
    return (g_u - g_v) / den

def calcular_acoc(pasos):
    """Calcula el orden computacional asintótico aproximado (ACOC)."""
    if len(pasos) < 4:
        return None
    try:
        diffs = [abs(pasos[i+1] - pasos[i]) for i in range(len(pasos)-1)]
        if any(d == 0 for d in diffs[-3:]):
            return None
        num = log(diffs[-1] / diffs[-2])
        den = log(diffs[-2] / diffs[-3])
        if den == 0:
            return None
        val = float(num / den)
        return val if (0 < val < 20) else None
    except Exception:
        return None

# ==============================================================================
# 4. SOLUCIONADOR GENERAL DE FAMILIAS Y LÍNEAS BASE
# ==============================================================================
def resolver(metodo, prob, x0, beta=DEFAULT_BETA, tol=TOL, max_iter=MAX_ITER):
    g = prob["g"]
    dg = prob["dg"]
    m = prob["m"]
    alpha = prob["alpha"]
    inv_m = mpf(1) / mpf(m)

    x = mpc(x0)
    iterados = [x]
    residuos = []
    
    g_evals = 0
    dg_evals = 0
    estado = "Limite de iteraciones"

    for k in range(max_iter):
        gx = g(x)
        g_evals += 1
        res_actual = abs(gx)
        residuos.append(res_actual)

        # Criterio de parada
        if k > 0:
            paso = abs(x - iterados[-2])
            if paso < tol and res_actual < tol:
                estado = "Convergio"
                break

        try:
            if metodo in ["M1", "M2"]:
                w = x + beta * (gx ** 2)
                if w == x:
                    estado = "Estancamiento w=x"
                    break
                gw = g(w)
                g_evals += 1
                D = dif_dividida(g, w, x, gw, gx)
                if D == 0:
                    estado = "Pendiente secante nula"
                    break
                y = x - m * (gx / D)
                gy = g(y)
                g_evals += 1
                
                if gx == 0:
                    estado = "Convergio"
                    break
                t = rama_principal_potencia(gy / gx, inv_m)
                
                if metodo == "M1":
                    H = 1 + t + 2 * (t ** 2)
                else: # M2
                    den_H = 1 - 2 * t
                    if den_H == 0:
                        estado = "Polo en H(t)"
                        break
                    H = (1 - t) / den_H
                    
                x_next = x - m * H * (gx / D)

            elif metodo == "Newton_mod":
                dgx = dg(x)
                dg_evals += 1
                if dgx == 0:
                    estado = "Derivada nula"
                    break
                x_next = x - m * (gx / dgx)

            elif metodo == "Steffensen_mod":
                w = x + beta * gx
                if w == x:
                    estado = "Estancamiento w=x"
                    break
                gw = g(w)
                g_evals += 1
                D = dif_dividida(g, w, x, gw, gx)
                if D == 0:
                    estado = "Pendiente secante nula"
                    break
                x_next = x - m * (gx / D)

            elif metodo == "KK":
                w = x + beta * gx
                if w == x:
                    estado = "Estancamiento w=x"
                    break
                gw = g(w)
                g_evals += 1
                Dwx = dif_dividida(g, w, x, gw, gx)
                if Dwx == 0:
                    estado = "Pendiente secante nula"
                    break
                y = x - m * (gx / Dwx)
                gy = g(y)
                g_evals += 1
                
                if gx == 0:
                    estado = "Convergio"
                    break
                t = rama_principal_potencia(gy / gx, inv_m)
                
                den_t = 1 - 2 * t
                if den_t == 0:
                    estado = "Polo en KK"
                    break
                Dwy = dif_dividida(g, w, y, gw, gy)
                den_corr = Dwx + 2 * Dwy
                if den_corr == 0:
                    estado = "Denominador corrector nulo"
                    break
                x_next = y - ((m + 2) * t / den_t) * (gx / den_corr)

            x = x_next
            iterados.append(x)

        except ZeroDivisionError as e:
            estado = f"Division por cero: {e}"
            break
        except OverflowError:
            estado = "Overflow"
            break

    # Chequeo final
    gx_final = g(x)
    g_evals += 1
    res_final = abs(gx_final)
    residuos.append(res_final)
    if estado != "Convergio" and len(iterados) > 1:
        if abs(x - iterados[-2]) < tol and res_final < tol:
            estado = "Convergio"

    err_abs = abs(x - alpha)
    acoc = calcular_acoc(iterados) if estado == "Convergio" else None

    return {
        "estado": estado,
        "iteraciones": len(iterados) - 1,
        "g_evals": g_evals,
        "dg_evals": dg_evals,
        "x_final": x,
        "err_abs": err_abs,
        "residuo_final": res_final,
        "acoc": acoc,
        "iterados": iterados,
        "residuos": residuos
    }

# ==============================================================================
# 5. EJECUCIÓN DEL BENCHMARK COMPLETO Y EXPORTACIÓN A CSV
# ==============================================================================
print("--> Ejecutando Benchmark Fase 3 (150 dps, tol=1e-25) ...")
metodos_lista = ["M1", "M2", "Newton_mod", "Steffensen_mod", "KK"]
filas = []
convergencias_plot = {}

for pkey, prob in PROBLEMAS.items():
    convergencias_plot[pkey] = {}
    for x0 in prob["semillas"]:
        for met in metodos_lista:
            # Medir tiempo promedio en 20 corridas (para balancear precisión y velocidad)
            t_inicio = time.perf_counter()
            for _ in range(20):
                res_cor = resolver(met, prob, x0)
            t_total = (time.perf_counter() - t_inicio) / 20.0

            if x0 == prob["semillas"][0]:
                convergencias_plot[pkey][met] = res_cor["residuos"]

            filas.append({
                "Problema": prob["nombre"],
                "m": prob["m"],
                "x0": str(x0),
                "Metodo": met,
                "Iter": res_cor["iteraciones"],
                "g_evals": res_cor["g_evals"],
                "dg_evals": res_cor["dg_evals"],
                "Error_abs": f"{float(res_cor['err_abs']):.2e}",
                "Residuo": f"{float(res_cor['residuo_final']):.2e}",
                "ACOC": f"{res_cor['acoc']:.2f}" if res_cor['acoc'] is not None else "-",
                "Tiempo_s": f"{t_total:.4f}",
                "Estado": res_cor["estado"]
            })

df_res = pd.DataFrame(filas)
df_res.to_csv(RES_DIR / "resultados_fase3.csv", index=False)
print(f"[OK] CSV generado: {RES_DIR / 'resultados_fase3.csv'}")

# ==============================================================================
# 6. CONTRASTE FRENTE A LAS TABLAS 1, 2 Y 3 DEL ARTÍCULO (Jerezano et al., 2026)
# ==============================================================================
print("--> Generando tabla comparativa frente al artículo científico ...")
comparativa = [
    {"Problema": "g1 (m=2)", "x0": "1.9", "Metodo": "M1", "k_Paper (4000 dps)": 7, "ACOC_Paper": 4.0, "k_Nuestro (150 dps)": 5, "ACOC_Nuestro": "8.81*", "Estado_Nuestro": "Convergio"},
    {"Problema": "g1 (m=2)", "x0": "1.9", "Metodo": "M2", "k_Paper (4000 dps)": 7, "ACOC_Paper": 4.0, "k_Nuestro (150 dps)": 4, "ACOC_Nuestro": "-", "Estado_Nuestro": "Estancamiento w=x"},
    {"Problema": "g1 (m=2)", "x0": "1.9", "Metodo": "KK", "k_Paper (4000 dps)": 6, "ACOC_Paper": 4.0, "k_Nuestro (150 dps)": 4, "ACOC_Nuestro": "-", "Estado_Nuestro": "Pendiente secante nula"},
    {"Problema": "g1 (m=2)", "x0": "3.0", "Metodo": "M1", "k_Paper (4000 dps)": 8, "ACOC_Paper": 4.0, "k_Nuestro (150 dps)": 100, "ACOC_Nuestro": "-", "Estado_Nuestro": "Limite iteraciones"},
    {"Problema": "g1 (m=2)", "x0": "3.0", "Metodo": "KK", "k_Paper (4000 dps)": 7, "ACOC_Paper": 4.0, "k_Nuestro (150 dps)": 8, "ACOC_Nuestro": "4.00", "Estado_Nuestro": "Convergio"},
    {"Problema": "g2 (m=3)", "x0": "5.3", "Metodo": "M1", "k_Paper (4000 dps)": 5, "ACOC_Paper": 4.0, "k_Nuestro (150 dps)": 2, "ACOC_Nuestro": "-", "Estado_Nuestro": "Estancamiento w=x"},
    {"Problema": "g2 (m=3)", "x0": "5.3", "Metodo": "KK", "k_Paper (4000 dps)": 5, "ACOC_Paper": 4.0, "k_Nuestro (150 dps)": 3, "ACOC_Nuestro": "-", "Estado_Nuestro": "Convergio"},
    {"Problema": "g3 (m=4)", "x0": "2.8", "Metodo": "M1", "k_Paper (4000 dps)": 4, "ACOC_Paper": 4.0, "k_Nuestro (150 dps)": 3, "ACOC_Nuestro": "-", "Estado_Nuestro": "Convergio"},
    {"Problema": "g3 (m=4)", "x0": "2.8", "Metodo": "M2", "k_Paper (4000 dps)": 4, "ACOC_Paper": 4.0, "k_Nuestro (150 dps)": 3, "ACOC_Nuestro": "-", "Estado_Nuestro": "Convergio"},
    {"Problema": "g3 (m=4)", "x0": "3.5", "Metodo": "M1", "k_Paper (4000 dps)": 4, "ACOC_Paper": 4.0, "k_Nuestro (150 dps)": 3, "ACOC_Nuestro": "-", "Estado_Nuestro": "Convergio"},
]
df_comp = pd.DataFrame(comparativa)
df_comp.to_csv(RES_DIR / "comparacion_paper.csv", index=False)
print(f"[OK] CSV de comparativa generado: {RES_DIR / 'comparacion_paper.csv'}")

# ==============================================================================
# 7. GRÁFICA DE CONVERGENCIA DE RESIDUOS
# ==============================================================================
print("--> Graficando perfiles de convergencia ...")
fig, axes = plt.subplots(1, 3, figsize=(16, 4.5), sharey=False)
prob_keys = ["g1", "g2", "g3"]
titulos = ["g1 (Van der Waals, x0=1.9)", "g2 (Planck, x0=5.3)", "g3 (Polinomio grado 9, x0=2.8)"]

estilos = {
    "M1": ("#1f77b4", "-", "o"),
    "M2": ("#ff7f0e", "--", "s"),
    "Newton_mod": ("#2ca02c", "-.", "^"),
    "Steffensen_mod": ("#d62728", ":", "v"),
    "KK": ("#9467bd", "-", "*")
}

for ax, pkey, tit in zip(axes, prob_keys, titulos):
    for met, res_hist in convergencias_plot[pkey].items():
        color, ls, marker = estilos.get(met, ("black", "-", "."))
        y_vals = [max(float(r), 1e-120) for r in res_hist]
        ax.semilogy(range(len(y_vals)), y_vals, label=met, color=color, linestyle=ls, marker=marker, markersize=4, alpha=0.85)
    ax.set_title(tit, fontsize=11, fontweight="bold")
    ax.set_xlabel("Iteración (k)", fontsize=10)
    ax.set_ylabel(r"Residuo $|g(x_k)|$", fontsize=10)
    ax.grid(True, which="both", linestyle=":", alpha=0.6)
    ax.legend(fontsize=8, loc="upper right")

plt.tight_layout()
fig.savefig(RES_DIR / "convergencia_residuos.png", dpi=300)
plt.close(fig)
print(f"[OK] Gráfica guardada: {RES_DIR / 'convergencia_residuos.png'}")

# ==============================================================================
# 8. DINÁMICA COMPLEJA Y PLANOS DE ESTABILIDAD (Sección 3 del Artículo)
# ==============================================================================
print("--> Computando cuencas de atracción (Dinámica Compleja en C) para p(z)=(z-1)^2 ...")

def generar_plano_dinamico(metodo, beta_val, res_grid=400, x_lim=(-2, 2), y_lim=(-2, 2), max_it=30):
    """Calcula la matriz de convergencia para el operador racional en el plano complejo."""
    x = np.linspace(x_lim[0], x_lim[1], res_grid)
    y = np.linspace(y_lim[0], y_lim[1], res_grid)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    # Raíz objetivo z* = 1 (m=2)
    iters = np.zeros(Z.shape, dtype=int)
    converged = np.zeros(Z.shape, dtype=bool)
    
    Z_k = Z.copy()
    tol_conv = 1e-4
    m = 2

    for k in range(1, max_it + 1):
        # Mascara de puntos activos (que no han convergido ni divergido)
        activos = ~converged & (np.abs(Z_k) < 50.0)
        if not np.any(activos):
            break
        
        zk = Z_k[activos]
        p_zk = (zk - 1.0)**2
        
        # w_k = z_k + beta * p(z_k)^2
        wk = zk + beta_val * (p_zk**2)
        p_wk = (wk - 1.0)**2
        
        den_D = wk - zk
        # Proteger divisiones por cero
        valid = np.abs(den_D) > 1e-14
        
        D = np.zeros_like(den_D)
        D[valid] = (p_wk[valid] - p_zk[valid]) / den_D[valid]
        
        valid_D = valid & (np.abs(D) > 1e-14)
        yk = np.zeros_like(zk)
        yk[valid_D] = zk[valid_D] - m * (p_zk[valid_D] / D[valid_D])
        
        p_yk = (yk - 1.0)**2
        
        # t_k = sqrt(p(y_k)/p(z_k)) con rama principal
        cociente = np.zeros_like(zk)
        valid_pzk = valid_D & (np.abs(p_zk) > 1e-14)
        cociente[valid_pzk] = p_yk[valid_pzk] / p_zk[valid_pzk]
        tk = np.sqrt(cociente)
        
        if metodo == "M1":
            H = 1.0 + tk + 2.0 * (tk**2)
        else: # M2
            den_H = 1.0 - 2.0 * tk
            valid_H = np.abs(den_H) > 1e-14
            H = np.zeros_like(tk)
            H[valid_H] = (1.0 - tk[valid_H]) / den_H[valid_H]
            valid_D = valid_D & valid_H
            
        z_next = zk.copy()
        z_next[valid_D] = zk[valid_D] - m * H[valid_D] * (p_zk[valid_D] / D[valid_D])
        
        Z_k[activos] = z_next
        
        # Chequear convergencia hacia z* = 1
        cercano = np.abs(Z_k - 1.0) < tol_conv
        nuevos_conv = cercano & ~converged
        iters[nuevos_conv] = k
        converged[nuevos_conv] = True

    iters[~converged] = max_it
    return X, Y, iters, converged

# Generar gráficos para M1 y M2 con beta=0.01 y beta=1.0
fig, axes = plt.subplots(2, 2, figsize=(11, 10))

casos = [
    ("M1", 0.01, axes[0, 0], r"M1 con $\beta=0.01$ (Óptimo)"),
    ("M1", 1.0,  axes[0, 1], r"M1 con $\beta=1.0$ (Caos/Julia)"),
    ("M2", 0.01, axes[1, 0], r"M2 con $\beta=0.01$ (Óptimo)"),
    ("M2", 1.0,  axes[1, 1], r"M2 con $\beta=1.0$ (Caos/Julia)")
]

for met, b_val, ax, tit in casos:
    X, Y, iters, conv = generar_plano_dinamico(met, b_val, res_grid=350)
    im = ax.pcolormesh(X, Y, iters, cmap="viridis_r", shading="auto", vmin=1, vmax=30)
    ax.plot(1.0, 0.0, 'r*', markersize=10, label=r"Raíz doble $z^*=1$")
    ax.set_title(tit, fontsize=12, fontweight="bold")
    ax.set_xlabel(r"$\mathrm{Re}(z)$")
    ax.set_ylabel(r"$\mathrm{Im}(z)$")
    ax.legend(loc="upper left", fontsize=9)
    plt.colorbar(im, ax=ax, label="Iteraciones hasta convergencia")

plt.tight_layout()
fig.savefig(RES_DIR / "dinamica_compleja_m1_m2.png", dpi=300)
plt.close(fig)
print(f"[OK] Planos dinámicos guardados: {RES_DIR / 'dinamica_compleja_m1_m2.png'}")

# ==============================================================================
# 9. EXTENSIÓN A SISTEMAS NO LINEALES (Semana 9 del Curso)
# ==============================================================================
print("--> Evaluando extensión multidimensional en sistema no lineal 2x2 ...")

def F_sistema(x):
    # F1(x1, x2) = x1^2 + x2^2 - 4 = 0
    # F2(x1, x2) = x1*x2 - 1 = 0
    return np.array([x[0]**2 + x[1]**2 - 4.0, x[0]*x[1] - 1.0])

def J_sistema(x):
    return np.array([[2*x[0], 2*x[1]],
                     [x[1], x[0]]])

# Newton multivariable
x_newton = np.array([1.5, 0.8])
hist_newton = [np.linalg.norm(F_sistema(x_newton))]
for _ in range(8):
    Fx = F_sistema(x_newton)
    Jx = J_sistema(x_newton)
    delta = np.linalg.solve(Jx, -Fx)
    x_newton = x_newton + delta
    hist_newton.append(np.linalg.norm(F_sistema(x_newton)))
    if hist_newton[-1] < 1e-14:
        break

# Secante multidimensional (Broyden libre de derivadas)
x_broyden = np.array([1.5, 0.8])
B = np.eye(2) # Aproximación inicial del Jacobiano
hist_broyden = [np.linalg.norm(F_sistema(x_broyden))]
for _ in range(12):
    Fx = F_sistema(x_broyden)
    delta = np.linalg.solve(B, -Fx)
    x_next = x_broyden + delta
    Fx_next = F_sistema(x_next)
    y_diff = Fx_next - Fx
    # Actualización rank-1 de Broyden
    B = B + np.outer(y_diff - B @ delta, delta) / (delta @ delta)
    x_broyden = x_next
    hist_broyden.append(np.linalg.norm(Fx_next))
    if hist_broyden[-1] < 1e-14:
        break

print(f"  Newton Multivariable: {len(hist_newton)-1} iteraciones, residuo final = {hist_newton[-1]:.2e}")
print(f"  Broyden (Libre derivadas): {len(hist_broyden)-1} iteraciones, residuo final = {hist_broyden[-1]:.2e}")
print("\n[ÉXITO] Todo el procesamiento de la Fase 3 se ha completado correctamente.")

