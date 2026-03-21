import numpy as np
import os

def generate_realistic_plate(seed=None, make_invalid=False):
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)  # ← agregué import random abajo
    
    # ==================== POSICIONES EXACTAS ====================
    b_pos = np.array([0, 1, 42, 43, 84, 85])      # Blancos
    p_pos = np.array([2, 3, 44, 45, 86, 87])      # Positivos
    n_pos = np.array([4, 5, 46, 47, 88, 89])      # Negativos
    sample_pos = np.setdiff1d(np.arange(90), np.concatenate([b_pos, p_pos, n_pos]))
    
    vals = np.zeros(90)
    
    # ===================== CONTROLES =====================
    vals[b_pos] = np.clip(np.random.normal(1.02, 0.28, 6), 0.5, 2.0)
    
    p_base = np.random.normal(137, 12, 3)
    if make_invalid and random.random() < 0.4:
        p_base[2] = 42.0
    for i, base in enumerate(p_base):
        idx = i * 2
        vals[p_pos[idx:idx+2]] = np.clip([
            base + np.random.normal(0, 2.5),
            base + np.random.normal(0, 2.5)
        ], 60, 180)
    
    vals[n_pos] = np.clip(np.random.normal(2.85, 0.45, 6), 1.5, 6.0)
    if make_invalid and random.random() < 0.4:
        vals[n_pos[4:]] = 45.0
    
    # ===================== MUESTRAS =====================
    sample_bases = np.concatenate([
        np.random.normal(8, 4, 8),
        np.random.normal(38, 12, 12),
        np.random.normal(82, 22, 16)
    ])
    np.random.shuffle(sample_bases)
    
    for i in range(36):
        base = sample_bases[i]
        vals[sample_pos[i*2 : i*2+2]] = np.clip([
            base + np.random.normal(0, 1.8),
            base + np.random.normal(0, 1.7)
        ], 4.0, 145.0)
    
    # ===================== VALIDACIÓN (igual que el insert) =====================
    BB = np.mean(vals[b_pos])
    NN = np.mean(vals[n_pos])
    P_min = np.min(vals[p_pos])
    valid = True
    msgs = []
    
    if np.any(vals[b_pos] >= 10): 
        valid = False; msgs.append("❌ Blanco ≥10")
    if np.max(vals[n_pos]) > BB + 10: 
        valid = False; msgs.append("❌ Negativo > BB+10")
    if not (60 <= P_min <= 180): 
        valid = False; msgs.append("❌ P fuera de 60-180")
    ratio = (NN - BB) / (P_min - BB) if (P_min - BB) > 0 else 999
    if ratio >= 0.1: 
        valid = False; msgs.append(f"❌ Ratio = {ratio:.3f} ≥ 0.1")
    
    status = "INVÁLIDA" if not valid else "VÁLIDA"
    print(f"   → Placa {status} | Controles OK: {valid}")
    if not valid:
        print("   ⚠️  " + " | ".join(msgs))
    
    return vals

# ============================ CONFIGURACIÓN ============================
NUM_PLACAS = 500                    # ← cámbialo a 10, 20, 50... lo que quieras
os.makedirs("placas_generadas", exist_ok=True)

print("🚀 Generando y guardando", NUM_PLACAS, "placas ultra-reales...\n")

import random  # ← lo agregué aquí para que funcione

for i in range(NUM_PLACAS):
    filename = f"placas_generadas/lec_SIM_{i+1}.flu"
    print(f"📄 Generando {filename} ...")
    
    vals = generate_realistic_plate(seed=100 + i, make_invalid=(i == 3))  # la 4ª sale inválida a propósito
    
    with open(filename, "w") as f:
        for v in vals:
            f.write(f"{v:.2f}\n")
    
    print(f"✅ ¡Guardado! → {filename}\n")

print("🎉 ¡Listo! Todas las placas están en la carpeta 'placas_generadas'")
print("   Puedes abrirlas con bloc de notas o copiar-pegar directo al programa UMELISA.")