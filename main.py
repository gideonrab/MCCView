import tkinter as tk
import matplotlib.pyplot as plt

from DAQChannel import DAQChannel

class Application(tk.Frame):  
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.configureGUI()
        self.createWidgets()

        self.thermo = DAQChannel(0, 1)

    def configureGUI(self):
        self.master.title("Demo")
        self.master.geometry("500x500")

    def createWidgets(self):
        self.readButton = tk.Button(self.master, text="Get temperature", command=self.readButtonCallBack)
        self.readButton.grid()

        self.label = tk.Label(self.master, text="Hello World")
        self.label.grid()

    def readButtonCallBack(self):
        self.label.configure(text= str(self.thermo.getTemperature()))

if __name__ == '__main__':
    app = Application()
    app.mainloop()
