import pandas as pd
import numpy as np


class OrderBook:

    def __init__(self, df_data):
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
            row = {'opn_timestamp': a.opn_timestamp, 'cld_timestamp': a.cld_timestamp, 'prise': a.prise}
            if row['cld_timestamp'] == np.nan:
                row['cld_timestamp'] = max_ts
            x = 0
            while x < len(empty_intervals):
                interval = empty_intervals[x]
                if interval['start'] <= row['opn_timestamp'] < interval['finish']:
                    if interval['finish'] >= row['cld_timestamp']:  # полное попадание в интервал
                        report_data.append({'ts': row['cld_timestamp'] - row['opn_timestamp'], 'price':row['prise']})
                        if interval['start'] == row['opn_timestamp'] and interval['finish'] == row['cld_timestamp']:
                            del empty_intervals[x]
                            break
                        elif interval['start'] == row['opn_timestamp']:
                            empty_intervals.append({'start': row['cld_timestamp'], 'finish': interval['finish']})
                            del empty_intervals[x]
                            break
                        elif interval['finish'] == row['cld_timestamp']:
                            empty_intervals.append({'start': interval['start'], 'finish': row['opn_timestamp']})
                            del empty_intervals[x]
                            break
                        else:
                            empty_intervals.append({'start': row['cld_timestamp'], 'finish': interval['finish']})
                            empty_intervals.append({'start': interval['start'], 'finish': row['opn_timestamp']})
                            del empty_intervals[x]
                            break
                    else:
                        report_data.append({'ts': row['cld_timestamp'] - interval['finish'], 'price': row['prise']})
                        if interval['start'] == row['opn_timestamp'] and interval['finish'] == row['cld_timestamp']:
                            del empty_intervals[x]
                            x = x - 1
                        else:
                            empty_intervals.append({'start': row['cld_timestamp'], 'finish': interval['finish']})
                            del empty_intervals[x]
                            x = x - 1

                elif interval['finish'] >= row['cld_timestamp'] > row['opn_timestamp'] and \
                        row['cld_timestamp'] > interval['start']:
                    report_data.append({'ts': row['cld_timestamp'] - interval['start'], 'price': row['prise']})
                    if interval['finish'] == row['cld_timestamp']:
                        del empty_intervals[x]
                        x = x - 1
                    else:
                        empty_intervals.append({'start': interval['start'], 'finish': row['opn_timestamp']})
                        del empty_intervals[x]
                        x = x - 1
                elif row['cld_timestamp'] < interval['start'] < interval['finish'] < row['cld_timestamp']:
                    report_data.append({'ts': interval['finish'] - interval['start'], 'price': row['prise']})
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
        not_cld = np.where(pd.isnull(df_data))[0]
        not_closed_orders = df_data.iloc[not_cld]
        print(not_closed_orders.to_string(index=False))
        print('текущая максимальня цена: ' + str(not_closed_orders['prise'].max()))
