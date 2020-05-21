#importando as bibliotecas
from iqoptionapi.stable_api import IQ_Option
import time, logging
from datetime import datetime
import getpass

email = str(input("Digite seu Email: "))
senha = getpass.getpass('Digite sua Senha: ')
API = IQ_Option(email, senha)
API.connect()#connect to iqoption

logging.disable(level=(logging.DEBUG))

#Checando a conexão
while True:
	if API.check_connect() == False:
		print('Erro ao conectar')
		API.connect()
	else:
		print('Conectado com sucesso')
		break

	time.sleep(1)

Par = 'EURUSD'
dir_call = 0
dir_put = 0
#Loop principal
while True:
	#Função que pega as ultimas velas para analisar
	#Argumentos: Paridade, Intervalo de Tempo(5s, 60s), Quantidade de Velas, Hora
	velas = API.get_candles(Par, 5, 3, time.time())
	for vela in velas:
		abertura = vela['open']
		fechamento = vela['close']
		print(vela)
	if abertura < fechamento:
		dir_call =+1
	else:
		dir_put +=1
	if dir_call > dir_put:
		direcao = "Put"
	else:
		direcao = "Call"

	#Função que executa a ordem
	check,id = API.buy(1, Par, direcao, 1)
	print("Ordem executada com sucesso")
	saldo = API.get_balance()
	#Criando o objeto que verifica o resultado
	valor_ganho = API.check_win_v3(id)
	print(valor_ganho)
	hora = datetime.now().strftime("%H:%M:%S")
	#Colando as informações no arquivo de relatorio
	relatorio = open("relatorio.txt", "a+")
	relatorio.write("Valor ganho R$:{}"'\t'"Saldo R$:{}"'\t'"Hora:{}".format(str(valor_ganho), str(saldo), str(hora)))
	relatorio.write('\n')
	relatorio.close()
	#função time para esperar os 5 minutos da proxima entrada
	print("Aguardando proxima entrada...")
	time.sleep(60*5)
