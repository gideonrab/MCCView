import tkinter as tk
from tkinter.filedialog import asksaveasfile
import csv
import time
import math

from PlotContainer import PlotContainer
from DAQChannel import DAQChannel


#Parent must have getDAQs method
class PlotWidget(tk.Frame):
    timeData = []
    tempData = []

    startTime = 0
    DAQs = []
    loop = None

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.createWidgets()

        for i in range(4):
            self.plot.addLine()


    def createWidgets(self):
        self.startButton = tk.Button(self, text="Start Recording", command=self.startRecording)
        self.startButton.grid(row=0, column=0, sticky="W")

        self.stopButton = tk.Button(self, text="Stop Recording", command=self.stopRecording)
        self.stopButton.grid(row=1, column=0, sticky="W")

        self.grid_columnconfigure(1, weight=1)

        self.resetButton = tk.Button(self, text="Clear Data", command=self.resetData)
        self.resetButton.grid(row=0, column=2, sticky="E")

        self.exportButton = tk.Button(self, text="Export Data", command=self.exportData)
        self.exportButton.grid(row=1, column=2, sticky="E")

        #Graph
        self.plot = PlotContainer(self)
        self.plot.grid(row=2, column=0, columnspan = self.grid_size()[0], sticky="NESW")

        self.plot.axes.set_ylabel("Temperature (C)")
        self.plot.axes.set_xlabel("Time (s)")
        self.plot.axes.set_xlim(0, 10)
        self.plot.axes.set_ylim(10, 40)

        self.grid_rowconfigure(self.plot.grid_info()["row"], weight=1)
        

    def recordData(self):
        tempData = [DAQ.getTemperature() for DAQ in self.DAQs]
        print(tempData)
        print(self.tempData)
        timeDatum = time.time() - self.startTime

        for i in range(len(self.DAQs)):
            if tempData[i] == self.tempData[i][-1]:
                self.loop = self.after(50, self.recordData)
                return

        self.loop = self.after(500, self.recordData)
        self.addDatum(timeDatum, tempData)
        
    
    def addDatum(self, timeDatum, tempData):
        print("added")
        xlim = self.plot.axes.get_xlim()
        ylim = self.plot.axes.get_ylim()

        self.timeData.append(timeDatum)

        for i in range(len(tempData)):
            self.tempData[i].append(tempData[i])
            
            self.plot.drawLine(i, self.timeData, self.tempData[i])

            if tempData[i] > ylim[1]:
                self.plot.axes.set_ylim(ylim[0], 10*math.ceil(tempData[i]/10))
            elif tempData[i] < ylim[0]:
                self.plot.axes.set_ylim(10*math.floor(tempData[i]/10), ylim[1])

        if timeDatum > xlim[1]:
            self.plot.axes.set_xlim(0, xlim[1]+10)
            

    def startRecording(self):
        #If not resuming
        if self.DAQs == []:
            self.DAQs = self.master.getDAQs()

            if self.DAQs == []: #No useful rows
                return
            
            self.startTime = time.time()
            self.tempData = [[] for DAQ in self.DAQs]

        tempData = [DAQ.getTemperature() for DAQ in self.DAQs]
        timeDatum = time.time() - self.startTime
        
        #Start the loop
        self.loop = self.after(500, self.recordData)

        self.addDatum(timeDatum, tempData)


    def stopRecording(self):
        self.after_cancel(self.loop)

    def resetData(self):
        self.after_cancel(self.loop)
        self.timeData = []
        self.tempData = []
        self.DAQs = []
        
        
        self.plot.axes.set_xlim(0, 10)
        self.plot.axes.set_ylim(10, 40)

        for i in range(4):
            self.plot.drawLine(i, [], [])
        

    def exportData(self):
        file = asksaveasfile(initialfile = 'Untitled.csv', defaultextension=".csv",filetypes=[("All Files","*.*"),("CSV Documents","*.csv")])

        if file != None:
            CSV = csv.writer(file, lineterminator = '\n')

            CSV.writerow(["Time"] + [DAQ.name for DAQ in self.DAQs])
            CSV.writerows(zip(self.timeData,*self.tempData))

            file.close()

            self.resetData()