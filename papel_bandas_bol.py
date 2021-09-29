import yfinance as yf


red = "\033[1;31m"
blue = "\033[1;34m"
cyan = "\033[1;36m"
green = "\033[0;32m"
reset = "\033[0;0m"
bold = "\033[;1m"
reverse = "\033[;7m"

lista_acao = "VALE3", "ITUB4", "B3SA3", "PETR4", "BBDC4", "MGLU3", "ABEV3", "WEGE3", "ITSA4", "BBAS3", "GNDI3", "RENT3", "SUZB3", "JBSS3", "NTCO3", "LREN3", "RADL3", "RAIL3", "BRDT3", "BBDC3", "AMER3", "GGBR4", "EQTL3", "UGPA3", "BTOW3", "VIVT3", "BPAC11", "BBSE3", "CAML3", "ROMI3", "BIDI11", "CYRE3", "WEGE3", "KLBN3", "GOAU4", "COGN3", "CCRO3", "BEEF3", "GOLL4", "ALLD3", "MOVI3", "IRBR3", \
             "TAEE11", "TRPL4", "AALR3", "SAPR11"


def chamaaaaa(pp):
    acao = yf.Ticker(f"{pp}.SA")
    data = acao.history(period='1y')
    df = data[['Close']]
    mm = df.rolling(window=20).mean()
    dpm = df.rolling(window=20).std()
    sup_band = mm + 2 * dpm
    inf_band = mm - 2 * dpm
    sup_band = sup_band.rename(columns={'Close': 'Superior'})
    inf_band = inf_band.rename(columns={'Close': 'Inferior'})

    bandas_bollinger = df.join(sup_band).join(inf_band)
    bandas_bollinger.dropna(inplace=True)

    compra = bandas_bollinger[bandas_bollinger['Close'] <= bandas_bollinger['Inferior']]
    venda = bandas_bollinger[bandas_bollinger['Close'] >= bandas_bollinger['Superior']]
    print(f"{cyan}░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░{green}{pp}{cyan}░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░{reset}")
    print(f"{blue}{compra}{reset}")
    print(f"{red}{venda}{reset}")


def imprimir_lista():
    for i, x in enumerate(lista_acao):
        print(str(i) + ": " + x)


while True:
    print("(L) Para imprimir a lista ou (X) para sair:")
    papel = input().upper()
    if papel == "L":
        imprimir_lista()
        print("Informe o papel:")
        papel = input()
        chamaaaaa(lista_acao[int(papel)])
    elif papel == "X":
        exit()
    elif papel != "L" or papel != "X":
        print("Comando não aceito!")
