import pyPLUTO as pp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator,
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
## Choose mode and tracer
if sys.argv[1] not in ["conv", "solv"]:
    raise ValueError("Plot arg must be\n \
                     'conv' for convergence test\n \
                     'solv' for solver test")
else:
    modekey = sys.argv[1]
if sys.argv[2] not in ["1","2"]:
    raise ValueError("Tracer arg must be 1 or 2")
else:
    tracer = "tr"+sys.argv[2]
## Setup units
UNIT_LENGTH = 3.0856776e18
UNIT_DENSITY = 1.6726219e-24
M_SUN = 1.98855e33
## Load data
modedict= {
    'conv':{'files' :["./128/roe/", "./256/roe/", "./512/roe/", "./1024/roe/"],
            'labels':["128x128", "256x256", "512x512", "1024x1024"],
            'lim'   :{"tr1":[0.60,1.02], "tr2":[0.92,1.02]}},
    'solv':{'files' :["./512/hll/", "./512/hllc/", "./512/roe/"],
            'labels':["hll", "hllc", "roe"],
            'lim'   :{"tr1":[0.80,1.025], "tr2":[0.97,1.01]}}
}

mode = modedict[modekey]
data = {}
mass = {}
for val,path in zip(mode['labels'], mode['files']):
    data.update({val:[]})
    mass.update({val:[]})
    for n in range(0, 11):
        data[val].append(pp.pload(n, w_dir=path))
    ## Calc volume
    vol = np.zeros([data[val][0].n1, data[val][0].n2])
    for i in range(data[val][0].n2):
        vol[:,i] = data[val][0].dx1*data[val][0].dx2*2*np.pi*data[val][0].x1
    ## Calc mass for tr1>0.9, with units and symmetry
    for d in data[val]:
        idx = (getattr(d, tracer) < 0.9)
        d.rho[idx] = 0
        mass[val].append(2*np.sum(vol*getattr(d, tracer)*d.rho)*
                         UNIT_DENSITY*
                         UNIT_LENGTH**3
                         /M_SUN)

# Plot data
## Setup fig, axes, labels
fig, ax = plt.subplots()
styleaxes(ax)
ax.set_xlabel(r'Step temporale')
ax.set_ylabel(r'Massa normalizzata con M(0)')
ax.set_ylim(mode['lim'][tracer])
ax.set_xlim([0,10])
ax.xaxis.set_major_locator(MultipleLocator(1))

## Plot mass for 128x128, 256x256, 512x512 and 1024x1024
## Normalized
for val in mode['labels']:
    ax.plot(mass[val]/mass[val][0], label=val)

ax.legend(fancybox=True, loc=0,
          title='Massa di elementi con tracciante {} > 90% \n normalizzata a M(0)'.format(tracer),
          framealpha=1)

# Show and save plot
plt.tight_layout()
fig.savefig("{}-test-{}.pdf".format(modekey, tracer), 
            bbox_inches="tight")
plt.show()
