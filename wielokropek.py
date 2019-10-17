# timestamp: 2019-10-09 14:07
# !/usr/bin/env python
# coding: utf-8

# Wielokropek / Slither Link
# unicode icons: http://xahlee.info/comp/unicode_geometric_shapes.html
from time import perf_counter
import examples
from datetime import datetime

### GLOSSARY
# cell      - any object behind coordinates (like 5.12)
# box       - kind of cell; it might contain a digit value or be empty
# boxn      - kind of cell; box with number (digit value)
# intrsc    - kind of cell; intersection; lines can go through it
# grid      - kind of cell; connects intersections; can become a line
# line      - kind of cell; part of the loop
# loop      - a loop made of lines
# combo     - combination of 4 neighbour values around one box
# edge      - edge of the displayed riddle, made of dummy symbols (makes calculations easier)

# tt        - total time
# loc       - list of changes
# floc      - final list of changes


### RIDDLE
## PARAMS
# Riddle format: 'columns,rows;digits from grid - row by row. dot(".") stands for empty'
riddle_a1 = '5,5;.33.....023..23.3..30..3.'
riddle_a2 = '6,6;.2..133.3..32.2.1...213.2131.3...2.2'
riddle_a3 = '10,12;.2..3...1..0111.13..1.3.0.32.3.3..1.1...122..32..23.......2..22...12...1.2.212..31.2323...21.1....2.1.1..12..3.3223222.3'
riddle_a4 = '17,23;..2.222.3..2.31223.2.2..1..3...1..2.21.222.1.222....133.3.12.....3.3.21...3.2.1.2.........112.2......2.2.22.1.1.22.2..2....2.2.3..232112.121.2...2.2....3212....1.2.2.1.....1..3....3.2.312.23.32.3.......1..2.112..1.3223.12....1.33.3....2.2.312.......3.2.1...1....1.232.3.....3..1...111.2.1..211.311.3.321...22..213...12.1.213.......323222232...211.3.2....2.112...312....2.2122..2...22..2..3.2'
riddle_a5 = '17,23;.2.32....2.22.3...13.11122.3.2.3.2.111.12.21.2.1..32221.1.1.......12...12.1...31..1...222......21.1.1..2....321....31.3....3.....2.123....32..2......1..3....22113.2.32....12.1.312.1..2..131..221.1..321..2..2....2...1.....211.2.2.2.....2....23..121.32222....2.11.2.2...1.3132..3.21232.2212..1..11323.11..11..21.2..12.212...21.......1..2...23..13.2..3..21.21..1...221.23.3.112.22.23.3.......33'
riddle_a6 = '25,30;....213.3.02.2.22..22.3.32..13..3.3...23......22..3221.2..1....2.12232........2322....1........11......1.....3...2..31.2.3...23.3..13..2.2211.13.3..21..2.0.....3....2.2...2...22.32....21322123.113.2122.31.....2...22.....2...32....2.3.12.31...2212..3.2..212.23..231.21.13..13.1...2.....2.312.......1..222.23.2.33..1.1...3....3.2..21.3....32.2..3112.....22..1.3....12.3..1...33.20212.21..223..3..2..22.2.3...1...23.21..13...1..22.1223..2.122.....2....3.22..3..........3.3..3....31....323.2..3.....1.212.13..3.121..2...23.3...322..1...2.....22.21213....1.31...03.33..31.......3..2.....2..20.1..312.221222..312...2..22213.....23.3...2222.3..2.2..23....2...3.2..121.2..2..0312..3.21.1.113.322.3.2...22213.3..2221.121....3..1.2..12.21.....3....23...3..2...'
# aa_870:  https://www.janko.at/Raetsel/Slitherlink/0870.a.htm
riddle_aa_870 = '45,31;3..022..023222..222.......333..333233..331..2.3.1.2..........2.2.......0.0..........1.2.2....1.2........23113..011..13233........1.1...2111.11211122.2.2....2.1....2.2.21211222.20112...........1.302....1.2....121.0...........21122.33211110.....2321.2230.....21131322.2212...2.1............3.......2............3.2....3.2.2........313.3221.1112.223........2.2.3.1..222.0120...3.3....3.1....2.3...1322.333..0.......3..2...32201..2.1..22303...1..3.......1103...2..1.....1.2..1.1..2.2.....2..1...1333....22.1211.332.221..1.2..212.331.3010.03.........2......2.1......1.1......2.2......3.....210...2.....1.2......1.1......2.2.....2...332...3..3..0112.21103210132122223.2221..1..0......3..2..2...........1.2...........3..3..1......3..1..1121.23131222131222322.1203..2..0...312...2.....2.2......1.3......2.3.....1...332.....2......2.2......1.3......2.2......3.........33.1232.222.133..2.2..222.232.3012.01....3132...3..2.....0.2..1.2..2.2.....3..1...0101.......3..1...12222..1.3..12231...2..2.......3..232.2101...2.2....2.2....2.3...3311.321..0.2.3.3........112.1220.2222.232........3.1.1....3.3............1.......1............2.1...2332.32221202.....2133.3113.....33132221.12123...........1.131....2.3....123.0...........13223.12201022.2.3....3.3....2.1.12212112.1312...2.1........22223..303..20311........1.1....1.1.1..........1.1.......1.2..........1.2.3.0..212..332333..223.......113..223323..222..1'
riddle_aa_96 = '16,12;...12..2.12.2.3.3211........1.1.1..1.131.2.2...1.1..10.2.3113.1..2..3...2....0.3.121.12.1.20.....13......2...2223..323.31.1.12...2.2.3..0..1..3...2........13...2..11.32.2....012..23..11.3122..'
riddle_aa_98 = '30,20;31..22.332.2..11.3...3.3.0..31..1121..0...3..12.02...1....1.3.....211...2..2.....333...3.1..112..2..13..1.32...11..2..2.1.13..1..13.02..3..1..2....213....1..32...2.1.1...0....2....11.3..1.22..11..212212.1..313.2.2..2.3.1..3..2.1.....3..2.31..3..31.1.3.11...1..32..3.21...1..1.3..31...32...1.1.2.12.2.13...3....32.....1.1..31.2..12..13..2.1....3..2..33..2..2.323.1..3....1..3.11..1..1...31.....12.322.33....23..1.123.22.23..1..10.......113..11.3.22.231.1.22.1.1322......3.1...31.221.02.21..12..20..30....1...3..2..2....312.2....2....2..2.1...1.2.1.2.2.....1..31.11.223..3.2...23...23.2112...3..1.3.222'
riddle_aa_194 = '40,30;...3.3222.2...2..20.3...3.3.....2..3.1...2.2312.1..21...23.3.223...2.121..2.2....3..1.......13....1.....313..1..22.2.23.....3.1132.22.1.1.2..3.........212011.3..2.1....2222..33.31...12.1.32...33..213.30..3.3..1..3...1.313.3.3...1121...12.2....221.2.23022....1.222..123....23..12....2.2..1...2....21.....32.2.0......2.2..2.1.32....3..2......22.21..1.3..30...1...222..2220...23..20..3...21.3...2...3..11...2.2.3...211.23.3131...11......1.22.2.22.13..2....2.231.12.22..1..13.3..1.2.11.3...3...23............1...223..022...3..1.......21.132.32.3..2..21...2.2.221.2...12.3..2.2.231...2.23.2....23.1312322...1.3..2.12..1..3..2..11..3......3........31.3.......3..22.....2.1..3.33222.321323..12.3.112..12.2.2.31...32.2..3.........3....3..32...22.3..22......3.22.3.0.12.3...3.31...302.2..3.2.2.........3..2..211.30..2.22.3...2.....221...2...1.1.0..2.....3..23.....2..2..22.1.13.22...1.1...........1..11...3...32.22.2..22...1.131.32.2.3.3.3.........2213.....12.2.......23..3....3...21..31.2.212..32.22.222....3....3.2..03.3......2..22...2..33.33.2.2.32.2.22.....3.2.032.23...3.33..2.2..1..3.2.2..22...22.3.2.22.2132.2111.12..1....12...2..212.3....23....2.....1..2.3.213233.3322..323......2..3..3..32...2...23..'

