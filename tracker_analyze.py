import pyPLUTO as pp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator,
                               ScalarFormatter)

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
dim = ["128", "256", "512", "1024"]
data = {}
mass = {}
for val in dim:
    data.update({val:[]})
    mass.update({val:[]})
    for n in range(0, 11):
        data[val].append(pp.pload(n, w_dir="./{}/".format(val)))
    ## Calc volume
    vol = np.zeros([data[val][0].n1, data[val][0].n2])
    vol[:,] = data[val][0].dx1*data[val][0].dx2*2*np.pi*data[val][0].x1
    ## Calc mass for tr1<0.9
    for d in data[val]:
        idx = (d.tr1 < 0.9)
        d.rho[idx] = 0
        mass[val].append(np.sum(vol*d.tr1*d.rho)*
                    UNIT_DENSITY*
                    UNIT_LENGTH**3
                    /M_SUN)

# Plot data
## Setup fig, axes, labels
fig, ax = plt.subplots()
styleaxes(ax)
ax.set_xlabel(r'Step temporale')
ax.set_ylabel(r'Massa ($M_{sun}$)')
ax.set_ylim([3,5.4])
ax.set_xlim([0,10])
ax.xaxis.set_major_locator(MultipleLocator(1))

## Plot mass for 128x128, 256x256, 512x512 and 1024x1024
for val in dim:
    ax.plot(mass[val], label="{}x{}".format(val, val))

## Add line at 5 M_SUN and add legend
ax.axhline(y=5)
ax.legend(fancybox=True, loc=0,
          title=r'Massa di elementi con tracciante < 90%',
          framealpha=1)

# Show and save plot
plt.tight_layout()
fig.savefig("andamentoMassa.pdf", bbox_inches="tight")
plt.show()
