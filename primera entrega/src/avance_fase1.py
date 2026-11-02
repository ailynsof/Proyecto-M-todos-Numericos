"""
Proyecto Integrador - Métodos Numéricos 2026-2
Universidad Externado de Colombia - Pregrado en Ciencia de Datos
Fase 1: Avance de Implementación Computacional (mpmath a alta precisión)
Métodos: M1 (polinomial) y M2 (racional) de Jerezano, Chicharro & Garrido-Saez (2026)
"""

from mpmath import mp

# Precisión de 4000 dígitos emulando la configuración original en MATLAB del artículo
mp.dps = 4000

# Función test 1: Ecuación de Van der Waals (g1)
g1 = lambda x: x**3 - mp.mpf('5.22')*x**2 + mp.mpf('9.0825')*x - mp.mpf('5.2675')
alpha1 = mp.mpf('1.75')
m1 = 2
beta_val = mp.mpf('0.01')
tol = mp.mpf('1e-200')

def run_solver(name, H_func, x0):
    x = mp.mpf(x0)
    xs = [x]
    print(f"\n==================== Método {name} (x0 = {x0}) ====================")
    print(f"{'k':<3} | {'|x_{k+1} - x_k|':<24} | {'|g(x_{k+1})|':<24} | {'|x_{k+1} - alpha|':<24} | {'ACOC':<8}")
    print("-" * 92)
    
    for k in range(1, 15):
        gx = g1(x)
        w = x + beta_val * (gx**2)
        
        # Guarda contra absorción numérica
        if w == x:
            print(f"Estancamiento por absorción numérica (w == x) en iteración {k}.")
            break
            
        g_wx = (g1(w) - gx) / (w - x)
        y = x - m1 * (gx / g_wx)
        gy = g1(y)
        
        # Rama principal de t_k
        t = mp.exp((mp.mpf(1)/m1) * mp.log(gy / gx))
        x_next = x - m1 * H_func(t) * (gx / g_wx)
        xs.append(x_next)
        
        step_diff = abs(x_next - x)
        res = abs(g1(x_next))
        error_true = abs(x_next - alpha1)
        
        # Cálculo de ACOC
        acoc_str = "N/A"
        if len(xs) >= 4:
            num = mp.log(abs(xs[-1] - xs[-2]) / abs(xs[-2] - xs[-3]))
            den = mp.log(abs(xs[-2] - xs[-3]) / abs(xs[-3] - xs[-4]))
            acoc = num / den
            acoc_str = f"{float(acoc):.4f}"
            
        print(f"{k:<3} | {mp.nstr(step_diff, 8):<24} | {mp.nstr(res, 8):<24} | {mp.nstr(error_true, 8):<24} | {acoc_str:<8}")
        
        # Criterio de parada del artículo: |x_{k+1}-x_k| + |g(x_k)| < 1e-200
        if step_diff + abs(gx) < tol:
            print("-" * 92)
            print(f"-> Criterio del artículo cumplido en iteración k = {k}.")
            print(f"   Paso final |x_{{k+1}} - x_k| : {mp.nstr(step_diff, 8)}")
            print(f"   Residuo final |g(x_{{k+1}})| : {mp.nstr(res, 8)}")
            print(f"   ACOC final                   : {acoc_str}")
            break
            
        x = x_next

if __name__ == '__main__':
    # M1: Acelerador polinomial H1(t) = 1 + t + 2*t^2
    run_solver("M1 (Polinomial)", lambda t: 1 + t + 2*(t**2), "1.9")
    
    # M2: Acelerador racional H2(t) = (1 - t) / (1 - 2*t)
    run_solver("M2 (Racional)", lambda t: (1 - t) / (1 - 2*t), "1.9")
