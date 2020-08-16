from Exeptions import IncorrectInput
import pandas as pd


class ReadFile:

    last_timestamp = 0

    @staticmethod
    def input(path):
        with open(path) as file:
            data = file.read().splitlines()
        control_data_id = []
        dict_data_inp = {}
        dict_data_del = {}
        j = 1
        for i in data:
            a = i.split(' ')
            j += 1
            if a[1] == 'I':
                control_data_id.append(a[2])
                try:
                    dict_data_inp = ReadFile.add_order_input(dict_data_inp, a)
                except IncorrectInput:
                    continue
            elif a[1] == 'E':
                if a[2] in control_data_id:
                    try:
                        dict_data_del = ReadFile.del_order_input(dict_data_del, a)
                    except IncorrectInput:
                        print('str num is '+str(j))
                        continue
                else:
                    print('Некоректная строка со значениями' + str(a) + ' - такой заказ не был добавден, строка № '
                          + str(j))
                #
            else:
                print('incorrect input at line '+str(j))
            j = j + 1

        add_orders_df = pd.DataFrame(dict_data_inp)
        add_orders_df.set_index('ID')
        del_orders_df = pd.DataFrame(dict_data_del)
        del_orders_df.set_index('ID')
        data = pd.merge(add_orders_df, del_orders_df, how='left', on='ID')
        return data

    @staticmethod
    def add_order_input(dict_add, order):

        if int(order[0]) < ReadFile.last_timestamp:  # контроль наростания метки времени
            raise IncorrectInput('Incorrect timestamp in ' + order[0])

        if float(order[3]) < 0:
            raise IncorrectInput('Incorrect prise')  # контроль адекватности цены (цена должна быть больше нуля)

        if len(dict_add) == 0:
            dict_add = {'opn_timestamp': [int(order[0])], 'ID': [int(order[2])], 'prise': [float(order[3])]}
        else:
            dict_add['opn_timestamp'].append(int(order[0]))
            dict_add['ID'].append(int(order[2]))
            dict_add['prise'].append(float(order[3]))
        ReadFile.last_timestamp = int(order[0])
        return dict_add

    @staticmethod
    def del_order_input(dict_del, order):
        if int(order[0]) < ReadFile.last_timestamp:  # контроль наростания метки времени
            raise IncorrectInput('Incorrect timestamp')
        if len(dict_del) == 0:
            dict_del = {'cld_timestamp': [int(order[0])], 'ID': [int(order[2])]}
        else:
            dict_del['cld_timestamp'].append(int(order[0]))
            dict_del['ID'].append(int(order[2]))
        ReadFile.last_timestamp = int(order[0])
        return dict_del

