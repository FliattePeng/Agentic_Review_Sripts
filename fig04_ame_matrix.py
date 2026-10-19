"""Figure 4: the AME evaluation matrix -- five metric families x four evidence levels.

Cell shading is the coverage actually observed in the 61 coded systems
(data/representative_systems.csv), not an aspiration: for each metric family the
cell records whether systems at that evidence level report the family at all.
Coverage is coded in data/ame_coverage.csv, whose "basis" column names the
column of representative_systems.csv or the section that justifies each entry.

E4 -- independent reproduction of a prospective result across laboratories -- is
empty for every metric family: no system in the corpus supplies it.

Palette: sequential ramp #8fb8e8 ... #0c3564 (ordinal checks PASS); unreported
cells are drawn as outlined and empty so absence never reads as a dark colour.
"""
import csv, os
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)

INK, INK2, INK3 = '#0b0b0b', '#52514e', '#898781'
GRID, SURF = '#e1e0d9', '#fcfcfb'
RAMP = ['#8fb8e8', '#639ede', '#3a7bcc', '#1f5aa2', '#0c3564']

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 7,
                     'figure.facecolor': SURF, 'axes.facecolor': SURF,
                     'savefig.facecolor': SURF, 'pdf.fonttype': 42})

rows = list(csv.DictReader(open(os.path.join(SRC, 'data', 'representative_systems.csv'),
                                encoding='utf8')))
ncase = Counter(r['evidence_level'] for r in rows)
ncase['E4'] = ncase.get('E4', 0)

cov = list(csv.DictReader(open(os.path.join(SRC, 'data', 'ame_coverage.csv'),
                               encoding='utf8')))

FAM = ['scientific quality', 'process capability', 'efficiency',
       'robustness and\nreproducibility', 'safety and\ngovernance']
FAMKEY = ['scientific_quality', 'process_capability', 'efficiency',
          'robustness', 'safety']
EV = ['E1', 'E2', 'E3', 'E4']
EVLAB = ['E1\nin silico /\nbenchmark', 'E2\nretrospective /\nrediscovery',
         'E3\nprospective\nexperiment', 'E4\nindependent\nreproduction']

M = {(c['metric_family'], c['evidence_level']): c for c in cov}

fig = plt.figure(figsize=(3.30, 3.55))
ax = fig.add_axes([0.335, 0.150, 0.650, 0.640]); ax.set_axis_off()
ax.set_xlim(0, 4); ax.set_ylim(0, 5)

LEVEL_FC = {0: '#ffffff', 1: RAMP[0], 2: RAMP[2], 3: RAMP[4]}
LEVEL_TXT = {0: 'none', 1: 'sparse', 2: 'partial', 3: 'routine'}

for i, fk in enumerate(FAMKEY):
    yy = len(FAMKEY) - 1 - i
    for j, ev in enumerate(EV):
        c = M[(fk, ev)]
        lv = int(c['coverage'])
        ax.add_patch(Rectangle((j + 0.045, yy + 0.085), 0.91, 0.83,
                               fc=LEVEL_FC[lv], ec=INK3 if lv == 0 else SURF,
                               lw=0.6 if lv == 0 else 1.1, zorder=3))
        ax.text(j + 0.5, yy + 0.50, c['label'], ha='center', va='center',
                fontsize=5.1, zorder=4, linespacing=1.28,
                color='#ffffff' if lv == 3 else INK)

for i, f in enumerate(FAM):
    ax.text(-0.075, len(FAM) - 1 - i + 0.50, f, ha='right', va='center',
            fontsize=6.0, color=INK, linespacing=1.25)
for j, e in enumerate(EVLAB):
    ax.text(j + 0.5, 5.10, e, ha='center', va='bottom', fontsize=5.4,
            color=INK2, linespacing=1.30)
for j, ev in enumerate(EV):
    ax.text(j + 0.5, -0.14, 'n = %d' % ncase[ev], ha='center', va='top',
            fontsize=5.8, color=INK2)

fig.text(0.012, 0.978, 'AME metric families × evidence level', fontsize=6.9,
         color=INK, fontweight='bold', va='top')
fig.text(0.012, 0.078,
         'shading: coverage observed across the 61 coded systems; empty cells are '
         'outlined,\nso an unreported metric never reads as a filled value.  '
         'No system supplies E4.',
         fontsize=5.3, color=INK2, va='top', linespacing=1.35)

# key -- the four coverage steps, direct-labelled (relief for the contrast WARN)
for k, (lv, lab) in enumerate(LEVEL_TXT.items()):
    x0 = 0.028 + k * 0.176
    fig.patches.append(Rectangle((x0, 0.906), 0.028, 0.021, transform=fig.transFigure,
                                 fc=LEVEL_FC[lv], ec=INK3 if lv == 0 else 'none',
                                 lw=0.6, figure=fig))
    fig.text(x0 + 0.035, 0.9165, lab, fontsize=5.4, color=INK2, va='center')

fig.savefig(os.path.join(SRC, 'figures', 'fig04_ame_matrix.pdf'))
fig.savefig(os.path.join(SRC, 'figures', 'fig04_ame_matrix.png'), dpi=300)
print('fig04 written; evidence counts', dict(ncase))
