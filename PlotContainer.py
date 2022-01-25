import tkinter as tk

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class PlotContainer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.createWidgets()

    def createWidgets(self):

        #Create plot
        self.figure = Figure()
        self.canvas = FigureCanvasTkAgg(self.figure, self)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update() #Seems to work fine without this, but all the examples had it

        self.canvas.get_tk_widget().pack(side="bottom", fill="both", expand=True)

        self.axes = self.figure.add_subplot(111)

        self.canvas.draw()

    def addLine(self):
        self.axes.plot([], [], "d")
    
    def drawLine(self, index, xData, yData):
        self.axes.lines[index].set_xdata(xData)
        self.axes.lines[index].set_ydata(yData)
        self.canvas.draw()

    def legend(self, labels):
        self.axes.legend(labels)