riddle_a0 = '4,4;......1..1......'
riddle_a01 = '3,3;....1.1..'
riddle_a02 = '4,4;......1..2..1...'
# riddle_ah1 - https://pl.puzzle-loop.com/?size=9 (25,30 hard)
riddle_ah1 = '25,30;3.23....1..13..3.31...2.3.......23..3..2.132...2....2.12.2110...2.13..2..3..22.231.2...3.1.2.3.3..2.3.222.222..1.132.....3.....323......3.3....332.12..212..1...1......1.0..3......13.3..3...2.1.....22.....2..1.23.23..221..33..31.31...22.231....2..0.23..1.1..1...1.1.....3.2..23..3...2.....2........2...2203....3.2.13.110...3.2.1.13.22..3.21..3.132..22...1.3.1......3.2.32...2.0...2....3.121.2.2....3.2.3.....2.0...3...1.3..13.31..22..22.12....23....2..2...2..2.2...3.31...023.3..323.3..23.2...223...2.12.3.2..1.1...3......3..23...2.3.221...212.12........231..1..2...1.2.1...21....3223.3.33....221212..2....21...22.1.12...23..332.....2..11.12.323.1..3..3.....323...1...1.1.2..0...2.2..1.2131...33..23.031...2..1313.2.2.221.1..2.312.3.3.........2..3.3..'
# riddle_ah2 - https://pl.puzzle-loop.com/?size=7 (20,20 hard)
riddle_ah2 = "20,20;...2.2322.23.....2..2..1.1.3..1...31..222..1.3....2.1..12..32.22....2133.2...2....11.22..2..3120..211.3...2.1.21....3......2230.....3.12..12213..3..2..1...3...3.232211...3223.2..1..221.22.2.2.21.3123223...2..1..3..1.2.21.2.....333.2.....212.3.3.....21..11......1221212..2...33...1.2.123.3.1.2..1.......3.212.2...3.3.1313.1.12..2.22220.3.31.32......3...2..1..1.21.1..32223.......13.2...3...3..2.23.3.."
# https://pl.puzzle-loop.com/?size=6 (15x15 hard)
riddle_ah3 = "15,15;..3...223.3....2..132..02.2.3....2..2...22.222......2101..3.3.21.21..23.....33.2..2.21.23..2...303........233.....3...2.3..22....12.2...21...3.23..0.....13..112..23.2...2...222..3...22.32.23.2..22.2...2.21.23.3233.31.2..32..."

riddle = riddle_aa_194

nl = '\u02df'  # no line
cr = '\u25cf'  # intersection
em = ' '  # empty
el = '#'  # edge line
bo = '\u25a1'  # box □
li = '-'  # line
lh = '\u2550\u2550\u2550'  # line horizontal  U.2550  ═ \u2501\u2501\u2501'
lv = '\u2551'  # line vertical U.2551  ║   '\u2503'

reversed_char = {li: nl, nl: li}

### Prepare grid
col_header, row_header = riddle.split(";")[0].split(",")
cols = list(a for a in range(0, int(col_header) * 2 + 3))
rows = list(a for a in range(0, int(row_header) * 2 + 3))
cells = [str(a) + '.' + str(b) for a in rows for b in cols]
cells_dict = dict(zip(cells, [em for c in cells]))
cols_odd, cols_even, rows_odd, rows_even = [], [], [], []
BOXES, BOXES_N, INTERSECTIONS, GRIDS = [], [], [], []
allowed_combos_dict = {}

# ALL - Allowed combinations for Box and Intersection
options = [nl, li, em]
combos = [[A, B, C, D] for A in options for B in options for C in options for D in options]
POSSIBLE_BOX = [x for x in combos if x.count(li) in (0, 1, 2, 3)]
POSSIBLE_INTRSC = [x for x in combos if x.count(li) in (0, 2)]
# FINISHED - Allowed combinations for Box and Intersection
options_f = [nl, li]
combos_f = [[A, B, C, D] for A in options_f for B in options_f for C in options_f for D in options_f]
POSSIBLE_BOX_F = [x for x in combos_f if x.count(li) in (0, 1, 2, 3)]
POSSIBLE_INTRSC_F = [x for x in combos_f if x.count(li) in (0, 2)]

for col in cols:
    if (col % 2) > 0:
        cols_odd.append(col)
    else:
        cols_even.append(col)

for row in rows:
    if (row % 2) > 0:
        rows_odd.append(row)
    else:
        rows_even.append(row)

# add intersections
for row in rows_odd:
    for col in cols_odd:
        intrsc = str(row) + '.' + str(col)
        cells_dict[intrsc] = cr
        INTERSECTIONS.append(intrsc)

# add boxes
for row in rows_even:
    for col in cols_even:
        if (col > 1 and col < len(cols) - 1) and (row > 1 and row < len(rows) - 1):
            cells_dict[str(row) + '.' + str(col)] = bo
            BOXES.append(str(row) + '.' + str(col))
# make assertment check: if len BOXES = len values

# replace '.' with actual numbers from the riddle
boxes_match = dict(zip(BOXES, [c for c in riddle.split(";")[1]]))
for box in boxes_match:
    if boxes_match[box] not in ('.'):
        cells_dict[box] = boxes_match[box]
        BOXES_N.append(box)

BOXES_N3 = [box for box in BOXES_N if cells_dict[box] == '3']

# create edges
# rows
for col in (str(0), str(len(cols) - 1)):
    for row in rows_odd:
        cells_dict[str(row) + '.' + str(col)] = nl
    for row in rows_even:
        cells_dict[str(row) + '.' + str(col)] = el
# cols
for row in (str(0), str(len(rows) - 1)):
    for col in cols_odd:
        cells_dict[str(row) + '.' + str(col)] = nl
    for col in cols_even:
        cells_dict[str(row) + '.' + str(col)] = el

# define GRID
GRIDS = [n for n in cells_dict if cells_dict[n] == em]
GRIDS_VERTICAL = [grid for grid in GRIDS if int(grid.split(".")[0]) in rows_even]
GRIDS_HORIZONTAL = [grid for grid in GRIDS if int(grid.split(".")[0]) in rows_odd]
GRIDS_COORDS_VER = dict(zip(GRIDS_VERTICAL, ([str(int(g.split(".")[0]) - 1) + '.' + g.split(".")[1],
                                              str(int(g.split(".")[0]) + 1) + '.' + g.split(".")[1]]
                                             for g in GRIDS_VERTICAL)))
GRIDS_COORDS_HOR = dict(zip(GRIDS_HORIZONTAL, ([g.split(".")[0] + '.' + str(int(g.split(".")[1]) - 1),
                                                g.split(".")[0] + '.' + str(int(g.split(".")[1]) + 1)]
                                               for g in GRIDS_HORIZONTAL)))
GRIDS_COORDS = {**GRIDS_COORDS_VER, **GRIDS_COORDS_HOR}

### HISTORY of execution
history = []


def add_to_history(history, choice, loc, empties, cmb, combos, elapsed, tt):
    history.append([choice, loc, empties, cmb, combos, round(elapsed, 1), round(tt, 1)])
    return history


