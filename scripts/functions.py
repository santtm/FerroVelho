#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime

path = f'{os.path.expanduser("~")}/FerroVelho'

telegram_path = f'{path}/database/temp/telegram_'

registro_path = f'{path}/database/persistent/registro.txt'
historico_geral_path = f'{path}/database/persistent/historico_geral.txt'
contabilidade_path = f'{path}/database/persistent/contabilidade.txt'


### ---------------- SQL ---------------- ###
# historico = [('xx-xx-xxx.txt', [__itens__]), ('yy-yy-yyyy.txt', [__itens__])]
# def carrega_historico_individual(whois):
# 	conn = sqlite3.connect('test.db')
# 	cursor = conn.cursor()
# 	arquivo = list(cursor.execute(f'''SELECT * FROM {whois}_HISTORY'''))
# 	historico = []
# 	for nome_arq in arquivos:
# 		with open(f'{path}/database/{whois}/{nome_arq}', 'r') as arq:
# 			historico.append((nome_arq, arq.readlines()))
# 	return _ordena_historico(historico)

# [(xx-xx-xxxx, [(peso,item,valor,hora), (peso,item,valor,hora)]), (yy-yy-yyyy,[('','','','')])]
# def carrega_historico_geral():
# 	conn = sqlite3.connect('test.db')
# 	cursor = conn.cursor()
# 	arquivo = list(cursor.execute('''SELECT * FROM GENERAL_HISTORY'''))
# 	datas = []
# 	for i in arquivo:
# 		data_ = i[0]
# 		if data_ not in datas:
# 			datas.append(data_)
# 	historico = []
# 	for data_ in datas:
# 		historico_data = []
# 		for i in arquivo:
# 			if data_ == i[0]:
# 				# [1:] remove data
# 				historico_data.append(i[1:])
# 		historico.append((data_, historico_data))
# 	return _ordena_historico(historico)

def data():
	return '-'.join(str(datetime.now()).split()[0].split('-')[::-1])

def hora():
	return str(datetime.now()).split()[1][:8]

# arredonda os centavos de 10 em 10
# ex. 1.15 -> 1.10 | 17.3942 -> 17.3
def round_cents(x: float) -> float:
	int_p, dec_p = str(x).split('.')
	return float(f'{int_p}.{dec_p[0]}')

# history[i] = 'weight,name,cash,time'
def session_cash_amount(target_history):
	amount = 0
	history = os.listdir(target_history)
	with open(f'{target_history}/{_ultimo_arquivo(history)}.txt') as h:
		content = h.readlines()
		if content:
			amount = sum([float(i.split(',')[2]) for i in content])
	return round(amount, 2)

### --------------- REGISTRO --------------- ###
def atualiza_registro(ajuste_investimento=0, ajuste_retorno=0):
	
	conteudo_registro = open(registro_path, 'r').readlines()
	
	inv = float(conteudo_registro[0].split(':')[1])
	ret = float(conteudo_registro[1].split(':')[1])

	new_inv = inv + float(ajuste_investimento)
	new_ret = ret + float(ajuste_retorno)

	with open(registro_path, 'w') as r:
		r.write(f'investido:{round(new_inv, 2)}\n')
		r.write(f'retornado:{round(new_ret, 2)}')

	lucro = new_ret-new_inv

	return new_inv, new_ret, lucro


### --- TELEGRAM/CONTABILIDADE/HISTORICOS --- ###

def handle_database_files(nome_usuario, id_venda, material_atual):

	_trash, historico_path = decide_target_history()
		
	with open(contabilidade_path, 'r') as cont:
		contabilidade_content = [i.split(',') for i in cont.readlines()]

	# salva conteudo pro telegram
	with open(f'{telegram_path}{id_venda}.txt', 'w') as tele:
		# salva compra em historico_geral.txt e historico_do_usuario.txt
		with open(historico_geral_path, 'a') as hist_geral:
			with open(historico_path, 'a') as hist:
				for mt in material_atual:
					_data = data()
					_hora = hora()
					hist.write(f'{mt[0]},{mt[1]},{mt[2]},{_hora}\n')
					hist_geral.write(f'{_data},{mt[0]},{mt[1]},{mt[2]},{_hora} {nome_usuario}\n')

					# calcula novo contabilidade.txt
					for i in contabilidade_content:
						if mt[1] in i:
							i[0] = str(round(float(i[0])+mt[0], 2))
							i[2] = str(round(float(i[2])+mt[2], 2))
							inv = i[3]
							i[3] = round(float(inv) + mt[2], 2)

					if mt[1][0]=='*':
						i = contabilidade_content[-1]
						i[0] = str(round(float(i[0])+mt[0], 2))
						i[2] = str(round(float(i[2])+mt[2], 2))
						inv = i[3]
						i[3] = round(float(inv) + mt[2], 2)

					# arquivo de controle para mensagem do telegram
					tele.write(f'{mt[0]},{mt[1]},{mt[2]}\n')

	with open(contabilidade_path, 'w') as gr:
		# corrige \n nas linhas que precisam
		for i in contabilidade_content:
			if '\n' in i[-1]:
				gr.write(f'{i[0]},{i[1]},{i[2]},{i[3]},{i[4]}')
			else:
				gr.write(f'{i[0]},{i[1]},{i[2]},{i[3]},{i[4]}\n')

