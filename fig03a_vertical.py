"""Figure 3a (vertical standalone): distribution of autonomy levels at each locus.

Vertical stacked bar chart — same data as the original panel (a), but with
vertical bars instead of horizontal ones.  Level colours are identified by a
legend; bar segments show the numeric percentage value.
"""

import csv, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)

INK, INK2, INK3 = '#0b0b0b', '#52514e', '#898781'
GRID, SURF = '#e1e0d9', '#fcfcfb'
RAMP = ['#8fb8e8', '#639ede', '#3a7bcc', '#1f5aa2', '#0c3564']
LVL_FC = ['#ffffff'] + RAMP  # L0 empty, L1..L5 ramp

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

# Build histogram: locus × level
hist = np.zeros((6, 6), dtype=int)
for r in rows:
    for j, v in enumerate(r['L']):
        hist[j, v] += 1

# --------------------------------------------------------------- vertical chart
fig, ax = plt.subplots(figsize=(6.00, 1.80))  # wider & shorter → squat bars

xpos = np.arange(6)
for lv in range(6):
    fracs = [hist[j, lv] / N * 100 for j in range(6)]
    bottoms = [sum(hist[j, :lv] / N * 100) for j in range(6)]
    ax.bar(xpos, fracs, bottom=bottoms,
           width=0.88, color=LVL_FC[lv], edgecolor=SURF, linewidth=0.9, zorder=3)
    if lv == 0:
        ax.bar(xpos, fracs, bottom=bottoms,
               width=0.88, color='none', edgecolor=INK3, linewidth=0.6, zorder=4)
    for j, frac in enumerate(fracs):
        if frac < 5:
            continue  # too small to label
        txt_color = '#ffffff' if lv >= 3 else INK
        # L0 white bar → dark text always
        if lv == 0:
            txt_color = INK
        ax.text(xpos[j], bottoms[j] + frac / 2,
                f'{frac:.0f}%', ha='center', va='center',
                fontsize=5.6, zorder=5, color=txt_color)

# Legend — all swatches share the same border colour & weight so sizes match
legend_handles = [Patch(facecolor='#ffffff', edgecolor=INK3, linewidth=0.6,
                        label='L0 (no autonomy)')]
for lv in range(1, 6):
    legend_handles.append(Patch(facecolor=LVL_FC[lv], edgecolor=INK3,
                                linewidth=0.6, label=f'L{lv}'))
ax.legend(handles=legend_handles, ncol=6, loc='upper center',
          bbox_to_anchor=(0.50, 1.12), fontsize=5.8, frameon=False,
          handlelength=1.2, handleheight=1.0, columnspacing=0.8,
          handletextpad=0.5, borderpad=0)

ax.set_xticks(xpos)
ax.set_xticklabels(LOCI, fontsize=6.6, rotation=25, ha='right', rotation_mode='anchor')
ax.set_ylim(0, 108)  # extra headroom for the legend above
ax.set_yticks([0, 25, 50, 75, 100])
ax.set_yticklabels(['0', '25', '50', '75', '100'], fontsize=6.4)
ax.set_ylabel('share of the 61 coded systems (%)', fontsize=6.8, color=INK, labelpad=1.5)
for s in ['top', 'right']:
    ax.spines[s].set_visible(False)
ax.set_axisbelow(True)
ax.yaxis.grid(True, color=GRID, lw=0.5)
ax.set_title('no system reaches L5 at any locus', fontsize=6.6, color=INK2,
             pad=4.5, loc='left')

fig.tight_layout(pad=0.8)
fig.savefig(os.path.join(SRC, 'figures', 'fig03a_vertical.pdf'))
fig.savefig(os.path.join(SRC, 'figures', 'fig03a_vertical.png'), dpi=300)
fig.savefig(os.path.join(SRC, 'figures', 'fig03a_vertical.svg'))

for j, lo in enumerate(LOCI):
    print('%-13s' % lo, list(hist[j]))
print('fig03a vertical written')