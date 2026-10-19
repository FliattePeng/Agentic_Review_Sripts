"""Figure 1: conceptual framework -- decision rights x loop-closure layer x grounding.

Panel (a) is the DAC boundary test (schematic).
Panel (b) locates the 61 coded systems in data/representative_systems.csv.
Autonomy breadth = number of MAS-6 loci scored L3 or above (source-coded, not inferred).

Palette: validated with dataviz scripts/validate_palette.js
  categorical #2a78d6 / #eb6834 / #1baf7a -- ALL CHECKS PASS (light, surface #fcfcfb)
"""
import csv, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)

INK, INK2, INK3 = '#0b0b0b', '#52514e', '#898781'
GRID, SURF = '#e1e0d9', '#fcfcfb'
C_AGENTIC, C_PARTIAL, C_AUTO = '#2a78d6', '#eb6834', '#1baf7a'

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 7,
    'axes.edgecolor': INK3, 'axes.linewidth': 0.6,
    'xtick.color': INK2, 'ytick.color': INK2,
    'xtick.labelsize': 7, 'ytick.labelsize': 7,
    'figure.facecolor': SURF, 'axes.facecolor': SURF,
    'savefig.facecolor': SURF, 'pdf.fonttype': 42,
})

rows = list(csv.DictReader(open(os.path.join(SRC, 'data', 'representative_systems.csv'),
                                encoding='utf8')))
for r in rows:
    r['L'] = [int(r['L%d' % i]) for i in range(1, 7)]
    r['breadth'] = sum(1 for v in r['L'] if v >= 3)
    r['dac'] = int(r['D']) + int(r['A']) + int(r['C'])

fig = plt.figure(figsize=(6.73, 3.05))
gs = fig.add_gridspec(1, 2, width_ratios=[1.00, 1.32], wspace=0.20,
                      left=0.045, right=0.995, top=0.90, bottom=0.115)

# ---------------------------------------------------------------- panel (a)
ax = fig.add_subplot(gs[0, 0]); ax.set_axis_off()
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.text(-0.35, 9.85, 'a', fontsize=9, fontweight='bold', color=INK, va='top')

def box(x, y, w, h, label, sub, fc, ec, tc=INK, fs=7, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.10,rounding_size=0.22',
                                fc=fc, ec=ec, lw=0.8))
    ax.text(x + w / 2, y + h * (0.62 if sub else 0.5), label, ha='center', va='center',
            fontsize=fs, color=tc, fontweight='bold' if bold else 'normal')
    if sub:
        ax.text(x + w / 2, y + h * 0.24, sub, ha='center', va='center',
                fontsize=6.2, color=INK2)

def arrow(x0, y0, x1, y1, color=INK2, lw=0.9, style='-|>'):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style,
                                 mutation_scale=7, lw=lw, color=color,
                                 shrinkA=0, shrinkB=0))

crit = [
    (8.05, 'Delegation', 'objective set at the level of\nscientific intent, not procedure'),
    (5.35, 'Adaptation', 'strategy, tools or steps\nrevised from runtime state'),
    (2.65, 'Closure', 'evidence updates persistent\nstate and drives the next action'),
]
BW = 5.05
for ypos, name, desc in crit:
    ax.add_patch(FancyBboxPatch((0.15, ypos), BW, 1.42,
                                boxstyle='round,pad=0.10,rounding_size=0.22',
                                fc='#ffffff', ec=INK3, lw=0.8))
    ax.text(0.45, ypos + 1.00, name, fontsize=7.2, fontweight='bold', color=INK, va='center')
    ax.text(0.45, ypos + 0.44, desc, fontsize=6.0, color=INK2, va='center', linespacing=1.25)
    # fail branch
    arrow(5.30, ypos + 0.71, 6.55, ypos + 0.71, color=INK3, lw=0.8)
    ax.text(5.92, ypos + 0.90, 'no', fontsize=6.0, color=INK3, ha='center')

CX = 2.68
arrow(CX, 8.05, CX, 6.77)
arrow(CX, 5.35, CX, 4.07)
ax.text(CX + 0.20, 7.40, 'yes', fontsize=6.0, color=INK2)
ax.text(CX + 0.20, 4.70, 'yes', fontsize=6.0, color=INK2)

box(6.55, 8.20, 3.35, 1.12, 'scripted', 'automation', '#ffffff', C_AUTO, fs=6.8)
box(6.55, 5.50, 3.35, 1.12, 'tool-augmented', 'model', '#ffffff', C_PARTIAL, fs=6.8)
box(6.55, 2.80, 3.35, 1.12, 'agent', 'loop not closed', '#ffffff', C_PARTIAL, fs=6.8)

