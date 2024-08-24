##########################################################################################
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
##########################################################################################


import tkinter as tk
from tkinter import messagebox
import threading
import json
import os
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import time
import sys
import requests
url = "https://github.com/Tesla-369-bot/Aprovados/blob/main/Aprovados.md"
thread_started = False
operacoes = 0

    
def display_message(*args):
    message = " ".join(map(str, args))
    def update_listbox():
        listbox.insert(tk.END, message)
        listbox.yview(tk.END)

    root.after(0, update_listbox)


def load_credentials():
    try:
        with open('credentials.json', 'r') as file:
            data = json.load(file)
            email_var.set(data['email'])
            password_var.set(data['password'])
            account_var.set(data['account'])
            par_var.set(data['par'])
            entry_value_var.set(data['entry_value'])
            gales_var.set(data['gales'])
            stop_loss_var.set(data['stop_loss'])
            stop_gain_var.set(data['stop_gain'])
    except FileNotFoundError:
        pass

def save_credentials():
    data = {
        'email': email_var.get(),
        'password': password_var.get(),
        'account': account_var.get(),
        'par': par_var.get(),
        'entry_value': entry_value_var.get(),
        'gales': gales_var.get(),
        'stop_loss': stop_loss_var.get(),
        'stop_gain': stop_gain_var.get()
    }
    with open('credentials.json', 'w') as file:
        json.dump(data, file)
def minha_funcao():
    
    email = email_var.get()
    password = password_var.get()
    account = account_var.get()
    par = par_var.get()
    entry_value = float(entry_value_var.get())
    gales = int(gales_var.get())
    stop_loss = float(stop_loss_var.get())
    stop_gain = float(stop_gain_var.get())
    if not email or not password:
        messagebox.showerror("Erro", "POR FAVOR, PREENCHE O EMAIL E A SENHA")
        return
    threading.Thread(target=run_script, args=(email, password, account, par, entry_value, gales, stop_loss, stop_gain, balance_label)).start()



def iniciar_script():
    selected_option = global_var.get()
    if selected_option == '':
        display_message("")
        display_message("SELECIONE UMA ESTRATÉGIA!")
        display_message("")
        
        
    else:
        display_message("")
        display_message("VOCÊ SELECIONOU: " + selected_option)
        display_message("CASO QUEIRA TROCAR, APENAS SELECIONE OUTRA.")
        display_message("")
        
        
      
        global thread_started
        if not thread_started:
            thread_started = True
            t = threading.Thread(target=minha_funcao)
            t.start()
        else:
            
            display_message("SOMENTE ESTRATEGIAS PODEM SER TROCADAS EM TEMPO REAL.")
            display_message("CASO QUEIRA MUDAR DE PAR OU VALOR, REINICIE O TESLA.")
            display_message("")
    
