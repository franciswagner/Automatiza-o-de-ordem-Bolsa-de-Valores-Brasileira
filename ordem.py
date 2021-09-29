import MetaTrader5 as Mt5

codigo_tick = "PETR3F"

if not Mt5.initialize(login="", server="", password=""):
    print(Mt5.last_error())
    quit()

selecionado = Mt5.symbol_select(codigo_tick, True)

if not selecionado:
    Mt5.shutdown()
    quit()

lot = 1
price = Mt5.symbol_info_tick(codigo_tick).ask
deviation = 1
request = {
    "action": Mt5.TRADE_ACTION_DEAL, "symbol": codigo_tick, "volume": float(lot), "type": Mt5.ORDER_TYPE_BUY, "price": price, "sl": price - 0.05,
    "tp": price + 0.05, "deviation": deviation, "magic": 10032021, "type_time": Mt5.ORDER_TIME_GTC, "type_filling": Mt5.ORDER_FILLING_RETURN,
}

resultado = Mt5.order_send(request)

Mt5.shutdown()


