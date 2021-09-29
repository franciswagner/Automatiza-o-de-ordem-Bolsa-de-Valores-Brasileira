import MetaTrader5 as Mt5

import pandas as pd

import numba

from datetime import datetime

import pytz

"""
Inicializa conexão
"""
codigo_tick = "PETR4"
red = "\033[1;31m"
blue = "\033[1;34m"
cyan = "\033[1;36m"
green = "\033[0;32m"
reset = "\033[0;0m"
bold = "\033[;1m"
reverse = "\033[;7m"

if not Mt5.initialize():
    print(Mt5.last_error())
    quit()

selecionado = Mt5.symbol_select(codigo_tick, True)
if not selecionado:
    Mt5.shutdown()
    quit()

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)
timezone = pytz.timezone("Etc/UTC")
utc_from = datetime(2021, 6, 14, 8, 00, tzinfo=timezone)
utc_to = datetime(2021, 9, 14, 15, 00, tzinfo=timezone)
ticks = Mt5.copy_ticks_range(codigo_tick, utc_from, utc_to, Mt5.COPY_TICKS_ALL)
ticks_frame = pd.DataFrame(ticks)
ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
ticks_frame['time_msc'] = pd.to_datetime(ticks_frame['time'], unit='f')
# print(ticks_frame.head(60))
# 344 Venda -  a tendencia ---- 312 Compra -  a tendencia
# 88 Venda -  a tendencia ---- 56 Compra -  a tendencia


@numba.jit
def analise():
    gatilho = False
    entrada = 0
    loss = 0
    gain = 0
    vendido = 0
    comprado = 0
    p = 0

    for tk in ticks:
        # print(ticks)
        if gatilho:
            if p == 88:
                if tk[7] > 10000:
                    profit = entrada - tk[3]
                    if profit <= -0.50:
                        loss = loss + profit
                        gatilho = False
                        vendido = vendido + 1
                    elif profit >= 0.05:
                        gain = gain + profit
                        gatilho = False
                        comprado = comprado + 1
            elif tk[7] > 10000:
                profit = tk[3] - entrada
                if profit <= -0.50:
                    loss = loss + profit
                    gatilho = False
                    vendido = vendido + 1
                elif profit >= 0.05:
                    gain = gain + profit
                    gatilho = False
                    comprado = comprado + 1
        elif tk[6] == 312:
            gatilho = True
            entrada = tk[3]
            p = tk[6]

        elif tk[6] == 344:
            gatilho = True
            entrada = tk[3]
            p = tk[6]

    print("R$:", green, gain, "QTD:", comprado, reset)
    print("R$:", cyan, loss, "QTD:", vendido, reset)


analise()