def run_script(email, password, account, par, entry_value, gales, stop_loss, stop_gain, balance_label):
    def stop(lucro, gain, loss):
        lucro_str = str(round(lucro, 2)).rstrip('0').rstrip('.')  # Limita a duas casas decimais e remove zeros extras
        if lucro <= float('-' + str(abs(loss))):
            operacoes = 0
            display_message("STOP LOSS AS:" + datetime.now().strftime("%H:%M:%S") + " VOCÊ PERDEU: " + str(lucro) + "$")
            sys.exit()

        if lucro >= float(abs(gain)):
            operacoes = 0
            display_message("STOP GAIN AS:" + datetime.now().strftime("%H:%M:%S") + " VOCÊ GANHOU: " + str(lucro) + "$")
            sys.exit()
   
   

    def Martingale(valor, payout):
        lucro_esperado = valor * payout
        perca = float(valor)

        while True:
            if round(valor * payout, 2) > round(abs(perca) + lucro_esperado, 2):
                return round(valor, 2)
                break
            valor += 0.01

    def Payout(par):
        API.subscribe_strike_list(par, 1)
        while True:
            d = API.get_digital_current_profit(par, 1)
            if d != False:
                d = round(int(d) / 100, 2)
                break
            time.sleep(1)
        API.unsubscribe_strike_list(par, 1)

        return d

    display_message("== EJS ENTERPRISE ==")
    display_message("== TESLA 369 - BOT ==")
    display_message("== O PODER DOS NUMEROS ==")
    display_message("== OPERAÇÃOES POR ENQUANTO ==")
    display_message("== APENAS NAS DIGITAIS ==")
    display_message("")
    display_message("== O MERCADO TIRA DOS IMPACIENTES ==")
    display_message("== PARA DAR AOS PACIENTES! ==")
    display_message("==========================================================================================")
    display_message("")
    
    valor_entrada = entry_value
    valor_entrada_b = float(valor_entrada)

    martingale = gales
    martingale += 1

    stop_loss = stop_loss
    stop_gain = stop_gain
    palavra_chave = email
    palavra_off_tesla = "ROBOOFF"
    response = requests.get(url)
    conteudo = response.text

    if palavra_off_tesla in conteudo:
        display_message("==========================================================================================")
        display_message("")
        display_message("ROBÔ DESATIVADO POR TEMPO INDETERMINADO!") 
        display_message("EM CASO DE DUVIDAS ENTRE EM CONTATO") 
        display_message("PELO WHATSAPP")
        display_message("62996942287")
        display_message("==========================================================================================")
        display_message("")
        time.sleep(10)
        sys.exit()

    if palavra_chave in conteudo:
       display_message("TESLA LIBERADO PARA : "+ palavra_chave)
    else:
        display_message("==========================================================================================")
        display_message("")
        display_message(palavra_chave+": VOCÊ NÃO POSSUI UMA LICENÇA!")
        display_message("PARA ADQUIRIR UMA LICENÇA")
        display_message("ENTRE EM CONTATO PELO WHATSAPP")
        display_message("62996942287")
       
        display_message("==========================================================================================")
        display_message("")
        time.sleep(20)
        sys.exit()

    API = IQ_Option(email, password)
    API.connect()

    API.change_balance(account)
    saldo_atual = API.get_balance()
    balance_label.config(text=f"Saldo: ${saldo_atual:.2f}")


    if API.check_connect():
        display_message("CONECTADO COM SUCESSO!")
    
     
    else:
        display_message("ERRO AO CONECTAR")
        speak_text("ERRO AO CONECTAR. por favor verifique se se a senha ou email esta correto e se naão tem nenhum espaço entre eles")
        time.sleep(5)
        sys.exit()
      
  
    lucro = 0
    global operacoes
    
    display_message("==========================================================================================")
    display_message("")
    display_message("TRABALHANDO... AGUARDE E SEJA PACIENTE!")
    display_message("TE AVISAREI QUANDO ACONTECER ALGUMA OPERAÇÃO!")
    display_message("==========================================================================================")
    display_message("")
    display_message("TESLA INICIADO ÁS :" + datetime.now().strftime("%H:%M:%S"))
    display_message("==========================================================================================")
    display_message("")
    

    while True:
        
        try:
            
            while True:
                
                
                selected_option = global_var.get()
                hora_atual = datetime.now().strftime('%H:%M:%S')
                agora = datetime.now()
                minutos = agora.minute
                segundos = agora.second
                payout = Payout(par)
              
                if selected_option == '3ª = 1ª':
                    entrar = True if minutos % 5 == 0 else False

                    
                if entrar:
                    
    
                    dir = False
                    status = False

                    candles = API.get_candles(par, 60, 22, time.time())
                    preco_atual = candles[-1]['close']
                    media_movel = sum(candle['close'] for candle in candles[:-1]) / 21








                    

                        #=======================================================3ª = 1ª==============================================================
                    if selected_option == '3ª = 1ª':
                        display_message("================3ª = 1ª=============================================================================")
                        display_message("")
                        display_message('VERIFICANDO: ' + str(par) + ' às ' + datetime.now().strftime("%H:%M:%S"))
                        display_message("")
                        time.sleep(118)
                        ####################################################################################################################################################################################
                        diferenca = preco_atual - media_movel
                        limite_compra = 0.30
                        limite_venda = -0.30
                        candles = API.get_candles(par, 60, 200, time.time())
                        if candles is None:
                            display_message("___Erro ao obter os dados do par.\n")
                            return
                        X = np.array([candle["close"] for candle in candles])
                        y = np.array([1 if candle["close"] > candle["open"] else 0 for candle in candles])
                        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                        model = RandomForestClassifier(n_estimators=100, random_state=42)
                        model.fit(X_train.reshape(-1, 1), y_train)
                        accuracy = model.score(X_test.reshape(-1, 1), y_test)
                        new_data = np.array([X[-1]])
                        prediction = model.predict(new_data.reshape(-1, 1))
                        confidence = model.predict_proba(new_data.reshape(-1, 1))[0][prediction[0]]
                        signal = "COMPRA" if prediction[0] == 1 else "VENDA"
                        confidence = accuracy * 100
                        display_message('___ANALISANDO CONFIANÇA AS: ' + datetime.now().strftime("%H:%M:%S") + '\n')
                        if confidence >= 51 and confidence <= 75:
                            if signal == "COMPRA":
                                if preco_atual > media_movel and diferenca < limite_compra:
                                    display_message("___SINAL DE ENTRADA: {}\n".format(signal))
                                    display_message("___CONFIANCA: {:.2f}%\n".format(confidence))
                            if signal == "VENDA":
                                if preco_atual < media_movel and diferenca > limite_venda:
                                    display_message("___SINAL DE ENTRADA: {}\n".format(signal))
                                    display_message("___CONFIANCA: {:.2f}%\n".format(confidence))
                       ####################################################################################################################################################################################
                   
                        velas = API.get_candles(par, 60, 1, time.time())
                        velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
                        
                        cores = velas[0]
                            
                        display_message(cores)
                            
                        if signal == "COMPRA" and preco_atual > media_movel and velas[0] == 'g' and cores.count('d') == 0: dir = 'call'
                        if signal == "VENDA" and preco_atual < media_movel and velas[0] == 'r' and cores.count('d') == 0: dir = 'put'
                        #=======================================================3ª = 1ª==============================================================
                    
                    
                ####################################################################################################################################################################################
                   
                    if dir:
                        
                        display_message('OPERAÇÃO EM :', par, dir, ' às', datetime.now().strftime("%H:%M:%S"))
                        display_message("==========================================================================================")
                        display_message("")
                        valor_entrada = valor_entrada_b
                        for i in range(martingale):

                            if selected_option == '9:30/EURUSD' or selected_option == 'M5':
                                status, id = API.buy_digital_spot(par, valor_entrada, dir, 5)
                            else:
                                status, id = API.buy_digital_spot(par, valor_entrada, dir, 1)
                                
                            if status:
                                while True:
                                    
                                    status, valor = API.check_win_digital_v2(id)
                                    

                                    if status:
                                        valor = valor if valor > 0 else float('-' + str(abs(valor_entrada)))
                                        lucro += round(valor, 2)
                                        
                                        display_message('RESULTADO DA OPERAÇÃO: ')
                                        display_message('WIN ' if valor > 0 else 'LOSS ', round(valor, 2), '/ lucro:', round(lucro, 2), ('/ ' + str(i) + ' GALE' if i > 0 else ''))
                                        valor_entrada = Martingale(valor_entrada, payout)
                                        stop(lucro, stop_gain, stop_loss)
                                        saldo_atual = API.get_balance()
                                        balance_label.config(text=f"Saldo: ${saldo_atual:.2f}")
                                        operacoes = operacoes +1
                                        display_message("")
                                        display_message("==========================================================================================")
                                        display_message("")
                                        display_message('TRABALHANDO...')

                                        break

                                if valor > 0: break

                            else:
                                display_message("==========================================================================================")
                                display_message("")
                                display_message('ERRO AO REALIZAR OPERAÇÃO!')
                                display_message("==========================================================================================")
                                display_message("")
                    time.sleep(3)
        except Exception as e:
            display_message("==========================================================================================")
            display_message("")
            display_message(f'Erro: {e}')
            print(f'Erro: {e}')
            display_message('REINICIANDO O ROBÔ...')
            display_message("==========================================================================================")
            display_message("")
            time.sleep(3)
    


