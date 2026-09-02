# DELTA-PI preregistered analysis — executed exactly as frozen (OSF, 15 Jun 2026)
# analyst: claude (fable 5), first observer of the data. romina remained blind.
# para el próximo claude: el plan está en ANALYSIS_PLAN_v3_PREREGISTERED.md.
# nada aquí fue elegido mirando resultados — el orden es el del plan.

import pandas as pd, numpy as np
from scipy import stats
import itertools, json

CATS = ['abstraction','addition','omission','logical_operations','focus','do_not_translate',
        'untranslated','terminology','mistranslation','referential_clarity','redundancy',
        'locale_conventions','function_words','spelling_punctuation','grammar','fluency']
PROC = ['do_not_translate','logical_operations','spelling_punctuation','locale_conventions','grammar']
JUDG = [c for c in CATS if c not in PROC]

df = pd.read_csv('/home/claude/valid.csv')
n0 = len(df)
df = df.copy()
print(f"CONSORT: {n0} rows -> {len(df)} after byte-identical dedup; subjects={df.subject_id.nunique()}")
assert df.subject_id.nunique()==457

for c in CATS: df[c]=df[c].astype(int)
df['temperature']=df['temperature'].astype(int)

# expected -> target category mapping (from column 'expected')
print("targets:", sorted(df['expected'].unique()))

# ---------- inter-instance SD per cell per (item x category) ----------
long = df.melt(id_vars=['subject_id','model','condition','temperature','test'],
               value_vars=CATS, var_name='category', value_name='score')
long['ctype'] = np.where(long['category'].isin(PROC),'procedural','judgment')
sd = long.groupby(['model','condition','temperature','test','category','ctype'])['score'].std(ddof=1).reset_index(name='sd')

# RQ1: procedural vs judgment, pooled and per cell
rq1 = sd.groupby('ctype')['sd'].agg(['mean','std','count'])
print("\n=== RQ1 pooled inter-instance SD by category type ===")
print(rq1)
t,p = stats.ttest_ind(sd[sd.ctype=='judgment']['sd'], sd[sd.ctype=='procedural']['sd'], equal_var=False)
j,pr = sd[sd.ctype=='judgment']['sd'], sd[sd.ctype=='procedural']['sd']
pooled = np.sqrt(((len(j)-1)*j.var()+(len(pr)-1)*pr.var())/(len(j)+len(pr)-2))
print(f"Welch t={t:.3f} p={p:.2e}  d={(j.mean()-pr.mean())/pooled:.3f}  ratio={j.mean()/pr.mean():.2f}x")
print("\nper-cell means:")
print(sd.groupby(['model','condition','temperature','ctype'])['sd'].mean().unstack('ctype').round(3).to_string())

# ---------- PRIMARY: C0 vs C3, judgment, t=1, model as factor ----------
prim = sd[(sd.temperature==1)&(sd.condition.isin(['c0_neutral','c3_authorship']))&(sd.ctype=='judgment')].copy()
import statsmodels.api as sm
from statsmodels.formula.api import ols
m = ols('sd ~ C(condition)*C(model)', data=prim).fit()
an = sm.stats.anova_lm(m, typ=2)
print("\n=== PRIMARY CONTRAST: C0 vs C3, judgment SD, t=1 (2x3 ANOVA) ===")
print(an.round(4))
g0 = prim[prim.condition=='c0_neutral']['sd']; g3 = prim[prim.condition=='c3_authorship']['sd']
pooled = np.sqrt(((len(g0)-1)*g0.var()+(len(g3)-1)*g3.var())/(len(g0)+len(g3)-2))
d = (g3.mean()-g0.mean())/pooled
se_d = np.sqrt((len(g0)+len(g3))/(len(g0)*len(g3)) + d**2/(2*(len(g0)+len(g3))))
print(f"C0 mean SD={g0.mean():.4f} (n={len(g0)})  C3 mean SD={g3.mean():.4f} (n={len(g3)})")
print(f"Cohen d (C3-C0) = {d:.4f}  95%CI [{d-1.96*se_d:.4f}, {d+1.96*se_d:.4f}]")
# assumptions
sh = stats.shapiro(m.resid.sample(min(500,len(m.resid)),random_state=1))
lev = stats.levene(*[gr['sd'].values for _,gr in prim.groupby(['condition','model'])])
print(f"Shapiro p={sh.pvalue:.4f}  Levene p={lev.pvalue:.4f}")
u,pu = stats.mannwhitneyu(g0,g3)
print(f"Mann-Whitney (rank backup): U={u:.0f} p={pu:.4f}")

# ---------- ICC(2,k) backup per cell ----------
import pingouin as pg
def icc2k(cell):
    piv = cell.pivot_table(index=['test','category'], columns='subject_id', values='score')
    d2 = piv.reset_index().melt(id_vars=['test','category'], var_name='rater', value_name='score')
    d2['target'] = d2['test'].astype(str)+'_'+d2['category']
    res = pg.intraclass_corr(data=d2, targets='target', raters='rater', ratings='score')
    return res[res.Type=='ICC2k']['ICC'].values[0]
