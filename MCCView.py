import tkinter as tk

from ChannelWidget import ChannelWidget
from PlotWidget import PlotWidget


from tkinter.filedialog import asksaveasfile
import csv

class MCCView(tk.Tk):
    channels = set()

    def __init__(self):
        tk.Tk.__init__(self)
        self.configureWindow()
        self.createWidgets()


    def configureWindow(self):
        self.title("Demo")
        self.geometry("1024x720")

    def createWidgets(self):
        #Channel Setup
        self.channels = ChannelWidget(self)
        self.channels.grid(row=0, column=0, sticky="NSW")

        #Plotter setup
        self.plotter = PlotWidget(self)
        self.plotter.grid(row=0, column=1, sticky="NSEW")
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)

    def getDAQs(self):
        return self.channels.getDAQs()

if __name__ == '__main__':
    app = MCCView()
    app.mainloop()