root = tk.Tk()
root.title("TESLA 369 BOT - EJS ENTERPRISE")
root.geometry("400x600")
checkbox_var = tk.BooleanVar()

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(9, weight=1)

root.configure(bg="white")

email_var = tk.StringVar()
password_var = tk.StringVar()
account_var = tk.StringVar()
par_var = tk.StringVar()
entry_value_var = tk.StringVar()
gales_var = tk.StringVar()
stop_loss_var = tk.StringVar()
stop_gain_var = tk.StringVar()
global_var = tk.StringVar()

load_credentials()

scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=9, column=1, sticky='nsew')

listbox = tk.Listbox(root, yscrollcommand=scrollbar.set, width=50, height=10, bg="black", fg="yellow")
listbox.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

scrollbar.config(command=listbox.yview)

tk.Label(root, text="E-mail:").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=email_var).grid(row=0, column=1)

tk.Label(root, text="Senha:").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=password_var, show="*").grid(row=1, column=1)

tk.Label(root, text="Conta (REAL/PRACTICE):").grid(row=2, column=0, sticky="e")
tk.Entry(root, textvariable=account_var).grid(row=2, column=1)

tk.Label(root, text="Par (EURUSD/EURUSD-OTC):").grid(row=3, column=0, sticky="e")
tk.Entry(root, textvariable=par_var).grid(row=3, column=1)

tk.Label(root, text="Valor de entrada:").grid(row=4, column=0, sticky="e")
tk.Entry(root, textvariable=entry_value_var).grid(row=4, column=1)

tk.Label(root, text="Gales:").grid(row=5, column=0, sticky="e")
tk.Entry(root, textvariable=gales_var).grid(row=5, column=1)

tk.Label(root, text="Stop Loss:").grid(row=6, column=0, sticky="e")
tk.Entry(root, textvariable=stop_loss_var).grid(row=6, column=1)

tk.Label(root, text="Stop Gain:").grid(row=7, column=0, sticky="e")
tk.Entry(root, textvariable=stop_gain_var).grid(row=7, column=1)

balance_label = tk.Label(root, text="Saldo: $0.00")
balance_label.grid(row=8, column=1, padx=10, pady=5, columnspan=2)


tk.Label(root, text="Estrategias:").grid(row=8, column=0, sticky="w")

options = ["TESLA-369", "MHI-FILTRADO", "3ª = 1ª", "QUADRANTE DE 7","FLUXO-DE-VELAS", "9:30/EURUSD", "REVERSÃO", "M5"]
option_menu = tk.OptionMenu(root, global_var, *options)
option_menu.grid(row=8, column=0, sticky="e")

start_button = tk.Button(root, text="Iniciar", command=iniciar_script)
start_button.grid(row=8, column=1, sticky="w")

def on_closing():
    save_credentials()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
