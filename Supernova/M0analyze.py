import pyPLUTO as pp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, 
                               ScalarFormatter)
import sys

# Styleaxes function
def styleaxes(*axs):
    for ax in axs:
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_axisbelow(True)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.grid(axis='y', color='0.9', linestyle='--', linewidth=0.6)
        ax.grid(axis='x', color='0.9', linestyle='--', linewidth=0.6)
        #ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.xaxis.set_major_formatter(ScalarFormatter(useOffset=False, useMathText=True))
        ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False, useMathText=True))


# Plot style settings
plt.style.use('seaborn-deep')
params = {
'axes.labelsize': 12,
'font.size': 12,
'legend.fontsize': 10,
'xtick.labelsize': 10,
'ytick.labelsize': 10,
'figure.figsize': [8, 6],
'font.family': 'serif',
'lines.linewidth': 1.5,
}
plt.rcParams.update(params)


# Data analysis
## Setup units
UNIT_LENGTH = 3.0856776e18
UNIT_DENSITY = 1.6726219e-24
M_SUN = 1.98855e33
## Load data
dim = [128, 256, 512, 1024]
data = {}
mass = {"tr1":{}, "tr2":{}}
for val in dim:
    data.update({val:[]})
    mass["tr1"].update({val:[]})
    mass["tr2"].update({val:[]})
    data[val] = pp.pload(0, w_dir="./{}/roe/".format(val))
    ## Calc volume
    vol = np.zeros([data[val].n1, data[val].n2])
    for i in range(data[val].n2):
        vol[:,i] = data[val].dx1*data[val].dx2*2*np.pi*data[val].x1
    ## Calc mass for tr and tr<90, with units and symmetry
    for tracer in ["tr1", "tr2"]:
        idx = (getattr(data[val], tracer) < 0.9)
        rho = np.copy(data[val].rho)
        rho[idx] = 0
        mass[tracer][val] = (2*np.sum(vol*getattr(data[val], tracer)*rho)*
                             UNIT_DENSITY*
                             UNIT_LENGTH**3
                             /M_SUN)

# Plot data
## Setup fig, axes, labels
fig, ax = plt.subplots()
styleaxes(ax)
ax.set_xlabel(r'Dimensione griglia')
ax.set_ylabel(r'Massa normalizzata con massa condizioni iniziali')
ax.set_ylim([0.9975, 1.02])
ax.set_xlim([-1,4])
plt.xticks([0,1,2,3],
           ["128x128", "256x256", "512x512", "1024x1024"])

initMass = {"tr1":10,
            "tr2":2*np.pi*np.pi*0.5*0.5*2.5*1.e2
            *UNIT_DENSITY
            *UNIT_LENGTH**3
            /M_SUN}

for tracer in ["tr1", "tr2"]:
    # Plot mass with tracer
    print(np.array(mass[tracer].values())/initMass[tracer])
    ax.plot(np.array(mass[tracer].values())/initMass[tracer],
            label="Massa di elementi con tracciante {} > 90%".format(tracer))

# Plot initial mass
ax.axhline(y=1, color="C4",
           label="Massa condizioni iniziali ")
ax.legend(fancybox=True, loc=0, framealpha=1)

# Show and save plot
plt.tight_layout()
fig.savefig("andamentoM0.pdf", 
            bbox_inches="tight")
plt.show()