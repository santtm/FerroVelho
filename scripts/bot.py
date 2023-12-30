#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time

import requests

from functions import data


chat_id = 1290373266 # sant
# chat_id = -718120799 # grupo ferro velho

token = '5484646285:AAFMpAAlKyUAcj_i9nCTEoqiWeYW4tsnK7k'
send_text_url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=MarkdownV2&text='
# https://api.telegram.org/bot5484646285:AAFMpAAlKyUAcj_i9nCTEoqiWeYW4tsnK7k/sendMessage?chat_id=1290373266&parse_mode=MarkdownV2&text=

expu = os.path.expanduser("~")
path = f'{expu}/FerroVelho/database/temp'
log_path = f'{expu}/FerroVelho/database/log'

def enviar_mensagem(mensagem):
	try:
		send_text = send_text_url + mensagem
		response = requests.get(send_text)
		return response.json()
	except:
		path
		with open(f'{log_path}/sem_internet_{data()}.txt', 'a') as log:
			log.write(mensagem+'\n\n')
		return


def main():

	open(f'{path}/bot_running.txt', 'a').close()
	
	enviar_mensagem('\\=\\=\\= PROGRAMA ABERTO \\=\\=\\=\n')

	while True:

		time.sleep(1)
		arquivos = os.listdir(path)

		# pre_ord e ord ordenam os arquivos telegram_n.txt
		# do menor n até o maior
		pre_ord = []
		ordem = []
		# percorre os arquivos de /database
		for arq in arquivos:
			# acha os arquivos telegram_n.txt
			if arq.split('_')[0]=='telegram':
				# pega só o numero, elimina 'telegram' e '.txt'
				pre_ord.append(int(arq.split('_')[1][:-4]))
		pre_ord = list(set(pre_ord))
		for i in pre_ord:
			ordem.append(f'telegram_{i}.txt')
		
		for arq in ordem:
			# cria uma unica mensagem com todas as infos
			tele = open(f'{path}/{arq}', 'r').readlines()
			mensagem = ''
			for item in tele:
				texto = item.split(',')
				# mensagem precisa do replace para entrar no estilo markdown
				mensagem += f'{texto[0]}kg de {texto[1]} custando {texto[2]}'.replace('.', '\\.').replace('*', '\\*')
			enviar_mensagem(mensagem)
			# remove o arquivo já reportado
			os.remove(f'{path}/{arq}')

		if 'main_running.txt' not in arquivos:
			break

	enviar_mensagem('\\=\\=\\= PROGRAMA FECHADO \\=\\=\\=\n')
	
	os.remove(f'{path}/bot_running.txt')

main()
os._exit(0)