def print_history(history):
    print("choice,".rjust(8), "empties,".rjust(8), "tot.em,".rjust(8), "combos,".rjust(8),
          "tot.cmb,".rjust(8), "time,".rjust(8), "tot.time".rjust(8))
    for i in history:
        print(str(i[0]).rjust(7), str(i[1]).rjust(8), str(i[2]).rjust(8), str(i[3]).rjust(8), str(i[4]).rjust(8),
              str(i[5]).rjust(8), str(i[6]).rjust(8))


### FUNCTIONS ###

# @profile
import cProfile, pstats, io


def profile(fnc):
    """A decorator that uses cProfile to profile a function"""

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner


def display(values):
    print()
    values_copy = values.copy()
    for cell in values_copy:
        if values_copy[cell] == 'e':
            values_copy[cell] = em
        if values_copy[cell] == bo:
            values_copy[cell] = em
        if values_copy[cell] == li:
            if (int(cell.split(".")[1]) in cols_odd):
                values_copy[cell] = lv
            if (int(cell.split(".")[1]) in cols_even):
                values_copy[cell] = lh

    print('     ' + ''.join((str(cols[c]) + ' ').center(3) for c in cols))  # column headers
    for r in rows:  # actual rows
        print(' ' + (str(rows[r]) + ' ').center(4)
              + ''.join((values_copy[str(r) + '.' + str(c)]).center(3) for c in cols))
    print()


def combos_len(values, allowed_combos_dict):
    combos_len = 0
    for box in unfinished_cells(values)[1]:
        if box in allowed_combos_dict:
            combos_len += len(allowed_combos_dict[box])
    return combos_len


def stats(values, allowed_combos_dict, tt):
    finished_intrsc, finished_boxes, finished_boxes_n, finished_grids, finished_lines = finished_cells(values)
    print('Empties:       ' + str(len(GRIDS) - len(finished_grids)))
    print('Intersections: ' + str(len(INTERSECTIONS)) + ' / ' + str(len(finished_intrsc)) + ' completed')
    print('Boxes:         ' + str(len(BOXES)) + ' / ' + str(len(finished_boxes)) + ' completed')
    print('Boxes N:       ' + str(len(BOXES_N)) + ' / ' + str(len(finished_boxes_n)) + ' completed')
    print('Grids:         ' + str(len(GRIDS)) + ' / ' + str(len(finished_grids)) + ' completed ('
          + str(len(finished_lines)) + " lines)")
    print('Combos:        ' + str(combos_len(values, allowed_combos_dict)))
    print("Total time:    " + str(round(tt, 2)) + 'sec (' + str(round(tt / 60, 2)) + 'min)')


def stats_start(values):
    empties = len(GRIDS) - len(finished_cells(values)[3])
    t1_start = perf_counter()
    return empties, t1_start


def stats_start_new(values, allowed_combos_dict):
    empties = len(GRIDS) - len(finished_cells(values)[3])
    t1_start = perf_counter()
    cmb_len = combos_len(values, allowed_combos_dict)
    unf_grids = unfinished_cells(values)[3]
    return empties, t1_start, cmb_len, unf_grids


def stats_end(values, empties, t1_start, print_flag, tt):
    empties_removed = empties - (len(GRIDS) - len(finished_cells(values)[3]))
    time_elapsed = round(perf_counter() - t1_start, 4)
    tt += time_elapsed
    if print_flag == 'yes':
        print('\nEMPTIES REMOVED: ', empties_removed)
        print("Time elapsed: ", time_elapsed, " seconds")
        print("Total time: ", round(tt, 2), 'sec (', round(tt / 60, 2), 'min)')
        print()
    return empties_removed, time_elapsed, tt


def stats_end_new(values, allowed_combos_dict, empties, t1_start, cmb_len, unf_grids, tt):
    empt_rmvd = empties - (len(GRIDS) - len(finished_cells(values)[3]))
    empties -= empt_rmvd
    combos_removed = cmb_len - combos_len(values, allowed_combos_dict)
    loc = [gr for gr in unf_grids if gr not in unfinished_cells(values)[3]]
    time_elapsed = round(perf_counter() - t1_start, 4)
    tt += time_elapsed
    print('\nEMPTIES REMOVED: ', empt_rmvd)
    print('COMBOS REMOVED: ', combos_removed)
    print("Time elapsed: ", time_elapsed, " seconds")
    print("Total time: ", round(tt, 2), 'sec (', round(tt / 60, 2), 'min)')
    print()
    return empt_rmvd, empties, time_elapsed, tt, combos_removed, combos_len(values, allowed_combos_dict), loc


### (UN)FINISHED CELLS
def finished_cells(values):
    finished_intrsc = [n for n in INTERSECTIONS if not cell_neighb_val(n, values)[1]]
    finished_boxes = [b for b in BOXES if not cell_neighb_val(b, values)[1]]
    finished_boxes_n = [b for b in BOXES_N if not cell_neighb_val(b, values)[1]]
    finished_grids = [b for b in GRIDS if not values[b] == em]
    finished_lines = [b for b in GRIDS if values[b] == li]
    return finished_intrsc, finished_boxes, finished_boxes_n, finished_grids, finished_lines


def unfinished_cells(values):
    unfinished_intrsc = [n for n in INTERSECTIONS if cell_neighb_val(n, values)[1]]
    unfinished_boxes = [b for b in BOXES if cell_neighb_val(b, values)[1]]
    unfinished_boxes_n = [b for b in BOXES_N if cell_neighb_val(b, values)[1]]
    unfinished_grids = [b for b in GRIDS if values[b] == em]
    unfinished_lines = [b for b in GRIDS if values[b] != li]
    return unfinished_intrsc, unfinished_boxes, unfinished_boxes_n, unfinished_grids, unfinished_lines


# NEIGHBOURS
def cell_neighbbours(cell):
    neighbours = [str(int(cell.split(".")[0]) - 1) + '.' + cell.split(".")[1],
                  cell.split(".")[0] + '.' + str(int(cell.split(".")[1]) + 1),
                  str(int(cell.split(".")[0]) + 1) + '.' + cell.split(".")[1],
                  cell.split(".")[0] + '.' + str(int(cell.split(".")[1]) - 1)]
    return neighbours


B_NEIGHBOURS_DICT = {}
for box in BOXES:
    B_NEIGHBOURS_DICT[box] = cell_neighbbours(box)
I_NEIGHBOURS_DICT = {}
for intrsc in INTERSECTIONS:
    I_NEIGHBOURS_DICT[intrsc] = cell_neighbbours(intrsc)
C_NEIGHBOURS_DICT = {**B_NEIGHBOURS_DICT, **I_NEIGHBOURS_DICT}


def cell_neighb_val(cell, values):
    neighbours = C_NEIGHBOURS_DICT[cell]
    em_neighb, nl_neighb, li_neighb, neigh_values = [], [], [], []
    for n in neighbours:
        nval = values[n]
        neigh_values.append(nval)
        if nval == em:
            em_neighb.append(n)
        elif nval == nl:
            nl_neighb.append(n)
        elif nval == li:
            li_neighb.append(n)
    return neighbours, em_neighb, nl_neighb, li_neighb, neigh_values


def dict_neighb_val(values):
    dict_neighb = {}
    for n in C_NEIGHBOURS_DICT:
        dict_neighb[n] = cell_neighb_val(n, values)
    return dict_neighb


def cell_wide_neighbours(cell, wp):
    x, y = int(cell.split('.')[0]), int(cell.split('.')[1])
    # y=int(cell.split('.')[1])
    neighb_wide = [str(x + A) + '.' + str(y + B) for A in range(-1 * wp, wp + 1) for B in range(-1 * wp, wp + 1)]
    neighb_wide.remove(cell)
    return neighb_wide


