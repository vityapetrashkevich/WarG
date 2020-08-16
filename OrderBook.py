import pandas as pd
import numpy as np


class OrderBook:

    def __init__(self, df_data):
        # список пременных
        # df_data['cld_timestamp'] = df_data.astype(np.int64)
        self.max_to_time = self.make_max_intervals(df_data)
        self.make_valid_order_list(df_data)

    def make_max_intervals(self, df_data):
        min_ts = df_data['opn_timestamp'].min()
        max_cld = df_data['cld_timestamp'].max()
        max_onp = df_data['opn_timestamp'].max()
        df_data = df_data.sort_values('prise', ascending=False)
        if max_cld > max_onp:
            max_ts = max_cld
        else:
            max_ts = max_onp
        empty_intervals = [{'start': min_ts, 'finish': max_ts}]
        report_data = []
        for a in df_data.itertuples(index=False):
            if empty_intervals is None:
                break
            i = {'opn_timestamp': a.opn_timestamp, 'cld_timestamp': a.cld_timestamp, 'prise': a.prise}
            if i['cld_timestamp'] == np.nan:
                i['cld_timestamp'] = max_ts
            x = 0
            while x < len(empty_intervals):
                j = empty_intervals[x]
                if j['start'] <= i['opn_timestamp'] < j['finish']:
                    if j['finish'] >= i['cld_timestamp']:  # полное попадание в интервал
                        report_data.append({'ts': i['cld_timestamp'] - i['opn_timestamp'], 'price': i['prise']})
                        if j['start'] == i['opn_timestamp'] and j['finish'] == i['cld_timestamp']:
                            del empty_intervals[x]
                            x = x-1
                            break
                        elif j['start'] == i['opn_timestamp']:
                            empty_intervals.append({'start': i['cld_timestamp'], 'finish': j['finish']})
                            del empty_intervals[x]
                            x = x - 1
                            break
                        elif j['finish'] == i['cld_timestamp']:
                            empty_intervals.append({'start': j['start'], 'finish': i['opn_timestamp']})
                            del empty_intervals[x]
                            x = x - 1
                            break
                        else:
                            empty_intervals.append({'start': i['cld_timestamp'], 'finish': j['finish']})
                            empty_intervals.append({'start': j['start'], 'finish': i['opn_timestamp']})
                            del empty_intervals[x]
                            x = x - 1
                            break
                    else:
                        report_data.append({'ts': i['cld_timestamp'] - j['finish'], 'price': i['prise']})
                        if j['start'] == i['opn_timestamp'] and j['finish'] == i['cld_timestamp']:
                            del empty_intervals[x]
                            x = x - 1
                        else:
                            empty_intervals.append({'start': i['cld_timestamp'], 'finish': j['finish']})
                            del empty_intervals[x]
                            x = x - 1

                elif j['finish'] >= i['cld_timestamp'] > i['opn_timestamp'] and i['cld_timestamp'] > j['start']:
                    report_data.append({'ts': i['cld_timestamp'] - j['start'], 'price': i['prise']})
                    if j['finish'] == i['cld_timestamp']:
                        del empty_intervals[x]
                        x = x - 1
                    else:
                        empty_intervals.append({'start': j['start'], 'finish': i['opn_timestamp']})
                        del empty_intervals[x]
                        x = x - 1
                elif i['cld_timestamp'] < j['start'] < j['finish'] < i['cld_timestamp']:
                    report_data.append({'ts': j['finish'] - j['start'], 'price': i['prise']})
                    del empty_intervals[x]
                    x = x - 1
                x = x + 1
        v_ts_max = 0
        for i in report_data:
            v_ts_max = v_ts_max + i['ts']*i['price']
        v_ts_max = v_ts_max/(max_ts-min_ts)
        print('Максимальное взмешеное по времени: ' + str(v_ts_max))
        return v_ts_max

    def make_valid_order_list(self, df_data):
        print("Список незавершенных заказов:")
        df_data.set_index('ID')
        not_cld = np.where(pd.isnull(df_data))

        not_cld = not_cld[0]
        a = df_data[lambda x: x['cld_timestamp'] == np.nan]
        b = pd.isnull(df_data)
        # c = df_data.query('cld_timestamp in None')
        e = df_data.iloc[not_cld]
        print(e.to_string(index=False))
