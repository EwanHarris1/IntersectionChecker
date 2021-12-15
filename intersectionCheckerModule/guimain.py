# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 14:49:15 2021

@author: ewanh
"""
import time
import intersectionClass
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg

fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
matplotlib.use("TkAgg")

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

# Define the window layout
layout = [
    [sg.Text("Plot test",key='writing')],
    [sg.Canvas(key="-CANVAS-")],
    [sg.Button("Ok")],
]

# Create the form and show it without the plot
window = sg.Window(
    "Matplotlib Single Graph",
    layout,
    location=(0, 0),
    finalize=True,
    element_justification="center",
    font="Helvetica 18",
)

# Add the plot to the window
canvagg=draw_figure(window["-CANVAS-"].TKCanvas, fig)
ax1 = fig.add_subplot(111)
#prompt user to input polygon coordinates
window['writing'].update('Click to Select the verteces of polygon cyclically. Press enter when complete. Backspace to undo a point')
polycoords=np.array(fig.ginput(-1))

length=len(polycoords)
#reshape polygon coordinates for plotting
temp=polycoords.T
[trix,triy]=np.reshape(temp,[2,length])
#display polygon
ax1.plot(trix,triy,'b')
ax1.plot([trix[0],trix[length-1]],[triy[0],triy[length-1]],'b')
canvagg.draw()

#prompt user to select circle centre
window['writing'].update('click to select centre of circle')
circlecoords=np.array(fig.ginput(1))[0]

ax1.plot(circlecoords[0],circlecoords[1],'r+')
canvagg.draw()
#prompt user to select edge of circle
window['writing'].update('click to select edge of circle')
R=float(np.linalg.norm(np.array(fig.ginput(1))-circlecoords))
#plot circle
circle = plt.Circle(circlecoords, R)
ax1.add_artist(circle)
#create intersection pair object using user input
pair=intersectionClass.IntersectionPair(polygonpts=polycoords,circlept=circlecoords,r=R)

#Draw lines of intersections in a different colour (red)
for i in range(0,length-1):
    if pair.intersecting[i]:
        ax1.plot([trix[i],trix[i+1]],[triy[i],triy[i+1]],'r')
    else:
        ax1.plot([trix[i],trix[i+1]],[triy[i],triy[i+1]],'b')
if pair.intersecting[length-1]:
    ax1.plot([trix[0],trix[length-1]],[triy[0],triy[length-1]],'r')
else:
    ax1.plot([trix[0],trix[length-1]],[triy[0],triy[length-1]],'b')
canvagg.draw()
#display result
window['writing'].update(pair.summary)
event, values = window.read()
window.close()
