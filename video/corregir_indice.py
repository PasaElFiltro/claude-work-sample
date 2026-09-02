"""Recalcula los tiempos de index.raw.json (Gemini 3.7 Flash) a hora de reloj real.

Fuente de verdad: el reloj del Mac visible en pantalla. Para cada archivo se detectó
el segundo exacto del primer cambio de minuto (diff de frames sobre los dígitos de la hora)
y de ahí el inicio exacto del archivo. Los archivos NO son contiguos: hay un hueco de 22 s
entre el 1 y el 2, y solapes de 59, 65 y 102 s entre 2-3, 3-4 y 4-5. Por eso no sirve
sumar duraciones ni confiar en los nombres (el 4 dice 0246 y arranca 2:47:58).

Gemini procesó los archivos en el orden 2,3,4,5,1 y asignó offsets según ese orden.
Su timestamp_global es consistente con ese orden; su timestamp_local es relativo al clip en
la mayoría de las ventanas pero relativo a la ventana de 10 min en 78 eventos. Se usa solo
el global: minuto_en_archivo = global - offset_gemini_del_clip.

Uso: python3 corregir_indice.py index.raw.json > index.corrected.json
"""
import json, sys

# archivo: (nombre, inicio exacto hh:mm:ss leído del reloj en pantalla, duración s)
ARCHIVOS = {1: ('zesty_session_01_0000-0057.mov', '11:14:27', 3425.95),
            2: ('zesty_session_01_0057-0150.mov', '12:11:55', 3212.11),
            3: ('zesty_session_01_0149-0248.mov', '13:04:28', 3541.92),
            4: ('zesty_session_01_0246-0343.mov', '14:02:25', 3397.36),
            5: ('zesty_session_01_0343-0425.mov', '14:57:20', 2473.36)}
GEMINI_CLIP_A_ARCHIVO = {1: 2, 2: 3, 3: 4, 4: 5, 5: 1}
GEMINI_OFFSET = {1: 0, 2: 3420, 3: 6600, 4: 10140, 5: 13380}

def secs(t):
    p = [int(x) for x in t.split(':')]
    return p[0]*3600 + p[1]*60 + p[2] if len(p) == 3 else p[0]*60 + p[1]

def hms(x): x = int(round(x)); return f"{x//3600:02d}:{(x%3600)//60:02d}:{x%60:02d}"

T0 = secs(ARCHIVOS[1][1])
raw = json.load(open(sys.argv[1]))
out = []
for e in raw['eventos']:
    g = secs(e['timestamp_global'])
    gc = max(k for k, v in GEMINI_OFFSET.items() if g >= v)
    loc = g - GEMINI_OFFSET[gc]
    real = GEMINI_CLIP_A_ARCHIVO[gc]
    fn, inicio, dur = ARCHIVOS[real]
    t_reloj = secs(inicio) + loc
    ne = {'archivo': real, 'archivo_nombre': fn, 'minuto_en_archivo': hms(loc),
          'reloj_chile': hms(t_reloj), 'tiempo_global_real': hms(t_reloj - T0),
          'fuera_de_duracion': loc > dur,
          'gemini_clip': gc, 'gemini_global': e['timestamp_global']}
    for k in ('surface', 'romina_action', 'system_or_model_action', 'decision_or_problem',
              'correction_or_pivot', 'anchor'):
        ne[k] = e.get(k)
    out.append(ne)
out.sort(key=lambda x: (x['reloj_chile'], x['archivo']))
json.dump({'sesion': 'lunes 31 de agosto de 2026, 11:14:27 → 15:38:33 hora Chile, cinco archivos con un hueco de 22 s y tres solapes',
           'metodo': __doc__.strip(),
           'archivos': {k: {'nombre': v[0], 'inicio_reloj': v[1], 'duracion_s': v[2],
                            'offset_real_s': secs(v[1]) - T0} for k, v in ARCHIVOS.items()},
           'equivalencia_gemini': {f'clip {k}': f'archivo {v}' for k, v in GEMINI_CLIP_A_ARCHIVO.items()},
           'eventos': out}, sys.stdout, ensure_ascii=False, indent=1)