### --------------- HISTÓRICO --------------- ###
# lista = ['xx-xx-xxxx.txt', 'yy-yy-yyyy.txt']
def _ultimo_arquivo(lista: list) -> str:
	# caso de não ter nenhum arquivo de historico
	if not lista:
		return data()
	# remove .txt
	if lista:
		if '.txt' in lista[0]:
			lista = [i.split('.')[0] for i in lista]
	ano = max([int(i.split('-')[2]) for i in lista])
	previa = [i for i in lista if int(i.split('-')[2]) == ano]
	mes = max([int(i.split('-')[1]) for i in previa])
	previa2 = [i for i in previa if int(i.split('-')[1]) == mes]
	dia = max([int(i.split('-')[0]) for i in previa2])
	if dia<10:
		dia = '0'+str(dia)
	if mes<10:
		mes = '0'+str(mes)
	return f'{dia}-{mes}-{ano}'

# historicos = [('xx-xx-xxx.txt', [__itens__]), ('yy-yy-yyyy.txt', [__itens__])]
def _ordena_historico(historicos: list) -> list:
		# separa as datas dos correspondentes historicos e remove .txt do final
		historico_datas = [i[0].split('.')[0] for i in historicos]
		historico_datas_save = historico_datas.copy()
		historico_ordenado = []
		for i in range(len(historico_datas)):
			ultimo = _ultimo_arquivo(historico_datas)
			if ultimo in historico_datas:
				historico_datas.remove(ultimo)
			historico_ordenado.append(ultimo)
		historico_ordenado = historico_ordenado[::-1]
		historico = [(i, historicos[historico_datas_save.index(i)][1]) for i in historico_ordenado]
		return historico

def decide_target_history():
	files = os.listdir(f'{path}/database/temp')
	if 'D.txt' in files:
		target_history = f'{path}/database/DOUGLAS'
		douglas_history = os.listdir(target_history)
		if 'D_still.txt' in files:
			history_path = f'{path}/database/DOUGLAS/{_ultimo_arquivo(douglas_history)}.txt'
		else:
			history_path = f'{path}/database/DOUGLAS/{data()}.txt'

	elif 'I.txt' in files:
		target_history = f'{path}/database/ITO'
		ito_history = os.listdir(target_history)
		if 'I_still.txt' in files:
			history_path = f'{path}/database/ITO/{_ultimo_arquivo(ito_history)}.txt'
		else:
			history_path = f'{path}/database/ITO/{data()}.txt'

	return target_history, history_path

# historico = [('xx-xx-xxx.txt', [__itens__]), ('yy-yy-yyyy.txt', [__itens__])]
def carrega_historico_individual(whois):
	historico = []
	arquivos = os.listdir(f'{path}/database/{whois}')
	for nome_arq in arquivos:
		with open(f'{path}/database/{whois}/{nome_arq}', 'r') as arq:
			historico.append((nome_arq, arq.readlines()))
	return _ordena_historico(historico)

# ['xx-xx-xxxx,peso,item,valor,hora nome', 'yy-yy-yyyy,peso,item,valor,hora nome']
def carrega_historico_geral():
	arquivo = open(historico_geral_path, 'r').readlines()
	datas = []
	for i in arquivo:
		data = i.split(',')[0]
		if data not in datas:
			datas.append(data)

	historico = []
	for data in datas:
		historico_data = []
		for i in arquivo:
			if data == i.split(',')[0]:
				# i[11:] retira a data da string
				historico_data.append(i[11:])
		historico.append((data, historico_data))

	return _ordena_historico(historico)




def session_cash_amount_DEV(target_history, history_date):
	# material = input('--')
	amount = 0
	with open(f'{target_history}/{history_date}.txt') as h:
		content = h.readlines()
		if content:
			amount = sum([float(i.split(',')[2]) for i in content])
	return round(amount, 2)



def nova_contabilidade_DEV(data):
	material = input('--')
	peso, valor = 0, 0
	with open(historico_geral_path, 'r') as h:
		content = h.readlines()
		for i in content:
			if i.split(',')[0]==data and i.split(',')[2]==material:
				peso += float(i.split(',')[1])
				valor += float(i.split(',')[3])
	
	with open(contabilidade_path, 'r') as cont:
		contabilidade_content = [i.split(',') for i in cont.readlines()]

	for i in contabilidade_content:
		if i[1]==material:
			print(i[0], i[2], i[3])
			i[0] = round(float(i[0])-peso, 2)
			i[2] = round(float(i[2])-valor, 2)
			i[3] = round(float(i[3])-valor, 2)
			print(i[0], i[2], i[3])

	with open(contabilidade_path, 'w') as gr:
		# corrige \n nas linhas que precisam
		for i in contabilidade_content:
			if '\n' in i[-1]:
				gr.write(f'{i[0]},{i[1]},{i[2]},{i[3]},{i[4]}')
			else:
				gr.write(f'{i[0]},{i[1]},{i[2]},{i[3]},{i[4]}\n')


if __name__ == '__main__':
	# while True:
		# nova_contabilidade_DEV('26-10-2022')
	history_date = input('--')
	print(session_cash_amount_DEV(f'{path}/database/DOUGLAS', history_date))