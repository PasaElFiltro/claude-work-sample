"""Recalcula los tiempos de index.raw.json (Gemini 3.7 Flash) a tiempos reales.

Gemini procesó los cinco archivos en el orden 2,3,4,5,1 y asignó offsets según ese orden.
Su timestamp_global es consistente con ese orden; su timestamp_local es relativo al clip
en la mayoría de las ventanas pero relativo a la ventana de 10 min en cuatro de ellas.
Por eso se usa solo el global: minuto_en_archivo = global - offset_gemini_del_clip.
Los relojes de inicio se leyeron en pantalla (esquina superior derecha del Mac).
Uso: python3 corregir_indice.py index.raw.json > index.corrected.json
"""
import json, sys

ARCHIVOS = {1: ('zesty_session_01_0000-0057.mov', 0,     '11:15'),
            2: ('zesty_session_01_0057-0150.mov', 3425,  '12:12'),
            3: ('zesty_session_01_0149-0248.mov', 6637,  '13:04'),
            4: ('zesty_session_01_0246-0343.mov', 10178, '14:02'),
            5: ('zesty_session_01_0343-0425.mov', 13575, '14:58')}
GEMINI_CLIP_A_ARCHIVO = {1: 2, 2: 3, 3: 4, 4: 5, 5: 1}
GEMINI_OFFSET = {1: 0, 2: 3420, 3: 6600, 4: 10140, 5: 13380}

def secs(t):
    p = [int(x) for x in t.split(':')]
    return p[0]*3600 + p[1]*60 + p[2] if len(p) == 3 else p[0]*60 + p[1]

def hms(x): return f"{x//3600:02d}:{(x%3600)//60:02d}:{x%60:02d}"

raw = json.load(open(sys.argv[1]))
out = []
for e in raw['eventos']:
    g = secs(e['timestamp_global'])
    gc = max(k for k, v in GEMINI_OFFSET.items() if g >= v)
    loc = g - GEMINI_OFFSET[gc]
    real = GEMINI_CLIP_A_ARCHIVO[gc]
    fn, off, clock = ARCHIVOS[real]
    h, m = map(int, clock.split(':'))
    t = h*3600 + m*60 + loc
    ne = {'archivo': real, 'archivo_nombre': fn, 'minuto_en_archivo': hms(loc),
          'tiempo_global_real': hms(off + loc), 'reloj_chile': f"{t//3600:02d}:{(t%3600)//60:02d}",
          'gemini_clip': gc, 'gemini_global': e['timestamp_global']}
    for k in ('surface', 'romina_action', 'system_or_model_action', 'decision_or_problem',
              'correction_or_pivot', 'anchor'):
        ne[k] = e.get(k)
    out.append(ne)
out.sort(key=lambda x: x['tiempo_global_real'])
json.dump({'sesion': 'lunes 31 de agosto de 2026, 11:15 → 15:40 hora Chile, cinco archivos continuos',
           'metodo': __doc__.strip(),
           'archivos': {k: {'nombre': v[0], 'offset_real_s': v[1], 'reloj_inicio': v[2]} for k, v in ARCHIVOS.items()},
           'equivalencia_gemini': {f'clip {k}': f'archivo {v}' for k, v in GEMINI_CLIP_A_ARCHIVO.items()},
           'eventos': out}, sys.stdout, ensure_ascii=False, indent=1)
