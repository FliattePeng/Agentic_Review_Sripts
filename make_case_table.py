"""Regenerate tables/tbl03_case_comparison.tex from data/representative_systems.csv.

The table is the only place the full coding appears; every row carries a citation
key that exists in refs/agentic.bib, so \\citet keeps table and bibliography
consistent by construction.
"""
import csv, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)

rows = list(csv.DictReader(open(os.path.join(SRC, 'data', 'representative_systems.csv'),
                                encoding='utf8')))

ORDER = {'knowledge': 0, 'computational': 1, 'experimental': 2}
rows.sort(key=lambda r: (ORDER[r['layer']], int(r['year']), r['system_name'].lower()))

ARCH = {'scripted automation': 'scripted', 'optimizer-driven': 'optimizer',
        'single-agent': 'single', 'tool-augmented': 'tool-aug.',
        'sequential multi-agent': 'sequential MAS',
        'hierarchical multi-agent': 'hierarchical MAS',
        'generative model': 'generative'}
GRND = {'symbolic': 'sym.', 'simulated': 'sim.', 'robotic': 'rob.'}
LAYER = {'knowledge': 'knowledge', 'computational': 'computational',
         'experimental': 'experimental'}

def esc(s):
    for a, b in [('&', r'\&'), ('%', r'\%'), ('_', r'\_'), ('#', r'\#')]:
        s = s.replace(a, b)
    return s

HEADNOTE = (
    r'DAC gives delegation/adaptation/closure as Y or N. The MAS-6 profile lists '
    r'levels at the six decision loci in the order formulate--design--execute--'
    r'characterize--interpret--redirect. Grounding (Gr.) is symbolic, simulated or '
    r'robotic; evidence (Ev.) is E1 in silico, E2 retrospective, E3 prospective '
    r'experimental or E4 independently reproduced; HIR records whether human '
    r'intervention is disclosed anywhere in the source. Every entry is coded from '
    r'methods, results and supporting information, never from a title or abstract, '
    r'and the table is generated from \texttt{data/representative\_systems.csv}.')

COLS = (r'\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}'
        r'p{2.55cm}p{0.40cm}p{1.72cm}p{1.52cm}p{0.36cm}p{0.62cm}p{1.48cm}p{0.32cm}p{0.30cm}}')
HEADER = (r'System & Yr & Domain & Architecture & Gr. & DAC & MAS-6 profile & '
          r'Ev. & HIR \\')

GROUPS = [
    ('knowledge',
     r'Cross-system coding of the 61 representative systems, part 1 of 3: '
     r'systems whose scientific loop closes at the knowledge layer. ' + HEADNOTE,
     r'\label{tab:representative-systems}'),
    ('computational',
     r'Cross-system coding, part 2 of 3: systems whose loop closes at the '
     r'computational layer. Conventions as in Table~\ref{tab:representative-systems}.',
     r'\label{tab:representative-systems-comp}'),
    ('experimental',
     r'Cross-system coding, part 3 of 3: systems whose loop closes at the '
     r'experimental layer. Conventions as in Table~\ref{tab:representative-systems}.',
     r'\label{tab:representative-systems-exp}'),
]

out = []
for layer, cap, lab in GROUPS:
    sub = [r for r in rows if r['layer'] == layer]
    out.append(r'\begin{table*}[!tp]')
    out.append(r'\footnotesize')
    out.append(r'\caption{%s}' % cap)
    out.append(lab)
    out.append(COLS)
    out.append(r'\hline')
    out.append(HEADER)
    out.append(r'\hline')
    for r in sub:
        dac = ''.join('Y' if r[k] == '1' else 'N' for k in ('D', 'A', 'C'))
        prof = '--'.join(r['L%d' % i] for i in range(1, 7))
        out.append('%s & %s & %s & %s & %s & %s & %s & %s & %s ' % (
            esc(r['system_name']) + r'\cite{' + r['key'] + '}',
            r['year'][2:],
            esc(r['domain']),
            ARCH[r['architecture']],
            GRND[r['grounding']],
            dac,
            prof,
            r['evidence_level'],
            'Y' if r['intervention_reported'] == 'yes' else 'N') + r'\\')
    out.append(r'\hline')
    out.append(r'\end{tabular*}')
    out.append(r'\end{table*}')
    out.append('')

path = os.path.join(SRC, 'tables', 'tbl03_case_comparison.tex')
open(path, 'w', encoding='utf8').write('\n'.join(out) + '\n')
print('wrote', path, len(rows), 'rows in', len(GROUPS), 'floats')
