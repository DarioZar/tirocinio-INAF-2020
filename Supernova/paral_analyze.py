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
'figure.figsize': [5, 5],
'font.family': 'serif',
'lines.linewidth': 1.5,
}
plt.rcParams.update(params)

# Data analysis
cores = [1,2,4]
filepaths = ["./ParalTest/{}-Core/pluto.0.log".format(core) for core in cores]
parTime = []
speedup = []
for path in filepaths:
    # Read log
    with open(path, "r") as f:
        s = f.readlines()
    # Get string with Time
    sub = [a for a in s if "Elapsed time" in a][0]
    # Create timedelta and parse string
    timeval = np.timedelta64()
    timestr = sub.split()[-1].replace("d", "D")
    for val in timestr.split(":"):
        timeval += np.timedelta64(val[:-1], val[-1])
    # Add parallel time to list
    parTime.append(timeval)
# Calc speedup
speedup = parTime[0]/parTime
print(speedup)

# Plot data
## Setup fig, axes, labels
fig, ax = plt.subplots()
styleaxes(ax)
ax.set_xlabel(r'N processori')
ax.set_ylabel(r'Speedup parallelo')
ax.set_ylim([1, 5])
ax.set_xlim([1,5])
ax.xaxis.set_major_locator(MultipleLocator(1))

x = np.linspace(1,5)
ax.plot(x, x, label="Speedup ideale")
ax.plot(cores, speedup, label=r"Speedup misurato $S=\frac{T_1}{T_p}$")
ax.legend(fancybox=True, loc=0, framealpha=1)

# Show and save plot
plt.tight_layout()
fig.savefig("paralSpeedup.pdf", 
            bbox_inches="tight")
plt.show()