def box_wide_neighbours(box, wp):
    x, y = int(box.split('.')[0]), int(box.split('.')[1])
    neighb_wide = [str(x + A * 2) + '.' + str(y + B * 2) for A in range(-1 * wp, wp + 1) for B in
                   range(-1 * wp, wp + 1)]
    neighb_wide.remove(box)
    for neigb in sorted(neighb_wide, reverse=True):
        x, y = int(neigb.split('.')[0]), int(neigb.split('.')[1])
        if x < 1 or y < 1 or y > len(cols) - 2 or x > len(rows) - 2:
            neighb_wide.remove(neigb)
    return neighb_wide


def list_set_of3_boxes(values):
    set_of3_boxes = []
    unfin_boxes = unfinished_cells(values)[1]
    for box1 in unfin_boxes:
        box_neighb1 = box_wide_neighbours(box1, 1)
        box_neighb1_unslvd = list(set(box_neighb1).intersection(set(unfin_boxes)))
        for box2 in box_neighb1_unslvd:
            box_neighb2 = box_wide_neighbours(box2, 1)
            box_neighb2_unslvd = list(set(box_neighb2).intersection(set(unfin_boxes)))
            box_neighb3 = list(set(box_neighb1_unslvd).intersection(box_neighb2_unslvd))
            for box3 in box_neighb3:
                set_of3_box = [box1, box2, box3]
                if [box2, box1, box3] in set_of3_boxes or set_of3_box in set_of3_boxes:
                    continue
                else:
                    set_of3_boxes.append(set_of3_box)
    return set_of3_boxes


# UTILITIES
def box_corners(box):
    x, y = box.split('.')
    vals = [-1, 1]
    box_corners = [str(int(x) + A) + '.' + str(int(y) + B) for A in vals for B in vals]
    return box_corners


def cells_with_x(cells, values, character):
    cells_x0, cells_x1, cells_x2, cells_x3, cells_x4 = [], [], [], [], []
    # dict_neighb=dict_neighb_val(values)
    # neighbours, em_neighb, nl_neighb, li_neighb, neighb_values = cell_neighb_val(cell, values)
    for cell in cells:
        count_x = 0
        for neighbour in cell_neighb_val(cell, values)[0]:
            if values[neighbour] == character:
                count_x += 1
        if count_x == 0:
            cells_x0.append(cell)
        elif count_x == 1:
            cells_x1.append(cell)
        elif count_x == 2:
            cells_x2.append(cell)
        elif count_x == 3:
            cells_x3.append(cell)
        elif count_x == 4:
            cells_x4.append(cell)
        else:
            print("error with cells_with_x")
    return cells_x0, cells_x1, cells_x2, cells_x3, cells_x4


def assign_character(values, cell, character, print_flag, loc):
    if values[cell] == em:
        values[cell] = character
        loc.append(str(cell + ':' + character))
        if print_flag == 'yes':
            print('Changed cell value: ' + cell + ' : ' + character)
    else:
        cell, character = "n", "n"
    return cell, character, loc


def check_loop(values, start_line):
    # for the start line we pick one of the 2 intersections defining this line
    start_intrsct = GRIDS_COORDS[start_line][0]
    aa, ab, ac, finished_grids, finished_lines = finished_cells(values)
    empties = len(GRIDS) - len(finished_grids)
    # this container will store all lines, lines that are part of the loop will be removed from it
    lines_container = finished_lines.copy()
    # this container will store all intersections that are part of the loop
    intrsc_used = []
    counter = len(lines_container) + 1
    result = ''

    if start_line in finished_lines:  # initial line must be line!
        lines_container.remove(start_line)
        intrsc_used.append(start_intrsct)

        while counter > 0:
            if start_line in lines_container:
                lines_container.remove(start_line)

            start_line_ends = [GRIDS_COORDS[start_line][0], GRIDS_COORDS[start_line][1]]
            for intrsc in sorted(start_line_ends, reverse=True):
                if intrsc in intrsc_used:
                    start_line_ends.remove(intrsc)

            if len(start_line_ends) == 0 and len(lines_container) > 0:
                result = 'loop_closed_error'
                break
            elif len(start_line_ends) == 0 and len(lines_container) == 0 and empties == 0:
                result = 'loop_closed_solved'
                break
            elif len(start_line_ends) == 1:
                start_intrsct = start_line_ends[0]
            else:
                # print(start_line_ends)
                # print(lines_container)
                # print(empties)
                result = 'loop_error_1'  # VERIFY THAT - it leads to false conclusions!!
                # print(result)

            intrsc_lines = cell_neighb_val(start_intrsct, values)[3]
            intrsc_lines.remove(start_line)

            if len(intrsc_lines) == 0:
                result = 'loop_open'
                if empties == 0:
                    result = 'loop_open_error'
                break
            elif len(intrsc_lines) == 1:
                intrsc_used.append(start_intrsct)
                start_line = intrsc_lines[0]
                # print('Start line: '+start_line)
            else:
                result = 'loop_error_2'
                # print(result)
            counter -= 1
    else:
        result = 'start_line_not_a_line'
    return result


# # ASSERTIONS

def assertions_loop(line, values):
    try:
        result = check_loop(values, line)
        assert result in ['loop_open', 'loop_closed_solved', 'loop_error_1']
        message = ''
    except AssertionError:
        message = ('FAILED Assertion for Loop check ' + line + ' // ' + result)
    return message


def run_assertions(values, cell):
    result = ''
    dict_neighb = dict_neighb_val(values)

    # wide_neighb = cell_wide_neighbours(cell,8)
    # wide_boxn=set(wide_neighb).intersection(set(unfinished_cells(values)[2]))
    # wide_intrsc=set(wide_neighb).intersection(set(unfinished_cells(values)[0]))
    # wide_box=set(wide_neighb).intersection(set(unfinished_cells(values)[1]))

    for boxn in BOXES_N:  # BOXES_N , wide_boxn
        # neighbours, em_neighb, nl_neighb, li_neighb, neighb_values = cell_neighb_val(cell, values)
        try:
            assert len(dict_neighb[boxn][3]) <= int(values[boxn])
            assert 4 - len(dict_neighb[boxn][2]) >= int(values[boxn])
            message = ''
        except AssertionError:
            message = ('FAILED Assertion for Boxn ' + boxn + ' digit value')
        if message:
            result = message
    if not result:
        for intersect in INTERSECTIONS:  # INTERSECTIONS , wide_intrsc
            try:
                assert len(dict_neighb[intersect][3]) <= 2
                assert not (len(dict_neighb[intersect][3]) == 1 and len(dict_neighb[intersect][2]) == 3)
                message = ''
            except AssertionError:
                message = ('FAILED Assertion for Intersection ' + intersect)
            if message:
                result = message
    if not result:
        for box in BOXES:  # BOXES , wide_box
            try:
                assert dict_neighb[box][4] in POSSIBLE_BOX
                message = ''
            except AssertionError:
                message = ('FAILED Assertion for Box ' + box + ' digit value')
            if message:
                result = message
    return result


# ### STRATEGIES ###

