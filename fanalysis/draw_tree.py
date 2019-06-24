from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle, Ellipse
from matplotlib.offsetbox import (
    AnchoredOffsetbox, AuxTransformBox, DrawingArea, TextArea, VPacker)
import matplotlib.patches as mpatches




class AnchoredDrawingArea(AnchoredOffsetbox):
    def __init__(self, width, height, xdescent, ydescent,
                 loc, pad=0.4, borderpad=0.5, prop=None, frameon=True):
        self.da = DrawingArea(width, height, xdescent, ydescent)
        super().__init__(loc, pad=pad, borderpad=borderpad,
                         child=self.da, prop=None, frameon=frameon)




def draw_circle(ax):
    """
    Draw a circle in axis coordinates
    """
    from matplotlib.patches import Circle
    ada = AnchoredDrawingArea(20, 20, 0, 0,
                              loc='upper right', pad=0., frameon=False)
    p = Circle((10, 10), 10)
    ada.da.add_artist(p)
    ax.add_artist(ada)



for i, (stylename, styleclass) in enumerate(sorted(styles.items())):
    print(i, (stylename, styleclass))
    x = 3.2 + (i // nrow) * 4
    y = (figheight - 0.7 - i % nrow)  # /figheight
    p = mpatches.Circle((x, y), 0.2)
    ax.add_patch(p)

    ax.annotate(to_texstring(stylename), (x, y),
                (x - 1.2, y),
                ha="right", va="center",
                size=fontsize,
                arrowprops=dict(arrowstyle=stylename,
                                patchB=p,
                                shrinkA=5,
                                shrinkB=5,
                                fc="k", ec="k",
                                connectionstyle="arc3,rad=-0.05",
                                ),
                bbox=dict(boxstyle="square", fc="w"))



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import math

fig, ax = plt.subplots(frameon=False)
#ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1.)


y= 0.
r = 0.2
x =r
d = math.sqrt((r**2.)/2.)

xlim = [0, 3]
ylim = [-5, 3]


ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_aspect(1.)

#lvl1
p1 = mpatches.Circle((x, y), r, facecolor='none', edgecolor = 'black')

#lvl2
p2 = mpatches.Circle((x+0.75, y+0.75), r, facecolor='none', edgecolor = 'black')
p3 = mpatches.Circle((x+0.75, y-0.75), r, facecolor='none', edgecolor = 'black')

#lvl1
#rw1
line1 = lines.Line2D([r, r], [r, 0.75], color = 'black')
line2 = lines.Line2D([r, 0.75], [0.75, 0.75], color = 'black')
#rw2
line3 = lines.Line2D([r, r], [-r, -0.75], color = 'black')
line4 = lines.Line2D([r, 0.75], [-0.75, -0.75], color = 'black')
#####

#lvl2
#rw1
line5 = lines.Line2D([r+0.75, r+0.75], [r+0.75, 0.75+0.75], color = 'black')
line6 = lines.Line2D([r+0.75, 0.75+0.75], [0.75+0.75, 0.75+0.75], color = 'black')

line7 = lines.Line2D([r+0.75, r+0.75], [-r+0.75, -0.75+0.75], color = 'black')
line8 = lines.Line2D([r+0.75, 0.75+0.75], [-0.75+0.75, -0.75+0.75], color = 'black')

#rw2
line7 = lines.Line2D([r+0.75, r+0.75], [-r-0.75, -0.75-0.75], color = 'black')
line8 = lines.Line2D([r+0.75, 0.75+0.75], [0.75+0.75, 0.75-0.75], color = 'black')

line9 = lines.Line2D([r+0.75, r+0.75], [-r+0.75, -0.75+0.75], color = 'black')
line10 = lines.Line2D([r+0.75, 0.75+0.75], [-0.75+0.75, -0.75+0.75], color = 'black')
#####


ax.add_line(line1)
ax.add_line(line2)
ax.add_line(line3)
ax.add_line(line4)

ax.add_line(line5)
ax.add_line(line6)
ax.add_line(line7)
ax.add_line(line8)

ax.add_patch(p1)
ax.add_patch(p2)
ax.add_patch(p3)
