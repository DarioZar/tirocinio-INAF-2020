# -*- coding: utf-8 -*-
import pyPLUTO as pp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import os
import argparse

# Plot style settings
plt.style.use('seaborn-deep')
params = {
'axes.labelsize': 12,
'font.size': 12,
'legend.fontsize': 10,
'xtick.labelsize': 10,
'ytick.labelsize': 10,
'figure.figsize': [8, 8],
'font.family': 'serif',
'lines.linewidth': 1.5,
}
plt.rcParams.update(params)

# Parse arguments
parser = argparse.ArgumentParser(description="Plot gif from Pluto simulation data")
parser.add_argument("path", help="Simulation path")
parser.add_argument("var", help="Variable to plot",
                    choices=["rho","prs","tr1","tr2"])
parser.add_argument("steps", help="Steps to plot", type=int)
parser.add_argument("--log", help="Plot log(var)",
                    action="store_true")
parser.add_argument("--cmap", help="Choose colormap",
                    choices=sorted(cm.cmap_d), default="jet")
args = parser.parse_args()


path = args.path
var = args.var
steps = args.steps
log = args.log
cmap = args.cmap

# Get data
data = []

maxstep = -1
for n in range(int(steps)+1):
    try:
        data.append(pp.pload(n, w_dir=path))
        maxstep = n
    except IOError:
        if maxstep==-1:
            raise IOError("Path does not contain any data.000x.dbl")
        else:
            print("{} is too high".format(steps))
            print("Plotting gif to step {}".format(maxstep))
            break

# Plotting
os.chdir(path)
labels = {'rho': u"Densità",
          'prs': "Pressione",
          'tr1': "Tracciante 1 (SNR)",
          'tr2': "Tracciante 2 (Ring)"}
if log:
    labels[var] += " (log)"
labels[var] += (" " + path)

plt.set_cmap(cmap)
for D,n in zip(data, range(maxstep+1)):
    if log:
        vals = np.log(getattr(D, var))
    else:
        vals = getattr(D, var)
    
    I = pp.Image()
    I.pldisplay(D, vals, x1=D.x1, x2=D.x2,
                title=labels[var], label1 = "r", label2="z",
                cbar=(True, "vertical"))
    plt.savefig("{}_{:04d}.png".format(var,n))
    plt.clf()

# Creating gif
os.system("convert -delay 30 {}_*.png {}.gif".format(var,var))
os.system("rm {}_*.png".format(var))
