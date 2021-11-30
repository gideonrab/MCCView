import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox
import csv
import time

from PlotContainer import PlotContainer
from DAQChannel import DAQChannel


#Make sure master has removeChannel function
class ChannelWidget(tk.Frame):
    timeData = []
    tempData = []

    startTime = 0
    DAQ = None
    loop = None

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.createWidgets()


    def createWidgets(self):
        #Fields for device and channel #
        self.deviceLabel = tk.Label(self, text="Device #:")
        self.deviceLabel.grid(row=0, column=0, sticky="W")

        self.deviceField = tk.Entry(self)
        self.deviceField.grid(row=0, column=1, sticky="W")

        self.channelLabel = tk.Label(self, text="Channel #:")
        self.channelLabel.grid(row=0, column=2, sticky="W")

        self.channelField = tk.Entry(self)
        self.channelField.grid(row=0, column=3, sticky="W")

        self.startButton = tk.Button(self, text="Start Recording", command=self.startRecording)
        self.startButton.grid(row=1, column=0, sticky="W")

        self.stopButton = tk.Button(self, text="Stop Recording", command=self.stopRecording)
        self.stopButton.grid(row=2, column=0, sticky="W")

        self.resetButton = tk.Button(self, text="Clear Data", command=self.resetData)
        self.resetButton.grid(row=1, column=5, sticky="E")

        self.exportButton = tk.Button(self, text="Export Data", command=self.exportData)
        self.exportButton.grid(row=2, column=5, sticky="E")

        #Exit button
        self.exitButton = tk.Button(self, text="X", command=self.removeSelf, background="#af5f5f")
        self.exitButton.grid(row=0, column=5, sticky="E")
        self.grid_columnconfigure(self.exitButton.grid_info()["column"], weight=1)

        #Graph
        self.plot = PlotContainer(self)
        self.plot.grid(row=3, column=0, columnspan = self.grid_size()[0], sticky="NESW")

        self.plot.axes.set_ylabel("Temperature (C)")
        self.plot.axes.set_xlabel("Time (s)")
        self.plot.axes.set_xlim(0, 10)
        self.plot.axes.set_ylim(10, 40)

        self.plot.addLine()

        self.grid_rowconfigure(self.plot.grid_info()["row"], weight=1)

    def removeSelf(self):
        try:
            self.after_cancel(self.loop)
        except:
            pass
        self.master.removeChannel(self)
    
    def recordData(self):
        tempDatum = self.DAQ.getTemperature()
        timeDatum = time.time() - self.startTime

        if tempDatum == self.tempData[-1]:
            self.loop = self.after(50, self.recordData)
            return

        self.loop = self.after(500, self.recordData)
        self.addDatum(timeDatum, tempDatum)
        
    
    def addDatum(self, timeDatum, tempDatum):
        self.timeData.append(timeDatum)
        self.tempData.append(tempDatum)

        self.plot.drawLine(0, self.timeData, self.tempData)

        xlim = self.plot.axes.get_xlim()
        ylim = self.plot.axes.get_ylim()

        if timeDatum > xlim[1]:
            self.plot.axes.set_xlim(0, xlim[1]+10)
        
        if tempDatum > ylim[1]:
            self.plot.axes.set_ylim(ylim[0], ylim[1]+10)
        elif tempDatum < ylim[0]:
            self.plot.axes.set_ylim(ylim[0]-10, ylim[1])


    def startRecording(self):
        try:
            device = int(self.deviceField.get())
            channel = int(self.channelField.get())

            self.DAQ = DAQChannel(device, channel)
            temp = self.DAQ.getTemperature() # Will throw an error if not a proper device

            if len(self.timeData) == 0 :
                self.startTime = time.time()
            
            self.loop = self.after(500, self.recordData)

            self.addDatum(time.time() - self.startTime, temp)
        except:
            messagebox.showwarning("Invalid Device or Channel", "Hey, you!\nPlease check the device and channel # imputs. Apparently they're not valid")

    def stopRecording(self):
        self.after_cancel(self.loop)

    def resetData(self):
        self.after_cancel(self.loop)
        timeData = []
        tempData = []
        
        self.plot.axes.set_xlim(0, 10)
        self.plot.axes.set_ylim(10, 40)

    def exportData(self):
        file = asksaveasfile(initialfile = 'Untitled.csv', defaultextension=".csv",filetypes=[("All Files","*.*"),("CSV Documents","*.csv")])

        if file != None:
            CSV = csv.writer(file, lineterminator = '\n')

            CSV.writerow(["Time", "Temperature"])
            CSV.writerows(zip(self.timeData, self.tempData))

            file.close()

            self.after_cancel(self.loop)
            timeData = []
            tempData = []
        

