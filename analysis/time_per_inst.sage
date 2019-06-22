#!/usr/bin/env sage

"""time_per_inst.sage

Script that outputs rows for a LaTeX table that shows how fast functions of
distinct time complexities grow.
"""

from scipy.special import lambertw as w

# number of seconds in a second, minute, ..., century
seconds = [
    1,
    1 * 60,
    1 * 60 * 60,
    1 * 60 * 60 * 24,
    1 * 60 * 60 * 24 * 30,
    1 * 60 * 60 * 24 * 30 * 12,
    1 * 60 * 60 * 24 * 30 * 12 * 100,
]
inst = 10 ** 10


def print_numeric_table_line(header, function):
    print "${:>8s}$".format(header),
    for period in seconds:
        value = function(period * inst)
        fmt = "& $2^{\\num{%s}}$" if type(value) == str else "& $\\num{%.2E}$"
        # old string formatting used due to multitude of sage types
        print fmt % value,
    print "\\\\"


def print_generic_table_line(header, function):
    print "${:>8s}$".format(header),
    for var in range(1, len(seconds) + 1):
        print "& ${:>25s}$".format(function(var)),
    print "\\\\"


def inv_gamma(nn):
    spi = sqrt(2 * pi)
    psi_zero = find_root(psi(x), 0, 10)
    c = spi / e - gamma(psi_zero)
    l = log((nn + c) / spi) - 1
    return round(real_part(l / (w((l / e).n())) + 1 / 2)) - 1


str_functions = [
    "\\lg n",
    "\\sqrt{n}",
    "n",
    "n \\lg n",
    "n^{2}",
    "n^{3}",
    "2^{n}",
    "n!",
]

inv_functions = [
    lambda x: "{:.2E}".format(x),  # hack for overflow
    lambda x: x ** 2,
    lambda x: x,
    lambda x: e ** w(x * log(2).n()),
    lambda x: x ** (1 / 2),
    lambda x: x ** (1 / 3),
    lambda x: log(x, 2),
    inv_gamma,
]

gen_functions = [
    lambda x: "2^{t_{%d} s}" % x,
    lambda x: "(t_{%d} s)^{2}" % x,
    lambda x: "t_{%d} s" % x,
    lambda x: "\\euler^{W(t_{%d} s \\ln 2)}" % x,
    lambda x: "\\sqrt{t_{%d} s}" % x,
    lambda x: "\\sqrt[3]{t_{%d} s}" % x,
    lambda x: "\\lg t_{%d} s" % x,
    lambda x: "\\iota(t_{%d} s)" % x,
]

for h, f in zip(str_functions, inv_functions):
    print_numeric_table_line(h, f)

for h, f in zip(str_functions, gen_functions):
    print_generic_table_line(h, f)
