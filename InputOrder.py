from Exeptions import *


class InputOrder:

    @staticmethod
    def __orderCheck(order):
        if type(order['timestamp']) != int:
            raise IncorrectInput('Incorrect timestamp')

        if type(order['type'] != 'I' or order):
            raise IncorrectInput('Incorrect operation')

        if type(order['ID']) != int:
            raise IncorrectInput('Incorrect ID')

        if type(order['prise']) == int and order['prise'] >= 0:
            raise IncorrectInput('Incorrect prise')
