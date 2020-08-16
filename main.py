# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import numpy as np
from ReadData import ReadFile
from OrderBook import OrderBook


def main_f():
    file_name = input("Введите путь к файлу: ")
    data = ReadFile.input(file_name)
    OrderBook(data)
    input('Нажмите любую клавишу...')


if __name__ == '__main__':
    main_f()