arrow(CX, 2.65, CX, 1.72)
ax.text(CX + 0.20, 2.10, 'yes', fontsize=6.0, color=INK2)
ax.add_patch(FancyBboxPatch((0.15, 0.35), BW, 1.32,
                            boxstyle='round,pad=0.10,rounding_size=0.22',
                            fc='#eaf2fd', ec=C_AGENTIC, lw=1.2))
ax.text(0.15 + BW / 2, 1.16, 'agentic system', ha='center', fontsize=7.4,
        fontweight='bold', color=C_AGENTIC)
ax.text(0.15 + BW / 2, 0.66, 'all three met for a stated scope',
        ha='center', fontsize=6.0, color=INK2)

# ---------------------------------------------------------------- panel (b)
ax2 = fig.add_subplot(gs[0, 1])
ax2.text(-0.115, 1.045, 'b', transform=ax2.transAxes, fontsize=9,
         fontweight='bold', color=INK, va='top')

LAYERS = ['knowledge', 'computational', 'experimental']
GROUND = {'symbolic': 'o', 'simulated': 's', 'robotic': '^'}
CLS = {3: ('agentic (D+A+C)', C_AGENTIC), 2: ('two criteria met', C_PARTIAL),
       1: ('automation or tool use', C_AUTO), 0: ('automation or tool use', C_AUTO)}

for i in range(len(LAYERS)):
    if i % 2 == 0:
        ax2.add_patch(Rectangle((i - 0.5, -0.55), 1.0, 7.15, fc='#f4f3ee',
                                ec='none', zorder=0))
for y in range(0, 7):
    ax2.axhline(y, color=GRID, lw=0.6, zorder=1)

rng = np.random.default_rng(7)
seen = set()
for r in rows:
    xi = LAYERS.index(r['layer'])
    lab, col = CLS[r['dac']]
    mk = GROUND[r['grounding']]
    key = (lab, col)
    ax2.scatter(xi + rng.uniform(-0.30, 0.30), r['breadth'] + rng.uniform(-0.17, 0.17),
                s=17, marker=mk, facecolor=col, edgecolor=SURF, linewidth=0.55,
                alpha=0.92, zorder=3,
                label=lab if key not in seen else None)
    seen.add(key)

ax2.set_xlim(-0.5, 2.5); ax2.set_ylim(-0.55, 8.60)
ax2.set_xticks(range(3)); ax2.set_xticklabels(['knowledge', 'computational', 'experimental'])
ax2.set_yticks(range(0, 7))
ax2.set_xlabel('layer at which the loop closes', fontsize=7.2, color=INK, labelpad=2)
ax2.set_ylabel('MAS-6 loci scored L3 or above', fontsize=7.2, color=INK, labelpad=2)
for s in ['top', 'right']:
    ax2.spines[s].set_visible(False)
ax2.spines['left'].set_bounds(0, 6)

ORDER = ['agentic (D+A+C)', 'two criteria met', 'automation or tool use']
h, l = ax2.get_legend_handles_labels()
idx = [l.index(x) for x in ORDER if x in l]
leg = ax2.legend([h[i] for i in idx], [l[i] for i in idx],
                 loc='upper left', bbox_to_anchor=(0.005, 0.995),
                 fontsize=6.1, frameon=False, handletextpad=0.20,
                 labelspacing=0.30, title='DAC status', title_fontsize=6.1,
                 borderpad=0.1, borderaxespad=0.2)
leg.get_title().set_color(INK2)
leg.get_title().set_ha('left')

# grounding key, encoded by marker so identity never rests on colour alone
ax2.text(1.06, 8.34, 'grounding', fontsize=6.1, color=INK2, va='center')
for j, (g, m) in enumerate(GROUND.items()):
    yk = 7.86 - j * 0.60
    ax2.scatter(1.13, yk, marker=m, s=15, facecolor=INK2,
                edgecolor=SURF, linewidth=0.5, zorder=4)
    ax2.text(1.25, yk, g, fontsize=6.0, color=INK2, va='center')

fig.savefig(os.path.join(SRC, 'figures', 'fig01_conceptual_space.pdf'))
fig.savefig(os.path.join(SRC, 'figures', 'fig01_conceptual_space.png'), dpi=260)
print('fig01 written;', len(rows), 'systems plotted')
