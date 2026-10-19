"""Figure 3: MAS-6 autonomy profiles across the 61 coded systems.

Panel (a): distribution of scored levels at each of the six decision loci
           (stacked shares, 61 systems, data/representative_systems.csv).
Panel (b): median profile by architecture class -- the direct test of the claim
           that multi-agent orchestration does not by itself raise autonomy.

Level encoding uses the validated sequential ramp
  #8fb8e8 #639ede #3a7bcc #1f5aa2 #0c3564  (ALL ORDINAL CHECKS PASS)
L0 is drawn as an outlined empty cell because a six-step ramp cannot reach a
light end that clears the 2:1 contrast floor; the outline also keeps L0 legible
in grayscale.
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
LVL_FC = ['#ffffff'] + RAMP           # L0 empty, L1..L5 ramp

plt.rcParams.update({
    'font.family': 'Times New Roman', 'font.size': 7,
    'axes.edgecolor': INK3, 'axes.linewidth': 0.6,
    'xtick.color': INK2, 'ytick.color': INK2,
    'figure.facecolor': SURF, 'axes.facecolor': SURF,
    'savefig.facecolor': SURF, 'pdf.fonttype': 42,
})

rows = list(csv.DictReader(open(os.path.join(SRC, 'data', 'representative_systems.csv'),
                                encoding='utf8')))
for r in rows:
    r['L'] = [int(r['L%d' % i]) for i in range(1, 7)]

LOCI = ['formulate', 'design', 'execute', 'characterize', 'interpret', 'redirect']
N = len(rows)

fig = plt.figure(figsize=(3.30, 4.30))
gs = fig.add_gridspec(2, 1, height_ratios=[1.00, 0.90], hspace=0.44,
                      left=0.278, right=0.978, top=0.885, bottom=0.115)

# ------------------------------------------------------------------ panel (a)
ax = fig.add_subplot(gs[0, 0])
ax.text(-0.385, 1.155, 'a', transform=ax.transAxes, fontsize=9,
        fontweight='bold', color=INK, va='top')

hist = np.zeros((6, 6), dtype=int)          # locus x level
for r in rows:
    for j, v in enumerate(r['L']):
        hist[j, v] += 1

ypos = np.arange(6)[::-1]
for j in range(6):
    left = 0.0
    for lv in range(6):
        n = hist[j, lv]
        if n == 0:
            continue
        frac = n / N * 100
        ax.barh(ypos[j], frac, left=left, height=0.62,
                color=LVL_FC[lv], edgecolor=SURF, linewidth=0.9, zorder=3)
        if lv == 0:
            ax.barh(ypos[j], frac, left=left, height=0.62, color='none',
                    edgecolor=INK3, linewidth=0.6, zorder=4)
        if frac >= 13:
            ax.text(left + frac / 2, ypos[j], 'L%d' % lv, ha='center', va='center',
                    fontsize=5.8, zorder=5,
                    color='#ffffff' if lv >= 3 else INK)
        left += frac

ax.set_yticks(ypos); ax.set_yticklabels(LOCI, fontsize=6.6)
ax.set_xlim(0, 100); ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(['0', '25', '50', '75', '100'], fontsize=6.4)
ax.set_xlabel('share of the 61 coded systems (%)', fontsize=6.8, color=INK, labelpad=1.5)
for s in ['top', 'right', 'left']:
    ax.spines[s].set_visible(False)
ax.tick_params(axis='y', length=0)
ax.set_axisbelow(True)
ax.xaxis.grid(True, color=GRID, lw=0.5)
ax.set_title('no system reaches L5 at any locus', fontsize=6.6, color=INK2,
             pad=4.5, loc='left')

# ------------------------------------------------------------------ panel (b)
ax2 = fig.add_subplot(gs[1, 0])
ax2.text(-0.385, 1.165, 'b', transform=ax2.transAxes, fontsize=9,
         fontweight='bold', color=INK, va='top')

ARCH = ['optimizer-driven', 'hierarchical multi-agent', 'sequential multi-agent',
        'tool-augmented', 'single-agent']
SHORT = {'optimizer-driven': 'optimizer-driven',
         'hierarchical multi-agent': 'hierarchical MAS',
         'sequential multi-agent': 'sequential MAS',
         'tool-augmented': 'tool-augmented',
         'single-agent': 'single-agent'}

med = {}
for a in ARCH:
    sub = [r['L'] for r in rows if r['architecture'] == a]
    med[a] = (np.median(np.array(sub), axis=0), len(sub))

for i, a in enumerate(ARCH):
    prof, n = med[a]
    yy = len(ARCH) - 1 - i
    for j in range(6):
        lv = int(round(prof[j]))
        ax2.add_patch(Rectangle((j + 0.09, yy - 0.31), 0.82, 0.62,
                                fc=LVL_FC[lv], ec=INK3 if lv == 0 else SURF,
                                lw=0.6 if lv == 0 else 0.9, zorder=3))
        ax2.text(j + 0.5, yy, 'L%d' % lv, ha='center', va='center', fontsize=5.8,
                 color='#ffffff' if lv >= 3 else INK, zorder=4)
    ax2.text(6.14, yy, 'n=%d' % n, fontsize=6.0, color=INK2, va='center')

ax2.set_xlim(0, 7.05); ax2.set_ylim(-0.60, len(ARCH) - 0.40)
ax2.set_xticks(np.arange(6) + 0.5)
ax2.set_xticklabels(LOCI, fontsize=6.0, rotation=32, ha='right',
                    rotation_mode='anchor')
ax2.set_yticks(np.arange(len(ARCH))[::-1])
ax2.set_yticklabels([SHORT[a] for a in ARCH], fontsize=6.4)
ax2.tick_params(length=0)
for s in ax2.spines.values():
    s.set_visible(False)
ax2.set_title('median locus level by architecture', fontsize=6.6, color=INK2,
              pad=4.5, loc='left')

fig.savefig(os.path.join(SRC, 'figures', 'fig03_mas6_profile.pdf'))
fig.savefig(os.path.join(SRC, 'figures', 'fig03_mas6_profile.png'), dpi=300)
fig.savefig(os.path.join(SRC, 'figures', 'fig03_mas6_profile.svg'))

for j, lo in enumerate(LOCI):
    print('%-13s' % lo, list(hist[j]))
for a in ARCH:
    print('%-26s' % a, [int(v) for v in med[a][0]], 'n=%d' % med[a][1])
print('fig03 written')