### INITIAL
def initial_numbers(values, print_flag, tt):
    BOXES_N0 = [box for box in BOXES_N if cells_dict[box] == '0']
    loc = []
    empties, t1_start = stats_start(values)
    # add empties around BOXES with 0
    print('\nBOXES with 0')
    for box in BOXES_N0:
        for nbr in cell_neighb_val(box, values)[0]:
            cell, character, loc = assign_character(values, nbr, nl, 'yes', loc)

    ### situation with two boxes with '3' that are neigbours
    BOXES_N3 = [box for box in BOXES_N if cells_dict[box] == '3']
    boxes_with_3 = BOXES_N3.copy()
    boxes_with_3_2 = BOXES_N3.copy()

    # neigbouring by cell (3 | 3)
    # this can be changed and merged with (3>3) - just find 3's with two common corners
    print('\nBOXES 3 | 3')
    for box in boxes_with_3:
        boxes_with_3_2.remove(box)
        frames1 = cell_neighb_val(box, values)[0]
        for box2 in boxes_with_3_2:
            frames2 = cell_neighb_val(box2, values)[0]
            frames_intersect = list(set(frames1).intersection(frames2))
            frames_sum = frames1 + frames2
            if len(frames_intersect) == 1:
                if frames_intersect[0] in GRIDS_VERTICAL:
                    for frame in list(set(frames_sum).intersection(GRIDS_VERTICAL)):
                        cell, character, loc = assign_character(values, frame, li, 'yes', loc)
                elif frames_intersect[0] in GRIDS_HORIZONTAL:
                    for frame in list(set(frames_sum).intersection(GRIDS_HORIZONTAL)):
                        cell, character, loc = assign_character(values, frame, li, 'yes', loc)
        boxes_with_3_2 = BOXES_N3.copy()

    # neigbouring by corner (3 > 3)
    print('\nBOXES 3 > 3')
    for box in boxes_with_3:
        boxes_with_3_2.remove(box)
        boxcorn = box_corners(box)
        for box2 in boxes_with_3_2:
            box2corn = box_corners(box2)
            common_corners = list(set(boxcorn).intersection(box2corn))
            if len(common_corners) == 1:
                all_frames = (cell_neighb_val(box, values)[0] + cell_neighb_val(box2, values)[0])
                inters_frames = cell_neighb_val(common_corners[0], values)[0]
                to_be_lines = list(set(all_frames) - set(inters_frames))  # those external frames will be lines
                for frame in to_be_lines:
                    cell, character, loc = assign_character(values, frame, li, 'yes', loc)
        boxes_with_3_2 = BOXES_N3.copy()
    empties_removed, time_elapsed, tt = stats_end(values, empties, t1_start, print_flag, tt)
    return values, loc, tt


### BASIC ###
# neighbours, em_neighb, nl_neighb, li_neighb, neighb_values = cell_neighb_val(cell, values)

def intersect_with_2_lines(values, print_flag, loc, tt):
    # if there are already 2 lines in intersection, the other two cells should be empty
    empties, t1_start = stats_start(values)
    intrsc_2li = cells_with_x(INTERSECTIONS, values, li)[2]
    range_list = list(set(intrsc_2li).intersection(set(unfinished_cells(values)[0])))

    for intrsc in range_list:
        for nbr in cell_neighb_val(intrsc, values)[1]:
            cell, character, loc = assign_character(values, nbr, nl, print_flag, loc)

    empties_removed, time_elapsed, tt = stats_end(values, empties, t1_start, print_flag, tt)
    return values, loc, tt


def compare_digit_w_lines(values, print_flag, loc, tt):
    # if there is box with 3 and neigbours are em, li, li, x - the em should be -> li
    empties, t1_start = stats_start(values)
    boxn_unfin = unfinished_cells(values)[2]
    for box in boxn_unfin:
        neighbours, em_neighb, nl_neighb, li_neighb, neighb_values = cell_neighb_val(box, values)
        digit = int(cells_dict[box])
        if len(li_neighb) + len(em_neighb) == digit:
            for neighb in em_neighb:
                cell, character, loc = assign_character(values, neighb, li, print_flag, loc)
        if len(li_neighb) == digit:
            for neighb in em_neighb:
                cell, character, loc = assign_character(values, neighb, nl, print_flag, loc)

    empties_removed, time_elapsed, tt = stats_end(values, empties, t1_start, print_flag, tt)
    return values, loc, tt


def box_3_in_corner(values, print_flag, rangeval, loc, tt):
    # box with digit '3' that touches with its corner an intersection with 2 'x' - lines must be added in this corner
    empties, t1_start = stats_start(values)
    boxn_unfin = unfinished_cells(values)[2]
    box3_unfin = list(set(BOXES_N3).intersection(set(boxn_unfin)))

    for box3 in box3_unfin:
        intrsc_2nl = cells_with_x(INTERSECTIONS, values, nl)[2]
        corn_2nl = list(set(box_corners(box3)).intersection(set(intrsc_2nl)).intersection(rangeval))

        for corner in corn_2nl:
            count_x = 0
            for corner_neighb in cell_neighb_val(corner, values)[0]:
                if (values[corner_neighb] == nl) and (corner_neighb not in cell_neighb_val(box3, values)[0]):
                    count_x += 1
            if count_x == 2:
                for corner_neighb in cell_neighb_val(corner, values)[0]:
                    cell, character, loc = assign_character(values, corner_neighb, li, print_flag, loc)

    empties_removed, time_elapsed, tt = stats_end(values, empties, t1_start, print_flag, tt)
    return values, loc, tt


def intersect_with_line_2nolines(values, print_flag, loc, tt):
    # intersection with 1 line and 2 no-lines - the 4th empty must be line
    empties, t1_start = stats_start(values)

    intrsc_2nl = cells_with_x(INTERSECTIONS, values, nl)[2]
    intrsc_1li = cells_with_x(INTERSECTIONS, values, li)[1]
    intrsc_unf = unfinished_cells(values)[0]
    inter_list = list(set(intrsc_2nl).intersection(set(intrsc_1li)).intersection(set(intrsc_unf)))
    for intersect in inter_list:
        for nbr in cell_neighb_val(intersect, values)[0]:
            cell, character, loc = assign_character(values, nbr, li, print_flag, loc)

    empties_removed, time_elapsed, tt = stats_end(values, empties, t1_start, print_flag, tt)
    return values, loc, tt


def intersect_with_3x(values, print_flag, loc, tt):
    # intersection with 3 nls - the 4th one must be nl as well
    empties, t1_start = stats_start(values)
    intrsc_3em = cells_with_x(INTERSECTIONS, values, nl)[3]
    for ints in intrsc_3em:
        for nbr in cell_neighb_val(ints, values)[0]:
            cell, character, loc = assign_character(values, nbr, nl, print_flag, loc)

    empties_removed, time_elapsed, tt = stats_end(values, empties, t1_start, print_flag, tt)
    return values, loc, tt


def run_basic_strategies(values, print_flag, rangeval, tt):
    floc = []
    loc = []
    values, loc, tt = intersect_with_2_lines(values, print_flag, loc, tt)
    floc = floc + list(set(loc) - set(floc))
    values, loc, tt = compare_digit_w_lines(values, print_flag, loc, tt)
    floc = floc + list(set(loc) - set(floc))
    values, loc, tt = box_3_in_corner(values, print_flag, rangeval, loc, tt)  # REMOVE rangeval from here, or fix it
    floc = floc + list(set(loc) - set(floc))
    values, loc, tt = intersect_with_line_2nolines(values, print_flag, loc, tt)
    floc = floc + list(set(loc) - set(floc))
    values, loc, tt = intersect_with_3x(values, print_flag, loc, tt)
    floc = floc + list(set(loc) - set(floc))
    return values, floc, tt


### ASSUMPTION 1
# check each empty; for each one test assign nl and li and check result;
# run basic strat. several times
# react on errors, if nl causes error - you must assign li, then.
def run_assumption_cell(values, cell, print_flag, tests_no):
    assumption_result = []
    for charact in [nl, li]:
        values_test = values.copy()
        values_test[cell] = charact
        for n in range(tests_no):  # run basic strategies N times
            values_test, loc1, tt1 = run_basic_strategies(values_test, print_flag, values_test, 99)
            # with this one, time is 6-10 times longer, it it solves only 10% more empties
            # values_test, loc1, tt1=run_assumptions3(values_test, print_flag, tt)
        result = run_assertions(values_test, cell)
        if len(result) > 1:
            assumption_result = [charact, cell, result]
        elif len(result) == 0:
            if cell in finished_cells(values_test)[4]:
                result = assertions_loop(cell, values_test)
                if len(result) > 1:
                    assumption_result = [charact, cell, result]
    return assumption_result, []


