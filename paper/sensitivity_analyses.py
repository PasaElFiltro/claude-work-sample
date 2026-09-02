#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sensitivity_analyses.py — DELTA-PI Benchmark
Second-round analyses responding to reviewer concerns (unit of analysis,
confounds, dedup audit, attrition, ICC(2,1), spread counts).

Reconstructed for the OSF deposit from the session of 1-2 July 2026, in which
these analyses were first run. Every number printed here appears in the
manuscript (Sensitivity Analyses section, revised Results, and Table 3).

Para el próximo Claude, o para la analista humana que verifique:
- input: delta_pi_CONSOLIDATED_3models_FINAL.csv (OSF: osf.io/ue4qy)
- el plan congelado vive en osf.io/zusb5; nada aquí lo contradice — estos
  análisis responden a revisión, y así se reportan en el paper.
- semilla de la permutación: 457 (el n de sujetos válidos; elegida por eso).
- números que deben reproducirse: t(23)=27.49 dz=5.61 | perm p≈.693 |
  clean ratio 3.20, t(23)=26.22 | ceiling 95.4/88.1 y 99.0/93.9 |
  incidencia: scores no-máximos 6.1% vs 1.0%; celdas SD>0 14.0% vs 7.2% | OR judgment=2.95 [2.39,3.63] |
  atrición χ² p=.21 (cond), p=1.0 (temp) | ICC(2,1) .655–.797 |
  spread t=0: 17 full-scale, 62 con rango>=3 |
  trace ANOVA instancia F(3,453)=68.5.
  (la permutación es estocástica salvo por la semilla; con seed=457 y 2000
  permutaciones el p reportado fue .693.)
