from mcculw import ul
from mcculw.enums import TempScale


class DAQChannel():

    def __init__(self, boardNumber, channelNumber, name):
        self.board = boardNumber
        self.channel = channelNumber
        self.name = name

    def getTemperature(self):
        return ul.t_in(self.board, self.channel, TempScale.CELSIUS)