def run_assumptions(values, print_flag, tests_no):  # 50
    # empties, t1_start = stats_start(values)
    floc = []

    cells_count=unfinished_cells(values)[3]
    print("\nNumber of cells that will be analyzed: ", len(cells_count), '\n')
    dt, dt_start = datetime.now(), datetime.now()
    time_elapsed=0

    for grid in unfinished_cells(values)[3]:

        index = cells_count.index(grid)
        if index % 20 == 0:
            if index==0:
                print("batch_id".rjust(10), "time stamp".rjust(15), "batch time".rjust(15),
                      "Total".rjust(15), "ETA".rjust(15))
            time_elapsed = round((datetime.now() - dt_start).total_seconds(), 1)
            print(str(index).rjust(10),
                  datetime.now().strftime("%H:%M:%S").rjust(15),
                  str(round((datetime.now() - dt).total_seconds(),1)).rjust(15),
                  str(round(len(cells_count)/(index+0.0000001)*time_elapsed/60,1)).rjust(10)," min",
                  str(round((len(cells_count)-index)/(index+0.0000001)*time_elapsed/60,1)).rjust(10)," min")
            dt = datetime.now()


        assumption_result, loc = run_assumption_cell(values, grid, print_flag, tests_no)
        if len(assumption_result) > 0:
            loc = []
            print(assumption_result[2])
            print('   In cell ' + assumption_result[1] + " you can't add " + assumption_result[0])
            cell, character, loc = assign_character(values, assumption_result[1],
                                                    reversed_char[assumption_result[0]], 'yes', loc)
            for v in loc:
                if v not in floc:
                    floc.append(v)
        else:
            loc = []

    # empties_removed, time_elapsed, tt = stats_end(values, empties, t1_start, 'yes', tt)
    return values, floc


### ASSUMPTION 2
# find all unfinished boxes (or intrsc), for each em nieghbour assign nl or li, track 'list changes' for each assignemnt
# after all assignments - search for cells that always has been changed to the same value (like 4 times 'li' after 4 tests)
# this cell will be 'li' !

def run_assumptions2(values, print_flag, tt):  # 53
    empties, t1_start = stats_start(values)
    floc = []
    tt = tt

    # CONSIDER to add: for rangec in [unfinished_cells(values)[0],unfinished_cells(values)[1]]
    for box in unfinished_cells(values)[1]:
        changes_assumpt, changes_to_apply, count_test = [], [], 0
        for n in cell_neighb_val(box, values)[1]:
            for charact in [nl, li]:
                values_test = values.copy()
                values_test[n] = charact
                values_test, loc, tt = run_basic_strategies(values_test, print_flag, values_test, tt)
                result = run_assertions(values_test, n)
                if len(result) == 0:
                    for c in loc:
                        changes_assumpt.append(c)
                    count_test += 1
        for v in changes_assumpt:
            if changes_assumpt.count(v) == count_test:
                print("Change repeated " + str(count_test) + " times for cell " + v + ". It will be applied.")
                changes_assumpt.remove(v)
                changes_to_apply.append(v)
        for grid in changes_to_apply:
            loc = []
            cell, character, loc = assign_character(values, grid.split(":")[0],
                                                    grid.split(":")[1], 'yes', loc)
            for v in loc:
                if v not in floc:
                    floc.append(v)

    empties_removed, time_elapsed, tt = stats_end(values, empties, t1_start, 'yes', tt)
    return values, floc, tt


### ASSUMPTION 3 - LOOP
# Check if the loop is OK
def run_assumptions3(values, print_flag, tt):  # 54
    empties, t1_start = stats_start(values)
    floc = []

    for empt in unfinished_cells(values)[3]:
        values_test = values.copy()
        values_test[empt] = li
        result = assertions_loop(empt, values_test)
        if len(result) > 1:
            loc = []
            if print_flag == 'yes':
                print(result)
            cell, character, loc = assign_character(values, empt, nl, print_flag, loc)
            for v in loc:
                if v not in floc:
                    floc.append(v)
    empties_removed, time_elapsed, tt = stats_end(values, empties, t1_start, 'no', tt)
    return values, floc, tt


### ASSUMPTION with COMBOS

def fix_solved_boxes_combos(values, allowed_combos_dict):  # solved boxes migth still have multiple combos assigned
    for box in finished_cells(values)[1]:
        allowed_combos_dict[box] = cell_neighb_val(box, values)[4]
    return allowed_combos_dict


def reduce_combos(values, print_flag, range_c, allowed_combos_dict, tt, variant, repet):
    if variant == 60:
        print("Reduce combos by checking each box, if each combo fits the current values state")
        print("Example: with current values of box neigbours: [em,nl,em,li] this combo [em,nl,em,nl] will be reduced")
        print('Remove combos by running assumptions on test values - react on failed assertions\n')
    elif variant == 63:
        print('Remove combos by testing each combo for two neighbouring boxes')

    empties, t1_start = stats_start(values)
    combos_len_start = combos_len(values, allowed_combos_dict)

    range_list = list(set(range_c).intersection(set(unfinished_cells(values)[1])))
    print("\nNumber of boxes that will be analyzed: ", len(range_list), '\n')
    dt = datetime.now()
    dt_start = datetime.now()
    time_elapsed=0

    for box in range_list:

        index = range_list.index(box)
        if index % 10 == 0:
            if index==0:
                print("batch_id".rjust(10), "time stamp".rjust(15), "batch time".rjust(15),
                      "Total".rjust(15), "ETA".rjust(15))
            time_elapsed = round((datetime.now() - dt_start).total_seconds(), 1)
            print(str(index).rjust(10),
                  datetime.now().strftime("%H:%M:%S").rjust(15),
                  str(round((datetime.now() - dt).total_seconds(),1)).rjust(15),
                  str(round(len(range_list)/(index+0.0000001)*time_elapsed/60,1)).rjust(10)," min",
                  str(round((len(range_list)-index)/(index+0.0000001)*time_elapsed/60,1)).rjust(10)," min")
            dt = datetime.now()

        neigh = cell_neighb_val(box, values)[0]
        allowed_combos = allowed_combos_dict[box].copy()
        for combo in sorted(allowed_combos, reverse=True):
            status, result = '', ''
            values_test = values.copy()
            for i in range(4):
                if not (values_test[neigh[i]] == combo[i] or values_test[neigh[i]] == em):
                    status = 'err'
                cell, character, loc = assign_character(values_test, neigh[i], combo[i], print_flag, [])
            if status == 'err':
                allowed_combos.remove(combo)
            else:
                values_test, loc, tt1 = run_basic_strategies(values_test, 'no', values_test, tt)

                if variant == 60:
                    for n in range(int(repet)):  # run basic strategies N times
                        values_test, loc, tt1 = run_assumptions3(values_test, 'no', tt)
                        values_test, loc, tt1 = run_basic_strategies(values_test, 'no', values_test, tt)
                    result = run_assertions(values_test, box)
                    if combo in allowed_combos and len(result) > 1:
                        allowed_combos.remove(combo)

                elif variant == 63:
                    box_neighb = box_wide_neighbours(box, 1)
                    box_neighb_unslvd = list(set(box_neighb).intersection(set(unfinished_cells(values_test)[1])))
                    for box2 in box_neighb_unslvd:
                        allowed_combos_2 = allowed_combos_dict[box2].copy()
                        neigh2, a, b, c, neigh2_val = cell_neighb_val(box2, values_test)
                        for combo2 in sorted(allowed_combos_2, reverse=True):
                            status2, result2 = '', ''
                            values_test2 = values_test.copy()
                            for j in range(4):  # checking if combo fits the cell (generally)
                                if not (neigh2_val[j] == combo2[j] or neigh2_val[j] == em):
                                    status2 = 'err'
                                cell, character, loc = assign_character(values_test2, neigh2[j], combo2[j], print_flag,
                                                                        [])
                            if status2 == 'err':
                                allowed_combos_2.remove(combo2)
                            else:
                                result2 = run_assertions(values_test2, box2)  # OPTIMIZE ME!!!
                                if combo2 in allowed_combos_2 and len(result2) != 0:
                                    # checking if combo doesn't result in errors with assertions
                                    allowed_combos_2.remove(combo2)
                                else:
                                    continue
                        if not allowed_combos_2 and combo in allowed_combos:
                            allowed_combos.remove(combo)
                        else:
                            continue

        if not allowed_combos:
            print("ERROR ALARM EMPTY allowed combos")
        allowed_combos_dict[box] = allowed_combos

    # fix_solved_boxes_combos(values,allowed_combos_dict)
    combos_removed = combos_len_start - combos_len(values, allowed_combos_dict)
    print('COMBOS REMOVED:', str(combos_len_start - combos_len(values, allowed_combos_dict)))
    print('Now run tests to find a cell that gets only one value in all allowed combos\n')
    values, floc, tt = reduce_combos_assign(values, 'yes', unfinished_cells(values)[1], allowed_combos_dict, tt)
    print("List of changes applied: ", sorted(floc))
    empties_removed, time_elapsed, tt = stats_end(values, empties, t1_start, 'yes', tt)
    return values, allowed_combos_dict, tt, floc, combos_removed