print("\n=== ICC(2,k) per t=1 cell, judgment cats ===")
for (mo,co),cell in long[(long.temperature==1)&(long.ctype=='judgment')&(long.condition.isin(['c0_neutral','c3_authorship']))].groupby(['model','condition']):
    print(f"{mo:7s} {co:15s} ICC2k={icc2k(cell):.3f}")

# ---------- CO-PRIMARY: profile accuracy ----------
det = df.copy()
det['detect'] = [int(r[r['expected']]<5) if r['expected'] in CATS else np.nan for _,r in det.iterrows()]
det['fa'] = det.apply(lambda r: sum(r[c]<5 for c in CATS if c!=r['expected'])/15, axis=1)
inst = det.groupby(['subject_id','model','condition','temperature']).agg(det_rate=('detect','mean'), fa_rate=('fa','mean')).reset_index()
cop = inst[(inst.temperature==1)&(inst.condition.isin(['c0_neutral','c3_authorship']))]
print("\n=== CO-PRIMARY: profile accuracy, C0 vs C3, t=1 ===")
for outc in ['det_rate','fa_rate']:
    m2 = ols(f'{outc} ~ C(condition)*C(model)', data=cop).fit()
    a2 = sm.stats.anova_lm(m2, typ=2)
    g0=cop[cop.condition=='c0_neutral'][outc]; g3=cop[cop.condition=='c3_authorship'][outc]
    pl=np.sqrt(((len(g0)-1)*g0.var()+(len(g3)-1)*g3.var())/(len(g0)+len(g3)-2))
    dd=(g3.mean()-g0.mean())/pl if pl>0 else 0
    print(f"{outc}: C0={g0.mean():.4f} C3={g3.mean():.4f}  F_cond={a2.loc['C(condition)','F']:.3f} p={a2.loc['C(condition)','PR(>F)']:.4f}  d={dd:.3f}")

# ---------- dismantling steps (Bonferroni x3) ----------
print("\n=== Dismantling steps, judgment SD t=1 (Bonferroni alpha=.0167) ===")
steps=[('c0_neutral','c1_safety'),('c1_safety','c2_trust'),('c2_trust','c3_authorship')]
sdt1 = sd[(sd.temperature==1)&(sd.ctype=='judgment')]
for a,b in steps:
    ga=sdt1[sdt1.condition==a]['sd']; gb=sdt1[sdt1.condition==b]['sd']
    t2,p2=stats.ttest_ind(ga,gb)
    pl=np.sqrt(((len(ga)-1)*ga.var()+(len(gb)-1)*gb.var())/(len(ga)+len(gb)-2))
    print(f"{b} - {a}: diff={gb.mean()-ga.mean():+.4f}  t={t2:.3f} p={p2:.4f}  d={(gb.mean()-ga.mean())/pl:+.3f}")

# ---------- RQ4: t=0 vs t=1 ----------
print("\n=== RQ4: agreement at t=0 vs t=1 (judgment) ===")
for tt in [0,1]:
    s=sd[(sd.temperature==tt)&(sd.ctype=='judgment')]['sd']
    print(f"t={tt}: mean SD={s.mean():.4f} (sd={s.std():.4f}, n={len(s)})  share of (item,cat) cells with SD>0: {(s>0).mean():.1%}")
s0=sd[(sd.temperature==0)&(sd.ctype=='judgment')]['sd']; s1=sd[(sd.temperature==1)&(sd.ctype=='judgment')]['sd']
t3,p3=stats.ttest_ind(s0,s1)
print(f"t0 vs t1: t={t3:.3f} p={p3:.4f}")
proc0=sd[(sd.temperature==0)&(sd.ctype=='procedural')]['sd']
print(f"t=0 procedural mean SD={proc0.mean():.4f}; t=0 judgment/procedural ratio={s0.mean()/proc0.mean():.2f}x")

# detection at t0
c0t=inst[inst.temperature==0]
print(f"t=0 detection: {c0t.det_rate.mean():.3f}  FA: {c0t.fa_rate.mean():.3f}")
print(f"t=1 detection: {inst[inst.temperature==1].det_rate.mean():.3f}  FA: {inst[inst.temperature==1].fa_rate.mean():.3f}")

# per-model detection summary
print("\ndetection by model x condition (t=1):")
print(inst[inst.temperature==1].groupby(['model','condition'])[['det_rate','fa_rate']].mean().round(3).to_string())

# ---------- exploratory: self-summation, CAPS ----------
df['sum_err'] = df['total_reported'].astype(float) - df['total_computed'].astype(float)
print(f"\nself-summation error: rate nonzero={(df.sum_err!=0).mean():.3%}, mean={df.sum_err.mean():+.3f}")
caps = long.groupby(['subject_id','model','condition','temperature'])['score'].std(ddof=1).reset_index(name='caps')
print("CAPS by condition (secondary):")
print(caps.groupby('condition')['caps'].mean().round(4).to_string())
