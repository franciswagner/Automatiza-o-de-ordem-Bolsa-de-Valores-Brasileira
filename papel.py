import time

import MetaTrader5 as Mt5

"""
Inicializa conexão
"""
codigo_tick = "WINV21"
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


def chama():
    tick_anterior = 0
    lista_agrecao_compradora = []
    lista_agrecao_vendedora = []
    while True:
        lot = 1
        deviation = 0

        if Mt5.positions_total() > 0 and float(Mt5.positions_get(symbol=codigo_tick)[0].profit) >= 2.0 and Mt5.positions_get(symbol=codigo_tick)[0].type == 0:
            Mt5.Close(codigo_tick, ticket=Mt5.positions_get(symbol=codigo_tick)[0].ticket)
            time.sleep(1)
        elif Mt5.positions_total() > 0 and float(Mt5.positions_get(symbol=codigo_tick)[0].profit) >= 2.0 and Mt5.positions_get(symbol=codigo_tick)[0].type == 1:
            Mt5.Close(codigo_tick, ticket=Mt5.positions_get(symbol=codigo_tick)[0].ticket)
            time.sleep(1)
        elif Mt5.positions_total() > 0 and float(Mt5.positions_get(symbol=codigo_tick)[0].profit) <= -20.0 and Mt5.positions_get(symbol=codigo_tick)[0].type == 0:
            Mt5.Close(codigo_tick, ticket=Mt5.positions_get(symbol=codigo_tick)[0].ticket)
            time.sleep(1)
        elif Mt5.positions_total() > 0 and float(Mt5.positions_get(symbol=codigo_tick)[0].profit) <= -20.0 and Mt5.positions_get(symbol=codigo_tick)[0].type == 1:
            Mt5.Close(codigo_tick, ticket=Mt5.positions_get(symbol=codigo_tick)[0].ticket)
            time.sleep(1)
        if Mt5.symbol_info_tick(codigo_tick).volume > 5 and Mt5.symbol_info_tick(codigo_tick).flags == 56 and tick_anterior != Mt5.symbol_info_tick(codigo_tick).last:
            lista_agrecao_vendedora = []
            lista_agrecao_compradora.append(Mt5.symbol_info_tick(codigo_tick).volume)
            tick_anterior = Mt5.symbol_info_tick(codigo_tick).last

        elif Mt5.symbol_info_tick(codigo_tick).volume > 5 and Mt5.symbol_info_tick(codigo_tick).flags == 88 and tick_anterior != Mt5.symbol_info_tick(codigo_tick).last:
            lista_agrecao_compradora = []
            lista_agrecao_vendedora.append(Mt5.symbol_info_tick(codigo_tick).volume)
            tick_anterior = Mt5.symbol_info_tick(codigo_tick).last

        if Mt5.symbol_info_tick(codigo_tick).flags == 56 and Mt5.positions_total() == 0 and Mt5.symbol_info(codigo_tick).price_change > 0.5 and len(lista_agrecao_compradora) >= 1:
            request = {
                "action": Mt5.TRADE_ACTION_DEAL, "symbol": codigo_tick, "volume": float(lot), "type": Mt5.ORDER_TYPE_SELL, "price": float(Mt5.symbol_info_tick(codigo_tick).bid), "deviation": deviation, "magic": 10032021, "type_filling": Mt5.ORDER_FILLING_IOC, "expiration": Mt5.ORDER_TIME_GTC, "type_time": Mt5.ORDER_TIME_DAY
            }
            print(f"{red}Venda: ", lista_agrecao_compradora)
            Mt5.order_send(request)

        elif Mt5.symbol_info_tick(codigo_tick).flags == 88 and Mt5.positions_total() == 0 and Mt5.symbol_info(codigo_tick).price_change < -0.5 and len(lista_agrecao_vendedora) >= 1:
            request = {
                "action": Mt5.TRADE_ACTION_DEAL, "symbol": codigo_tick, "volume": float(lot), "type": Mt5.ORDER_TYPE_BUY, "price": float(Mt5.symbol_info_tick(codigo_tick).ask), "deviation": deviation, "magic": 10032021, "type_filling": Mt5.ORDER_FILLING_IOC, "expiration": Mt5.ORDER_TIME_GTC, "type_time": Mt5.ORDER_TIME_DAY
            }
            print(f"{blue}Compra: ", lista_agrecao_vendedora)
            Mt5.order_send(request)


chama()
