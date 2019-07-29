import pandas as pd


def read_csv(ip_data, sep=','):
    with open(ip_data, 'r', encoding='UTF-8') as rd:
        data = pd.read_csv(rd, sep=sep)
    return data


# write csv file #
def write_csv(data, op_data, sep=',', index=False):
    data.to_csv(op_data, sep=sep, index=index)


