"""Figure 2: the unified materials R&D loop with agent roles, human gates and failure paths.

Schematic; drawn from the MAS-6 locus definitions in sections/03_autonomy_scale.tex.
The six stations correspond one-to-one to the six MAS-6 decision loci, so this figure
and the autonomy profile in Fig. 4 share a single vocabulary.

All connectors are routed orthogonally with explicit way-points so that no path
passes behind a station box.
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)

INK, INK2, INK3 = '#0b0b0b', '#52514e', '#898781'
GRID, SURF = '#e1e0d9', '#fcfcfb'
C_BLUE, C_ORANGE, C_GREEN = '#2a78d6', '#eb6834', '#1baf7a'

plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 7,
                     'figure.facecolor': SURF, 'savefig.facecolor': SURF,
                     'pdf.fonttype': 42})

fig = plt.figure(figsize=(6.73, 3.45))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
ax.set_xlim(0, 100); ax.set_ylim(0, 51.3)

def path(pts, color=INK2, lw=1.0, ls='-', head=True, ms=8, z=2):
    """Orthogonal polyline; arrowhead on the final segment only."""
    for i in range(len(pts) - 1):
        last = (i == len(pts) - 2)
        ax.add_patch(FancyArrowPatch(
            pts[i], pts[i + 1],
            arrowstyle='-|>' if (last and head) else '-',
            mutation_scale=ms, lw=lw, color=color, linestyle=ls,
            shrinkA=0, shrinkB=0, zorder=z, joinstyle='miter'))

# ------------------------------------------------------------------ stations
CY, H, W = 31.0, 9.0, 12.6
XS = [19.3 + 14.68 * i for i in range(6)]
STATIONS = [
    ('1  formulate', 'hypothesis and\ntarget property', C_BLUE),
    ('2  design', 'select the next\nexperiment or run', C_BLUE),
    ('3  execute', 'robot, instrument\nor solver', C_ORANGE),
    ('4  characterize', 'measure, reduce\nto features', C_ORANGE),
    ('5  interpret', 'update belief,\nquantify uncertainty', C_BLUE),
    ('6  redirect', 'revise goal, stop\nor reallocate', C_GREEN),
]
for x, (title, sub, col) in zip(XS, STATIONS):
    ax.add_patch(FancyBboxPatch((x - W / 2, CY - H / 2), W, H,
                                boxstyle='round,pad=0.35,rounding_size=1.1',
                                fc='#ffffff', ec=col, lw=1.1, zorder=4))
    ax.text(x, CY + 2.15, title, ha='center', va='center', fontsize=7.0,
            fontweight='bold', color=col, zorder=5)
    ax.text(x, CY - 1.45, sub, ha='center', va='center', fontsize=5.9,
            color=INK2, linespacing=1.30, zorder=5)

for i in range(5):
    path([(XS[i] + W / 2 + 0.5, CY), (XS[i + 1] - W / 2 - 0.5, CY)], INK2, 1.0, ms=7)

# --------------------------------------------- adaptation loop: 5 -> 2, routed over
AD_Y = 46.8
path([(XS[4] + 3.2, CY + H / 2), (XS[4] + 3.2, AD_Y), (XS[1] + 1.4, AD_Y),
      (XS[1] + 1.4, CY + H / 2 + 0.4)], C_BLUE, 1.1, ms=8, z=3)
ax.text((XS[1] + XS[4]) / 2, 49.4,
        'adaptation  |  strategy, tool or step revised from runtime state',
        ha='center', fontsize=6.4, color=C_BLUE, fontweight='bold')

# ------------------------------------------------------------------ human gates
for gx, gt, ha in zip([XS[1] - 4.2, XS[2] - 4.2, XS[5] - 3.4],
                      ['approve the plan', 'safety interlock', 'accept, veto or stop'],
                      ['center', 'center', 'center']):
    ax.plot([gx, gx], [CY + H / 2, 38.4], color=INK, lw=0.8, zorder=3)
    ax.add_patch(Circle((gx, 39.4), 1.0, fc='#ffffff', ec=INK, lw=1.0, zorder=6))
    ax.plot([gx - 0.45, gx + 0.45], [39.4, 39.4], color=INK, lw=1.0, zorder=7)
    ax.text(gx, 42.4, gt, ha=ha, fontsize=5.9, color=INK)
ax.text(1.0, 40.9, 'human\ngate', ha='left', va='center', fontsize=5.9,
        color=INK, fontweight='bold', linespacing=1.25)

# ------------------------------------------------- failure recovery: 4 -> 3, routed under
RC_Y = 24.3
path([(XS[3], CY - H / 2), (XS[3], RC_Y), (XS[2], RC_Y), (XS[2], CY - H / 2 - 0.4)],
     C_ORANGE, 0.9, ls=(0, (2.4, 1.6)), ms=7, z=3)
ax.text((XS[2] + XS[3]) / 2, RC_Y, 'repeat / recover', ha='center', va='center',
        fontsize=5.8, color=C_ORANGE, zorder=5,
        bbox=dict(fc=SURF, ec='none', pad=1.1))

# ----------------------------------------------------------------- failure tags
FAILS = ['unfalsifiable\nhypothesis', 'redundant\nsampling', 'tool misuse,\nunsafe action',
         'artefact read\nas signal', 'over-confident\nattribution', 'goal drift,\nno stopping rule']
for x, t in zip(XS, FAILS):
    ax.text(x, 21.2, t, ha='center', va='center', fontsize=5.6, color=C_ORANGE,
            linespacing=1.25, zorder=6,
            bbox=dict(fc=SURF, ec='none', pad=1.4))
ax.text(1.0, 21.2, 'characteristic\nfailure', ha='left', va='center', fontsize=5.9,
        color=C_ORANGE, fontweight='bold', linespacing=1.25, zorder=6,
        bbox=dict(fc=SURF, ec='none', pad=1.4))

# ------------------------------------------------------------- provenance bus
BUS_Y = 17.4
for x in [XS[2], XS[3], XS[4]]:
    ax.plot([x, x], [18.9, BUS_Y], color=INK3, lw=0.7, ls=(0, (1.6, 1.6)), zorder=2)
ax.plot([XS[2], XS[4]], [BUS_Y, BUS_Y], color=INK3, lw=0.7, ls=(0, (1.6, 1.6)), zorder=2)
path([(XS[3], BUS_Y), (XS[3], 13.9)], INK3, 0.7, ls=(0, (1.6, 1.6)), ms=6, z=2)

# ------------------------------------------------------------- persistent state
SB_L, SB_R, SB_B, SB_T = 31.5, 68.5, 6.6, 13.6
ax.add_patch(FancyBboxPatch((SB_L, SB_B), SB_R - SB_L, SB_T - SB_B,
                            boxstyle='round,pad=0.35,rounding_size=1.1',
                            fc='#f4f3ee', ec=INK3, lw=0.8, zorder=4))
ax.text(50.0, 11.6, 'persistent state', ha='center', fontsize=7.0,
        fontweight='bold', color=INK, zorder=5)
ax.text(50.0, 8.7, 'provenance  |  rejected options  |  calibration  |  budget',
        ha='center', fontsize=5.6, color=INK2, zorder=5)

# ------------------------------------------------------ closure run: 6 -> state -> 1
CL_Y = 10.1
path([(XS[5], CY - H / 2), (XS[5], CL_Y), (SB_R + 0.4, CL_Y)], C_GREEN, 1.2, ms=8, z=3)
path([(SB_L - 0.4, CL_Y), (XS[0], CL_Y), (XS[0], CY - H / 2 - 0.4)],
     C_GREEN, 1.2, ms=8, z=3)
ax.text(50.0, 2.6, 'closure  |  evidence updates persistent state and sets the next objective',
        ha='center', fontsize=6.4, color=C_GREEN, fontweight='bold')

fig.savefig(os.path.join(SRC, 'figures', 'fig02_closed_loop.pdf'))
fig.savefig(os.path.join(SRC, 'figures', 'fig02_closed_loop.png'), dpi=260)
fig.savefig(os.path.join(SRC, 'figures', 'fig02_closed_loop.svg'))
print('fig02 written')