def run_assumptions4(values, print_flag, range_c, allowed_combos_dict, tt, repet):  # no.55
    # find all unfinished boxes (or intrsc), test each possible combo, track 'list changes' for each assignemnt
    # after all assignments - search for cells that always have been changed to the same value (like 4 times 'li' after 4 tests)
    # this cell will be 'li' !
    empties, t1_start = stats_start(values)
    range_list = list(set(range_c).intersection(set(unfinished_cells(values)[1])))
    floc = []
    tt = tt

    for box in range_list:
        if box in allowed_combos_dict:
            changes_assumpt, changes_to_apply, count_test = [], [], 0
            neigh = cell_neighb_val(box, values)[0]
            allowed_combos = allowed_combos_dict[box]
            for combo in sorted(allowed_combos, reverse=True):
                values_test = values.copy()
                for i in range(4):
                    cell, character, loc = assign_character(values_test, neigh[i], combo[i], 'no', [])
                for n in range(int(repet)):  # run basic strategies N times
                    values_test, loc, tt = run_basic_strategies(values_test, 'no', values_test, tt)
                result = run_assertions(values_test, box)
                if len(result) == 0:
                    for c in loc:
                        changes_assumpt.append(c)
                    count_test += 1
        for v in changes_assumpt:
            if changes_assumpt.count(v) == count_test:
                print("Change repeated " + str(count_test) + " times for cell " + v + ". It will be applied.")
                changes_assumpt.remove(v)
                changes_to_apply.append(v)
        for grid in changes_to_apply:
            loc = []
            cell, charc, loc = assign_character(values, grid.split(":")[0], grid.split(":")[1], 'yes', loc)
            for v in loc:
                if v not in floc:
                    floc.append(v)

    empties_removed, time_elapsed, tt = stats_end(values, empties, t1_start, 'yes', tt)
    return values, floc, tt


def reduce_combos_assign(values, print_flag, range_c, allowed_combos_dict, tt):  # 64
    # it can happen that in all allowed combos there is a cell that gets only one value, then we have a match!
    empties, t1_start = stats_start(values)
    floc = []
    range_list = list(set(range_c).intersection(set(unfinished_cells(values)[1])))

    for box in range_list:
        if box in allowed_combos_dict:
            neigh = cell_neighb_val(box, values)[0]
            allowed_combos = allowed_combos_dict[box]
            for i in range(4):
                list_char = [allowed_combos[j][i] for j in range(len(allowed_combos))]
                if list_char.count(list_char[0]) == len(list_char) and values[neigh[i]] == em:
                    loc = []
                    print('The only possible value in all allowed combos for box', box, 'cell', neigh[i], list_char[0],
                          '(', i, ')')
                    cell, character, loc = assign_character(values, neigh[i], list_char[0], 'yes', loc)
                    for v in loc:
                        if v not in floc:
                            floc.append(v)

    empties_removed, time_elapsed, tt = stats_end(values, empties, t1_start, 'yes', tt)
    return values, floc, tt


def reduce_combos_set3boxes(values, print_flag, range_c, allowed_combos_dict, tt):  # 65
    empties, t1_start = stats_start(values)
    floc = []
    set_of3_boxes = list_set_of3_boxes(values)
    print("\nNumber of 3-boxes variations that will be analyzed: ", len(set_of3_boxes), '\n')
    combos_len_start = combos_len(values, allowed_combos_dict)
    # set_of3_boxes=[['8.2', '6.4', '4.6']]
    dt = datetime.now()

    for set3 in set_of3_boxes:

        index = set_of3_boxes.index(set3)
        if index % 20 == 0:
            print(index, datetime.now(), datetime.now() - dt)
            dt = datetime.now()

        combos0, combos1, combos2 = [], [], []
        combi_combos = [[set3[0], set3[1], set3[2], A, B, C] for A in allowed_combos_dict[set3[0]]
                        for B in allowed_combos_dict[set3[1]] for C in allowed_combos_dict[set3[2]]]
        print(len(combi_combos))
        for combi in combi_combos:
            values_test = values.copy()
            status, result = '', ''

            # box0
            neigh0 = cell_neighb_val(combi[0], values_test)[0]
            neigh0_val = cell_neighb_val(combi[0], values_test)[4]
            for i in range(4):
                if not (neigh0_val[i] == combi[3][i] or neigh0_val[i] == em):
                    status = 'err'
                cell, character, loc = assign_character(values_test, neigh0[i], combi[3][i], 'no', [])
            if status == 'err':
                continue
            else:
                values_test, loc, tt = run_basic_strategies(values_test, 'no', values_test, tt)
                result = run_assertions(values_test, combi[0])
                if len(result) > 1:
                    continue
                else:
                    if combi[3] not in combos0:
                        combos0.append(combi[3])

            # box1
            if status == 'err' or len(result) > 1:
                continue
            else:
                neigh1 = cell_neighb_val(combi[1], values_test)[0]
                neigh1_val = cell_neighb_val(combi[1], values_test)[4]
                for i in range(4):
                    if not (neigh1_val[i] == combi[4][i] or neigh1_val[i] == em):
                        status = 'err'
                    cell, character, loc = assign_character(values_test, neigh1[i], combi[4][i], 'no', [])
                if status == 'err':
                    continue
                else:
                    values_test, loc, tt = run_basic_strategies(values_test, 'no', values_test, tt)
                    result = run_assertions(values_test, combi[1])
                    if len(result) > 1:
                        continue
                    else:
                        if combi[4] not in combos1:
                            combos1.append(combi[4])

            # box2
            if status == 'err' or len(result) > 1:
                continue
            else:
                neigh2 = cell_neighb_val(combi[2], values_test)[0]
                neigh2_val = cell_neighb_val(combi[2], values_test)[4]
                for i in range(4):
                    if not (neigh2_val[i] == combi[5][i] or neigh2_val[i] == em):
                        status = 'err'
                    cell, character, loc = assign_character(values_test, neigh2[i], combi[5][i], 'no', [])
                if status == 'err':
                    continue
                else:
                    values_test, loc, tt = run_basic_strategies(values_test, 'no', values_test, tt)
                    result = run_assertions(values_test, combi[2])
                    if len(result) > 1:
                        continue
                    else:
                        if combi[5] not in combos2:
                            combos2.append(combi[5])

        allowed_combos_dict[set3[0]] = combos0
        allowed_combos_dict[set3[1]] = combos1
        allowed_combos_dict[set3[2]] = combos2

    combos_removed = combos_len_start - combos_len(values, allowed_combos_dict)
    print('COMBOS REMOVED:', str(combos_len_start - combos_len(values, allowed_combos_dict)))
    empties_removed, time_elapsed, tt = stats_end(values, empties, t1_start, 'yes', tt)
    return values, allowed_combos_dict, floc, tt, combos_removed


