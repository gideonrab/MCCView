from mcculw import ul
from mcculw.enums import TempScale


class DAQChannel():

    def __init__(self, boardNumber, channelNumber):
        self.board = boardNumber
        self.channel = channelNumber

    def getTemperature(self):
        return ul.t_in(self.board, self.channel, TempScale.CELSIUS)