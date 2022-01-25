import tkinter as tk
from tkinter import messagebox
import csv
import time

from PlotContainer import PlotContainer
from DAQChannel import DAQChannel


#Make sure master has removeChannel function
class ChannelWidget(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.createWidgets()


    def createWidgets(self):
        #Column Headers
        self.deviceLabel = tk.Label(self, text="Device #:")
        self.deviceLabel.grid(row=0, column=0, sticky="W")

        self.channelLabel = tk.Label(self, text="Channel #:")
        self.channelLabel.grid(row=0, column=1, sticky="W")

        self.nameLabel = tk.Label(self, text="Channel Name:")
        self.nameLabel.grid(row=0, column=2, sticky="W")

        self.deviceFields = []
        self.channelFields = []
        self.nameFields = []

        for i in range(4):
            self.addChannelRow()

    def addChannelRow(self):
        self.deviceFields.append(tk.Entry(self))
        self.deviceFields[-1].grid(row = self.grid_size()[1], column=0, sticky="W")

        self.channelFields.append(tk.Entry(self))
        self.channelFields[-1].grid(row = self.grid_size()[1] - 1, column=1, sticky="W")

        self.nameFields.append(tk.Entry(self))
        self.nameFields[-1].grid(row = self.grid_size()[1] - 1, column=2, sticky="W")

    def getDAQs(self):
        DAQs = []

        for i in range(len(self.deviceFields)):
            if self.deviceFields[i].get() != "":
                try:
                    device = int(self.deviceFields[i].get())
                    channel = int(self.channelFields[i].get())
                    name = self.nameFields[i].get()

                    DAQs.append(DAQChannel(device, channel, name))

                    DAQs[-1].getTemperature() # Will throw an error if not a proper device

                except:
                    messagebox.showwarning("Invalid Device or Channel", "Hey, you!\nPlease check the device and channel # imputs. Apparently they're not valid")
                    return [] #Exit so user has to fix error

        return DAQs
                