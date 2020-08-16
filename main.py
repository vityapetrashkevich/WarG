from ReadData import ReadFile
from OrderBook import OrderBook
import sys

def main_f(file_name):
    if file_name is None:
        file_name = input("Введите путь к файлу: ")
    data = ReadFile.input(file_name)
    OrderBook(data)
    input('Нажмите любую клавишу...')


if __name__ == '__main__':
    try:
        main_f(file_name=sys.argv[1])
    except IndexError:
        main_f(file_name=None)
