"""Standalone scatter plot: 61 coded systems positioned by loop-closure layer & autonomy breadth.

Extracted from fig01_conceptual_space.py (panel b only).
"""
import csv, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)

# ---------- palette ----------
INK, INK2, INK3 = '#000000', '#52514e', '#000000'
GRID, SURF = '#e1e0d9', '#fcfcfb'
C_AGENTIC, C_PARTIAL, C_AUTO = '#2a78d6', '#eb6834', '#1baf7a'

plt.rcParams.update({
    'font.family': 'Times New Roman', 'font.size': 8,
    'axes.edgecolor': INK3, 'axes.linewidth': 0.6,
    'xtick.color': INK2, 'ytick.color': INK2,
    'xtick.labelsize': 8, 'ytick.labelsize': 8,
    'figure.facecolor': SURF, 'axes.facecolor': SURF,
    'savefig.facecolor': SURF, 'pdf.fonttype': 42,
})

# ---------- load data ----------
rows = list(csv.DictReader(
    open(os.path.join(SRC, 'data', 'representative_systems.csv'), encoding='utf8')
))
for r in rows:
    r['L'] = [int(r['L%d' % i]) for i in range(1, 7)]
    r['breadth'] = sum(1 for v in r['L'] if v >= 3)
    r['dac'] = int(r['D']) + int(r['A']) + int(r['C'])

# ---------- figure ----------
fig, ax = plt.figure(figsize=(5, 5)), plt.gca()

ax.text(-0.08, 1.02, 'b', transform=ax.transAxes, fontsize=10,
        fontweight='bold', color=INK, va='top')

LAYERS = ['knowledge', 'computational', 'experimental']
GROUND = {'symbolic': 'o', 'simulated': 's', 'robotic': '^'}
CLS = {3: ('agentic (D+A+C)', C_AGENTIC),
       2: ('two criteria met', C_PARTIAL),
       1: ('automation or tool use', C_AUTO),
       0: ('automation or tool use', C_AUTO)}

# alternating band for even-indexed layer columns
for i in range(len(LAYERS)):
    if i % 2 == 0:
        ax.add_patch(Rectangle((i - 0.5, -0.55), 1.0, 7.15,
                               fc='#f4f3ee', ec='none', zorder=0))

# horizontal grid lines
for y in range(0, 7):
    ax.axhline(y, color=GRID, lw=0.6, zorder=1)

# scatter
rng = np.random.default_rng(7)
seen = set()
for r in rows:
    xi = LAYERS.index(r['layer'])
    lab, col = CLS[r['dac']]
    mk = GROUND[r['grounding']]
    key = (lab, col)
    ax.scatter(xi + rng.uniform(-0.30, 0.30),
               r['breadth'] + rng.uniform(-0.17, 0.17),
               s=38, marker=mk, facecolor=col, edgecolor='#ffffff',
               linewidth=0.8, alpha=0.92, zorder=3,
               label=lab if key not in seen else None)
    seen.add(key)

# axes & spines
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(-0.55, 8.60)
ax.set_xticks(range(3))
ax.set_xticklabels(['knowledge', 'computational', 'experimental'])
ax.set_yticks(range(0, 7))
ax.set_xlabel('layer at which the loop closes', fontsize=8.2, color=INK, labelpad=2)
ax.set_ylabel('MAS-6 loci scored L3 or above', fontsize=8.2, color=INK, labelpad=2)
for s in ['top', 'right']:
    ax.spines[s].set_visible(False)
ax.spines['left'].set_bounds(0, 6)

# legend
ORDER = ['agentic (D+A+C)', 'two criteria met', 'automation or tool use']
h, l = ax.get_legend_handles_labels()
idx = [l.index(x) for x in ORDER if x in l]
leg = ax.legend([h[i] for i in idx], [l[i] for i in idx],
                loc='upper left', bbox_to_anchor=(0.01, 0.99),
                fontsize=7, frameon=False, handletextpad=0.20,
                labelspacing=0.30, title='DAC status', title_fontsize=7,
                borderpad=0.1, borderaxespad=0.2)
leg.get_title().set_color(INK2)
leg.get_title().set_ha('left')

# grounding key — encoded by marker
ax.text(1.06, 8.34, 'grounding', fontsize=7, color=INK2, va='center')
for j, (g, m) in enumerate(GROUND.items()):
    yk = 7.86 - j * 0.60
    ax.scatter(1.13, yk, marker=m, s=30, facecolor=INK2,
               edgecolor='none', linewidth=0, zorder=4)
    ax.text(1.28, yk, g, fontsize=6.5, color=INK2, va='center')

# ---------- save ----------
out_pdf = os.path.join(SRC, 'figures', 'fig01b_scatter.pdf')
out_png = os.path.join(SRC, 'figures', 'fig01b_scatter.png')
fig.savefig(out_pdf)
fig.savefig(out_png, dpi=260)
out_svg = os.path.join(SRC, 'figures', 'fig01b_scatter.svg')
fig.savefig(out_svg)
print(f'Panel-b scatter written to:')
print(f'  {out_pdf}')
print(f'  {out_png}')
print(f'  {out_svg}')
print(f'  {len(rows)} systems plotted')