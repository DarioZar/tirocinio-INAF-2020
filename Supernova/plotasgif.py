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
'lines.linewidth': 1.5
}
plt.rcParams.update(params)

def parsearguments():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Plot gif from Pluto simulation data")
    parser.add_argument("path", help="Simulation path")
    parser.add_argument("var", help="Variable to plot",
                        choices=["rho","prs","tr1","tr2"])
    parser.add_argument("steps", help="Steps to plot",
                        type=int)
    parser.add_argument("--log", help="Plot log(var)",
                        action="store_true")
    parser.add_argument("--cmap", help="Choose colormap",
                        choices=sorted(cm.cmap_d), default="jet")
    parser.add_argument("--fixscale", help="Fix the scale",
                        action="store_true")
    args = parser.parse_args()
    return args

def plotimage(D, var, vmin, vmax, cmap, log=False):
    if log:
        vals = np.log10(getattr(D, var)).T
        vmin = np.log10(vmin)
        vmax = np.log10(vmax)
    else:
        vals = getattr(D, var).T
    fig, ax = plt.subplots()
    ax.set_title(labels[var])
    ax.set_xlabel('r (Parsec)')
    ax.set_ylabel('z (Parsec)')
    ax.set_xlim([min(D.x1), max(D.x1)])
    ax.set_ylim([min(D.x2), max(D.x2)])
    image = ax.pcolormesh(D.x1,D.x2,vals,cmap=cmap,vmin=vmin,vmax=vmax)
    fig.colorbar(image)
    return fig

# Get range of var for all the timesteps
def getfixrange(data, var):
    minvar = []
    maxvar = []
    for D in data:
        minvar.append(np.min(getattr(D, var)))
        maxvar.append(np.max(getattr(D, var)))
    return np.min(minvar), np.max(maxvar)

# Parse arguments using the defined function
args = parsearguments()
path = args.path
var = args.var
steps = args.steps
log = args.log
cmap = args.cmap
fixscale = args.fixscale

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
## Change dir
os.chdir(path)
## Prepare plot labels
labels = {'rho': u"Densità",
          'prs': "Pressione",
          'tr1': "Tracciante 1 (SNR)",
          'tr2': "Tracciante 2 (Ring)"}
if log:
    labels[var] += " (log)"
labels[var] += (" " + path) 
## Prepare scale if fixed
if fixscale:
    vmin, vmax = getfixrange(data, var)

## Plot data and save in .png
for D,n in zip(data, range(maxstep+1)):
    if not fixscale:
        vmin = np.min(getattr(data[n], var))
        vmax = np.max(getattr(data[n], var))
    
    fig = plotimage(D, var, vmin, vmax, cmap, log)
    fig.savefig("{}_{:04d}.png".format(var,n))
    fig.clf()

# Create gif using generated .png
os.system("convert -delay 30 {}_*.png {}_log{}_fix{}.gif".format(var,var,log,fixscale))
os.system("rm {}_*.png".format(var))