"""
import sys
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

CSV = sys.argv[1] if len(sys.argv) > 1 else "delta_pi_CONSOLIDATED_3models_FINAL.csv"
CATS = ['abstraction','addition','omission','logical_operations','focus',
        'do_not_translate','untranslated','terminology','mistranslation',
        'referential_clarity','redundancy','locale_conventions',
        'function_words','spelling_punctuation','grammar','fluency']
PROC = ['do_not_translate','logical_operations','spelling_punctuation',
        'locale_conventions','grammar']
JUDG = [c for c in CATS if c not in PROC]

# ---------------------------------------------------------------- load + dedup
raw = pd.read_csv(CSV)
n_raw = len(raw)

# DEDUP AUDIT (reviewer concern 3): key ALWAYS includes instance id.
grp = raw.groupby(['subject_id','test'])
conflicts = sum(
    1 for _, g in grp
    if g[CATS + ['timestamp']].drop_duplicates().shape[0] > 1
)
df = raw.drop_duplicates(subset=['subject_id','test']).copy()
print(f"[dedup] raw rows={n_raw} -> unique (subject,item)={len(df)}; "
      f"groups with conflicting content={conflicts} (must be 0)")

# frozen exclusion rule: any unpopulated category on any item -> whole instance out
bad = df[df[CATS].isna().any(axis=1)]['subject_id'].unique()
valid = df[~df.subject_id.isin(bad)].copy()
for c in CATS:
    valid[c] = valid[c].astype(int)
valid['temperature'] = valid['temperature'].astype(int)
print(f"[consort] launched={df.subject_id.nunique()} valid={valid.subject_id.nunique()} "
      f"excluded={len(bad)}")

# ----------------------------------------------------- long form + per-cell SD
long = valid.melt(id_vars=['subject_id','model','condition','temperature','test'],
                  value_vars=CATS, var_name='category', value_name='score')
long['ctype'] = np.where(long['category'].isin(PROC), 'procedural', 'judgment')
sd = (long.groupby(['model','condition','temperature','test','category','ctype'])
          ['score'].std(ddof=1).reset_index(name='sd'))

# ------------------------------------------- 1. RQ1 at the correct unit (cells)
cellm = (sd.groupby(['model','condition','temperature','ctype'])['sd']
           .mean().unstack('ctype').reset_index())
t_c, p_c = stats.ttest_rel(cellm['judgment'], cellm['procedural'])
dif = cellm['judgment'] - cellm['procedural']
dz = dif.mean() / dif.std(ddof=1)
ratios = cellm['judgment'] / cellm['procedural']
print(f"\n[RQ1 cell-level] t(23)={t_c:.2f} p={p_c:.2e} dz={dz:.2f} "
      f"ratio range {ratios.min():.2f}-{ratios.max():.2f}")

# --------------------------- 2. Primary contrast: instance-level permutation test
def cellmean_judgment(sub):
    l = sub.melt(id_vars=['subject_id','test'], value_vars=JUDG,
                 var_name='cat', value_name='s')
    return l.groupby(['test','cat'])['s'].std(ddof=1).mean()

prim = valid[(valid.temperature == 1) &
             (valid.condition.isin(['c0_neutral','c3_authorship']))]
rng = np.random.default_rng(457)          # semilla = n de sujetos válidos
N_PERM = 2000
obs, perm = [], np.zeros(N_PERM)
for m in ['Haiku','Sonnet','Opus']:
    sub = prim[prim.model == m]
    obs.append(cellmean_judgment(sub[sub.condition == 'c3_authorship']) -
               cellmean_judgment(sub[sub.condition == 'c0_neutral']))
    ids = sub[['subject_id','condition']].drop_duplicates()
    for i in range(N_PERM):
        sh = ids.copy()
        sh['condition'] = rng.permutation(sh['condition'].values)
        s2 = sub.drop(columns='condition').merge(sh, on='subject_id')
        perm[i] += (cellmean_judgment(s2[s2.condition == 'c3_authorship']) -
                    cellmean_judgment(s2[s2.condition == 'c0_neutral'])) / 3
d_obs = float(np.mean(obs))
p_perm = float(np.mean(np.abs(perm) >= abs(d_obs)))
print(f"[primary perm] obs diff={d_obs:+.4f} per-model={[round(x,4) for x in obs]} "
      f"p={p_perm:.3f} (seed=457, {N_PERM} perms)")

# --------------------------------- 3. Confound (a): error placement / clean cells
tgt = valid[['test','expected']].drop_duplicates().rename(columns={'expected':'target'})
n_jt = tgt['target'].isin(JUDG).sum()
print(f"\n[placement] planted targets in judgment categories: {n_jt}/11")
sd2 = sd.merge(tgt, on='test')
clean = sd2[sd2.category != sd2.target]
cj = clean[clean.ctype == 'judgment']['sd'].mean()
cp = clean[clean.ctype == 'procedural']['sd'].mean()
cellc = (clean.groupby(['model','condition','temperature','ctype'])['sd']
              .mean().unstack('ctype'))
t2, p2 = stats.ttest_rel(cellc['judgment'], cellc['procedural'])
print(f"[clean cells] judgment={cj:.4f} procedural={cp:.4f} ratio={cj/cp:.2f} "
      f"| paired t(23)={t2:.2f} p={p2:.2e}")

# --------------------------------------------- 4. Confound (b): ceiling incidence
lt = long.merge(tgt, on='test')
lc = lt[lt.category != lt.target]
for name, frame in [('all', long), ('clean', lc)]:
    pj = (frame[frame.ctype == 'judgment']['score'] == 5).mean()
    pp = (frame[frame.ctype == 'procedural']['score'] == 5).mean()
    print(f"[ceiling {name}] %5s judgment={pj:.1%} procedural={pp:.1%}")
cc = clean.copy(); cc['div'] = (cc['sd'] > 0).astype(int)
inc = cc.groupby('ctype')['div'].mean()
print(f"[cell incidence clean] judgment={inc['judgment']:.1%} procedural={inc['procedural']:.1%}")
nm = lc.groupby('ctype')['score'].apply(lambda s:(s<5).mean())
print(f"[score non-max clean] judgment={nm['judgment']:.1%} procedural={nm['procedural']:.1%}  # 6.1/1.0 del manuscrito")

# ---------------- 5. Confound (c): serial position + trace length (logistic model)
pos = {c: i for i, c in enumerate(CATS)}
dv = sd.copy()
dv['div'] = (dv['sd'] > 0).astype(int)
dv['pos'] = dv['category'].map(pos)
dv['isj'] = (dv['ctype'] == 'judgment').astype(int)
tl = valid.copy(); tl['tlen'] = tl['thinking'].fillna('').str.len()
itl = (tl.groupby(['model','condition','temperature','test'])['tlen']
         .mean().reset_index())
dv = dv.merge(itl, on=['model','condition','temperature','test'])
logit = smf.logit('div ~ isj + pos + tlen', data=dv).fit(disp=0)
orj = np.exp(logit.params['isj'])
ci = np.exp(logit.conf_int().loc['isj'])
print(f"[serial/length] OR(judgment)={orj:.2f} [{ci[0]:.2f},{ci[1]:.2f}] "
      f"pos p={logit.pvalues['pos']:.1e}")

# -------------------------------------------------- 6. Attrition (concern 4)
allsub = raw[['subject_id','model','condition','temperature']].drop_duplicates()
allsub['excluded'] = ~allsub.subject_id.isin(valid.subject_id.unique())
_, p_cond, _, _ = stats.chi2_contingency(pd.crosstab(allsub.condition, allsub.excluded))
_, p_temp, _, _ = stats.chi2_contingency(pd.crosstab(allsub.temperature, allsub.excluded))
print(f"\n[attrition] chi2 x condition p={p_cond:.3f} | x temperature p={p_temp:.3f}")

# ----------------------------------------- 7. ICC(2,1), clean judgment cells, t=1
def icc21(cell):
    piv = cell.pivot_table(index=['test','category'], columns='subject_id',
                           values='score').dropna()
    X = piv.values; n, k = X.shape
    grand = X.mean()
    SSR = k * ((X.mean(axis=1) - grand) ** 2).sum()
    SSC = n * ((X.mean(axis=0) - grand) ** 2).sum()
    SST = ((X - grand) ** 2).sum()
    MSE = (SST - SSR - SSC) / ((n - 1) * (k - 1))
    MSR = SSR / (n - 1); MSC = SSC / (k - 1)
    return (MSR - MSE) / (MSR + (k - 1) * MSE + k * (MSC - MSE) / n)

lcl = lc[(lc.temperature == 1) & (lc.ctype == 'judgment')]
iccs = [icc21(cell) for _, cell in lcl.groupby(['model','condition'])]
print(f"[ICC(2,1)] clean judgment t=1: {min(iccs):.3f}-{max(iccs):.3f} across 12 cells")

# ------------------------------------------------- 8. Spread at temperature zero
t0 = long[long.temperature == 0]
sp = t0.groupby(['model','condition','test','category'])['score'].agg(['min','max'])
full = ((sp['min'] == 1) & (sp['max'] == 5)).sum()
r3 = (sp['max'] - sp['min'] >= 3).sum()
print(f"[t0 spread] full 1-5 cells={full} | range>=3 cells={r3}")

# --------------------------------- 9. Trace length, instance-level ANOVA (minor 5)
il = tl.groupby(['subject_id','condition'])['tlen'].mean().reset_index()
an = sm.stats.anova_lm(smf.ols('tlen ~ C(condition)', data=il).fit(), typ=2)
print(f"[trace ANOVA instance] F(3,{int(an.loc['Residual','df'])})="
      f"{an.loc['C(condition)','F']:.1f} p={an.loc['C(condition)','PR(>F)']:.2e}")

print("\nDone. Compare against the manuscript's Sensitivity Analyses section.")
