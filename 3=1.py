if selected_option == '3ª = 1ª':
    display_message("================3ª = 1ª=============================================================================")
    display_message("")
    display_message('VERIFICANDO: ' + str(par) + ' às ' + datetime.now().strftime("%H:%M:%S"))
    display_message("")
    time.sleep(118)
    velas = API.get_candles(par, 60, 1, time.time())
    velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
    cores = velas[0]
    display_message(cores)
    if signal == "COMPRA" and preco_atual > media_movel and velas[0] == 'g' and cores.count('d') == 0: dir = 'call'
    if signal == "VENDA" and preco_atual < media_movel and velas[0] == 'r' and cores.count('d') == 0: dir = 'put'
                         
