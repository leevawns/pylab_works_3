#icon = applications-accessories.png

## Scope_Plot / Scope_Display
"""
- bottom/top label click dialog: add set color of signal
- real-time, history signal is lost during rescale
- implement linewidth of signals
- sometimes a hole in the history signal after compression is increased
  (this seems to happy only with long signal fragments)
- calibration of numerical labels top/bottom/signal
- timebase compression normal display in realtime mode
- start / stop has some noise
- AC/DC coupling
- triggering
- all measured values viewable in a grid
"""

## Code Editor
"""
- force autocompletion if special imports, like Visual / 2D_Scene
"""

##Control IDE
"""
 - setting the initial width of the AUI-panes in the sumulation
 - multi-control support ?
"""

##GUI-support
"""
 - extend Save_Restore with complex types, like Class_URL_Viewer, Base_STC
"""

##DONT USE
"""
 - wx.MiniFrame: not visible in taskbar, can't be shown by alt-tab when hidden
 - AssignImageList gives away full ownership (use SetImageList instead)
"""

## Control_HTML
"""
- Standalone editor for creating the pages
  (richtextctrl is too buggy and limited for now)
"""


## MatPlot
"""
- crosshair in polar: must be a circle with a midline ?
- crosshair in pseudo color: add z-value
- crosshair in pseudo color: should not work in colorbar
- crosshair in pseudo color: z-waarde in colorbar aangeven
- legend in polar should become figlegend ??
- BUG in MatPlot: in xy-plot and pseudo-color-plot, when axis are removed
"""

## VPython Cherry Tree
"""
- Embed the tree into a class with keyword arguments
  such as colors, sizes, depth, fullness, etc...
- Add texture to make it more realistic
- Create a small forest
- Implement dynamic looks like the effect of waves of wind
"""