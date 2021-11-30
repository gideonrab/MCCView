import tkinter as tk
from tkinter import ttk

from ChannelWidget import ChannelWidget

class Application(tk.Tk):
    channels = set()

    def __init__(self):
        tk.Tk.__init__(self)
        self.configureWindow()
        self.createWidgets()


    def configureWindow(self):
        self.title("Demo")
        self.geometry("500x500")

    def createWidgets(self):
        self.readButton = tk.Button(self.master, text="Add Channel", command=self.addChannel)
        self.readButton.grid(sticky="EW")

        self.grid_columnconfigure(0, weight=1)

        self.addChannel()

    def addChannel(self):
        channel = ChannelWidget(self)
        self.channels.add(channel)
        channel.grid(sticky="NESW")
        self.grid_rowconfigure(channel.grid_info()["row"], weight=1)

    def removeChannel(self, channel):
        self.grid_rowconfigure(channel.grid_info()["row"], weight=0)
        channel.grid_forget()
        self.channels.remove(channel)

if __name__ == '__main__':
    app = Application()
    app.mainloop()
