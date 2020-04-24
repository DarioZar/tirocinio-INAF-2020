import pyPLUTO as pp
import matplotlib.pyplot as plt
import sys
import os

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

# Choose path
path = sys.argv[1]
# Choose variable to plot
if sys.argv[2] not in ["rho","prs","tr1","tr2"]:
    raise ValueError("Var to plot must be rho, prs, tr1 or tr2")
else:
    var = sys.argv[2]
# Choose max step to plot
steps = sys.argv[3]

# Get data
data = []

maxstep = -1
for n in range(int(steps)+1):
    try:
        data.append(pp.pload(n, w_dir=path))
        maxstep = n
    except IOError:
        if maxstep==-1:
            print("Path does not contain any data.000x.dbl")
        else:
            print("{} is too high".format(steps))
            print("Plotting gif to step {}".format(maxstep))
            break

# Plotting
os.chdir(path)
for D,n in zip(data, range(maxstep+1)):
    I = pp.Image()
    I.pldisplay(D, getattr(D, var), x1=D.x1, x2=D.x2,
                title=var, label1 = "r", label2="z",
                cbar=(True, "vertical"))
    plt.savefig("{}_{:04d}.png".format(var,n))
    plt.clf()

# Creating gif
os.system("convert -delay 30 {}_*.png {}.gif".format(var,var))
os.system("rm {}_*.png".format(var))