def solve_ambiguous():
    print()
    # for each unfinished grid assign li/nl
    # for each unfinished cell box check all combos
    # run basic tests
    # check loop
    # if check loop for every combo returns error - then exclude value from point 1


# ### MAIN
# @profile
def main(values, allowed_combos_dict):
    tt = 0
    allowed_combos_dict = {}
    values = cells_dict
    #values = examples.ex870

    # values['8.1'] = nl
    # values['9.2'] = nl

    for box in unfinished_cells(values)[1]:
        allowed_combos_dict[box] = POSSIBLE_BOX_F.copy()

    #allowed_combos_dict = examples.exa870_acd

    choice = None
    while choice != "0":
        print('\n=================================')
        choice = input("Your choice - enter 1 for menu: ")  # What To Do ???
        if choice == "0":
            print("Good bye!\n")
        elif choice == "1":
            print("""
            ---MENU---
            0  - Exit
            1  - Print initial grid
            2  - Display current state
            3  - Run Initial checks              E-2, T-1
            4  - Run basic tests                 E-4, T-1
            50 - Assumptions 1 (X assumptions)   E-8, T-4 (with 2 assmpt)
            53 - Assumptions 2                   E-8, T-2
            54 - Check false loops               E-1, T-1
            55 - Assumptions 4 (with combos)     E-4, T-9
            60 - Reduce Combos 1                 E-3, T-3 (with 1 assmpt)
            63 - Reduce Combos 3                 E-_, T-_
            64 - Clean reduced combos            E-_, T-_
            65 - Reduce combos (3 boxes sets)    E-_, T-_
            8  - Check if solved
            9  - History
            91  - Print Values
            """)
        elif choice == "2":
            display(values)
            stats(values, allowed_combos_dict, tt)
        elif choice == "3":
            t_ini = tt
            values, floc, tt = initial_numbers(values, 'yes', tt)
            print('Changed cells: ', floc)
            add_to_history(history, choice, len(floc), '?', 0, '?', tt - t_ini, tt)
            # history, choice, loc, empties, cmb, combos, elapsed, tt
        elif choice == "4":
            t_ini = tt
            floc = []
            values, loc, tt = run_basic_strategies(values, 'yes', values, tt)
            floc = floc + list(set(loc) - set(floc))
            print('\nCahnges applied in a single round: ', loc)
            while len(loc) > 0:
                # values,loc,tt=run_assumptions3(values, 'no',tt)
                print('Changed cells in total: ' + str(len(loc)))
                print(sorted(loc))
                values, loc, tt = run_basic_strategies(values, 'yes', values, tt)
                floc = floc + list(set(loc) - set(floc))
                print('\nChanges applied in a single round: ', loc)
            print('Changed cells in total: ' + str(len(loc)))
            print('\nFinal list of applied changes: ', str(len(floc)))
            print(sorted(floc))
            add_to_history(history, choice, len(floc), '?', 0, '?', tt - t_ini, tt)
        elif choice == "50":
            # t_ini = tt
            repet = input("How many repetitions? : ")
            empties, time1, cmb_len, unf_grids = stats_start_new(values, allowed_combos_dict)
            values, floc = run_assumptions(values, 'no', int(repet))
            print('\nChanged cells in total: ' + str(len(floc)))
            print(sorted(floc))
            empts_rmvd, empties, time_2_1, tt, combos_rmvd, combos, loc = stats_end_new(values, allowed_combos_dict,
                                                                                        empties, time1, cmb_len,
                                                                                        unf_grids, tt)
            add_to_history(history, str(choice) + '-' + str(repet), empts_rmvd, empties, combos_rmvd, combos,
                           time_2_1, tt)
        elif choice == "53":
            t_ini = tt
            values, loc, tt = run_assumptions2(values, 'no', tt)
            print('Changed cells in total: ' + str(len(loc)))
            print(sorted(loc))
            add_to_history(history, choice, len(loc), '?', 0, '?', tt - t_ini, tt)
        elif choice == "54":
            t_ini = tt
            values, loc, tt = run_assumptions3(values, 'yes', tt)
            print('Changed cells in total: ' + str(len(loc)))
            print(sorted(loc))
            add_to_history(history, choice, len(loc), '?', 0, '?', tt - t_ini, tt)
        elif choice == "55":
            t_ini = tt
            repet = input("How many repetitions? : ")
            values, loc, tt = run_assumptions4(values, 'no', unfinished_cells(values)[1], allowed_combos_dict, tt,
                                               repet)
            print('Changed cells in total: ' + str(len(loc)))
            print(sorted(loc))
            add_to_history(history, choice, len(loc), '?', 0, '?', tt - t_ini, tt)
        elif choice == "60":
            t_ini = tt
            loc = []
            repet = input("How many repetitions? : ")
            empties, time1, cmb_len, unf_grids = stats_start_new(values, allowed_combos_dict)
            values, allowed_combos_dict, tt, floc, cmb_rmv = reduce_combos(values, 'no', unfinished_cells(values)[1],
                                                                           allowed_combos_dict, tt, 60, repet)
            empts_rmvd, empties, time_2_1, tt, combos_rmvd, combos, loc = stats_end_new(values, allowed_combos_dict,
                                                                                        empties, time1, cmb_len,
                                                                                        unf_grids, tt)
            add_to_history(history, str(choice) + '-' + str(repet), empts_rmvd, empties, combos_rmvd, combos, tt - t_ini, tt)
        elif choice == "63":
            t_ini = tt
            loc = []
            values, allowed_combos_dict, tt, floc, cmb_rmv = reduce_combos(values, 'no', unfinished_cells(values)[1],
                                                                           allowed_combos_dict, tt, 63, 0)
            add_to_history(history, choice, len(floc), '?', 0, '?', tt - t_ini, tt)
        elif choice == "64":
            t_ini = tt
            values, floc, tt = reduce_combos_assign(values, 'yes', unfinished_cells(values)[1], allowed_combos_dict, tt)
            add_to_history(history, choice, len(floc), '?', 0, '?', tt - t_ini, tt)
        elif choice == "65":
            t_ini = tt
            loc = []
            values, allowed_combos_dict, floc, tt, cmb_rmv = reduce_combos_set3boxes(values, 'no', values,
                                                                                     allowed_combos_dict, tt)
            add_to_history(history, choice, len(floc), '?', 0, '?', tt - t_ini, tt)
        elif choice == "8":
            result = check_loop(values, finished_cells(values)[4][1])
            if result == 'loop_closed_solved':
                print(result, '   |||   GOOD JOB, MAN!\n')
            else:
                print('No yet solved. Keep working on it!')
        elif choice == "9":
            print_history(history)
        elif choice == "91":
            print(values,'\n\n\n',allowed_combos_dict)
        else:
            print(" ### Wrong option ### ")
    return values, allowed_combos_dict


### MAIN
values, allowed_combos_dict = {}, {}
values, allowed_combos_dict = main(values, allowed_combos_dict)
