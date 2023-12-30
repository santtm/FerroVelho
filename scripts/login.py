#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from sys import argv

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtWidgets import QApplication, QTableWidgetItem

from functions import atualiza_registro
from functions import carrega_historico_geral, carrega_historico_individual


class MainWindow(QMainWindow):
	
	def __init__(self, *args, **kwargs):

		super(QMainWindow, self).__init__(*args, **kwargs)
		uic.loadUi(login_page_path, self)

		self.setWindowIcon(QtGui.QIcon(icon_path))

		self.pushButton.clicked.connect(self.douglas)
		self.pushButton_2.clicked.connect(self.ito)
		self.pushButton_3.clicked.connect(self.admin)

		self.lineEdit.setFocus()
		self.lineEdit.editingFinished.connect(lambda: self.lineEdit.setFocus())
		self.lineEdit.returnPressed.connect(self.admin)

	def douglas(self):
		global escolheu_um_usuario
		escolheu_um_usuario = True
		open(f'{path}/database/temp/D.txt', 'a').close()
		self.close()

	def ito(self):
		global escolheu_um_usuario
		escolheu_um_usuario = True
		open(f'{path}/database/temp/I.txt', 'a').close()
		self.close()

	def admin(self):
		if self.lineEdit.text() == 'spike999':
			global escolheu_um_usuario
			escolheu_um_usuario = 'admin'
			self.close()


class Administrador(QMainWindow):
	
	def __init__(self, *args, **kwargs):
		
		super(QMainWindow, self).__init__(*args, **kwargs)
		uic.loadUi(admin_page_path, self)

		self.setWindowIcon(QtGui.QIcon(icon_path))

		self.setFixedSize(900, 480)

		self.stackedWidget.setCurrentWidget(self.historico_page)

		self.pushButton_login_ito.clicked.connect(self.ito)
		self.pushButton_login_douglas.clicked.connect(self.douglas)

		# conecta coisas relacionadas ao historico #
		self.historicos = {}
		self.botoes_historico = [self.ITO, self.DOUGLAS, self.GERAL]
		self.botoes_menu = [
			self.pushButton_historico, self.pushButton_contabilidade, self.pushButton_precos
			]

		self.DOUGLAS.clicked.connect(self.visualizar_historico)
		self.ITO.clicked.connect(self.visualizar_historico)
		self.GERAL.clicked.connect(self.visualizar_historico)

		self.pushButton_historico.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.historico_page))
		self.pushButton_historico.clicked.connect(lambda: self.check_n_uncheck(self.botoes_menu))
		############################################

		# conecta coisas relacionadas a contabilidade #
		self.pushButton_contabilidade.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.contabilidade_page))
		self.pushButton_contabilidade.clicked.connect(lambda: self.lineEdit_contabilidade_peso.setFocus())
		self.pushButton_contabilidade.clicked.connect(lambda: self.check_n_uncheck(self.botoes_menu))
		self.pushButton_contabilidade.clicked.connect(self.contabilidade)
		
		self.pushButton_contabilidade_ok.clicked.connect(self.contabilidade)
		self.pushButton_contabilidade_limpar.clicked.connect(self.limpar)

		self.lineEdit_contabilidade_peso.returnPressed.connect(lambda: self.lineEdit_contabilidade_material.setFocus())
		self.lineEdit_contabilidade_material.returnPressed.connect(lambda: self.lineEdit_contabilidade_valor.setFocus())
		self.lineEdit_contabilidade_valor.returnPressed.connect(self.contabilidade)
		###############################################

		# conecta coisas relacionadas a preços #
		self.pushButton_precos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.precos_page))
		self.pushButton_precos.clicked.connect(lambda: self.lineEdit_precos_material.setFocus())
		self.pushButton_precos.clicked.connect(lambda: self.check_n_uncheck(self.botoes_menu))
		self.pushButton_precos.clicked.connect(self.precos)

		self.pushButton_precos_limpar.clicked.connect(self.limpar2)
		self.pushButton_precos_ok.clicked.connect(self.precos)

		self.lineEdit_precos_material.returnPressed.connect(lambda: self.lineEdit_precos_novo_preco.setFocus())
		self.lineEdit_precos_novo_preco.returnPressed.connect(self.precos)
		########################################

	def douglas(self):
		global escolheu_um_usuario
		escolheu_um_usuario = True
		open(f'{path}/database/temp/D.txt', 'a').close()
		self.close()

	def ito(self):
		global escolheu_um_usuario
		escolheu_um_usuario = True
		open(f'{path}/database/temp/I.txt', 'a').close()
		self.close()

	# deixa selecionado o botão que vc clicou
	# e tira a seleção dos outros
	def check_n_uncheck(self, botoes):
		for i in botoes:
			if i != self.sender():
				i.setChecked(False)
		self.sender().setChecked(True)

	def limpar(self):
		self.lineEdit_contabilidade_peso.clear()
		self.lineEdit_contabilidade_material.clear()
		self.lineEdit_contabilidade_valor.clear()
		self.lineEdit_contabilidade_peso.setFocus()

	def limpar2(self):
		self.lineEdit_precos_material.clear()
		self.lineEdit_precos_novo_preco.clear()
		self.lineEdit_precos_material.setFocus()

	def mensagem_erro(self, erro):
		msgBox = QMessageBox()
		msgBox.setWindowTitle('ERRO')
		msgBox.setText(erro)
		msgBox.setStandardButtons(QMessageBox.Ok)
		x = msgBox.exec()

	def mensagem_confirma(self, texto):
		msgBox = QMessageBox()
		msgBox.setWindowTitle('CONFIRMA')
		msgBox.setText(texto)		
		msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.No)
		return msgBox.exec()


	def visualizar_historico(self):

		self.check_n_uncheck(self.botoes_historico)

		# carregar os 3 historicos de uma vez e salva
		if not self.historicos:
			self.historicos['ITO'] = carrega_historico_individual('ITO')
			self.historicos['DOUGLAS'] = carrega_historico_individual('DOUGLAS')
			self.historicos['GERAL'] = carrega_historico_geral()

		# if self.sender().text() == 'GERAL' and self.vazio:
			# self.mensagem_erro('Sem conteúdo no histórico geral')

		# dicionario self.historicos puxa o historico
		# de acordo com o botao apertado
		historico = self.historicos[self.sender().text()]
		
		# exemplo de historico
		# [('03-10-2022', []), ('04-10-2022', ['1.0,HD,100.0,09:21:06\n', '1.0,PVC,100.0,10:35:14\n'])]
		# [(xx-xx-xxxx, [(peso,item,valor,hora), (peso,item,valor,hora)]), (yy-yy-yyyy,[('','','','')])]

		tamanho_historico = 0
		for i in historico:
			# caso o historico do dia seja vazio, corrige a contagem
			if not len(i[1]):
				tamanho_historico += 1
			else:
				tamanho_historico += len(i[1])

		self.tableWidget_historico.setRowCount(tamanho_historico)
		
		dinheiro_total = 0

		previous_row = -1
		for data in historico:
			# data[0] = data da sessão
			# data[1] lista de itens comprados
			if not data[1]:
				previous_row += 1
				self.tableWidget_historico.setItem(previous_row, 0, QTableWidgetItem(data[0]))
				
				for j in range(1, 5):
					self.tableWidget_historico.setItem(previous_row, j, QTableWidgetItem(''))

			for item in data[1]:
				previous_row += 1
				self.tableWidget_historico.setItem(previous_row, 0, QTableWidgetItem(data[0]))

				item = item.split(',')
				if item[2]:
					dinheiro_total += float(item[2])

				# cada j é um atributo da compra
				# respectivamente, peso, nome, preço, hora
				for j in item:
					self.tableWidget_historico.setItem(previous_row, item.index(j)+1, QTableWidgetItem(j))

		self.label_historico_total.setText(str(round(dinheiro_total, 2)))


	def contabilidade(self):
		
		valor_total = 0
		ajuste_de_retorno = 0
		with open(contabilidade_path, 'r') as cont:
			
			conteudo = cont.readlines()
		
		# checar se o nome do material ta la
		# if checa se quem pediu a mudança na tabela foi o botão OK
		# ou o lineEdit
		if self.sender().text() != 'CONTABILIDADE':
			peso_vendido = self.lineEdit_contabilidade_peso.text()
			material = self.lineEdit_contabilidade_material.text().upper()
			valor_venda = self.lineEdit_contabilidade_valor.text()

			try:
				if peso_vendido!='tudo':
					peso_vendido = float(peso_vendido)
				valor_venda  = float(valor_venda)
			except:
				self.mensagem_erro('peso ou valor passado incorretamente')
				peso_vendido = 0
				valor_venda = 0

			if not all([peso_vendido, material, valor_venda]):
				self.mensagem_erro('ficou faltando alguma informação')
			else:
				achou_material = False
				for i in conteudo:
					if material==i.split(',')[1]:
						achou_material = True
						info = conteudo[conteudo.index(i)].split(',')
						peso_antigo = float(info[0])
						valor_antigo = float(info[2])
						if peso_vendido=='tudo':
							peso_vendido = peso_antigo
						if peso_antigo<peso_vendido:
							self.mensagem_erro('peso informado é maior que peso contido no estoque')
						else:
							novo_peso = round(peso_antigo-peso_vendido, 2)
							novo_valor = round(peso_vendido*valor_venda - valor_antigo, 2)
							
							if novo_valor>=0 and novo_peso>=0:
								estado = 'lucro'
								novo_valor_table = 0
							elif novo_valor<0 and novo_peso==0:
								estado = 'prejuízo'
								novo_valor_table = -novo_valor
							# caso
							elif novo_valor<0 and peso_antigo>0:
								estado = ''
								novo_valor_table = -novo_valor
							
							if estado:
								x = self.mensagem_confirma(f'deseja realizar operação?\n{peso_vendido}kg de {material} a {valor_venda} reais o kg\n{estado} de {abs(novo_valor)} reais')
							else:
								x = self.mensagem_confirma(f'deseja realizar operação?\n{peso_vendido}kg de {material} a {valor_venda} reais o kg')

							if x == QMessageBox.Ok:
								ajuste_de_retorno = round(valor_venda*peso_vendido, 2)
								invest = i.split(',')[3]
								new_ret = round(float(i.split(',')[4]) + ajuste_de_retorno, 2)
								conteudo[conteudo.index(i)] = f'{novo_peso},{material},{novo_valor_table},{invest},{new_ret}\n'
								
								# atualiza contabilidade.txt
								with open(contabilidade_path, 'w') as cont:
									for i in conteudo:
										cont.write(i)

								self.lineEdit_contabilidade_material.clear()
								self.lineEdit_contabilidade_peso.clear()
								self.lineEdit_contabilidade_valor.clear()

								self.lineEdit_contabilidade_peso.setFocus()
							else:
								# print('else')
								pass
				if not achou_material:
					self.mensagem_erro('material não encontrado')

		self.tableWidget_contabilidade.setRowCount(len(conteudo))
		
		for i in conteudo:
			valor_total += float(i.split(',')[2])

			index_j = 0
			for j in i.split(','):
				self.tableWidget_contabilidade.setItem(
					conteudo.index(i), index_j, QTableWidgetItem(j)
					)
				index_j += 1

		# printa os valores da contabilidade #
		self.label_5.setText(str(round(valor_total, 2)))

		inv, ret, lucro = atualiza_registro(ajuste_retorno=ajuste_de_retorno)

		self.label_contabilidade_investido.setText(str(inv))
		self.label_contabilidade_retornado.setText(str(ret))
		
		if lucro<0:
			self.label_contabilidade_lucro.setText(str(lucro))
			self.label_contabilidade_lucro.setStyleSheet('color: rgb(239, 41, 41)')
		else:
			self.label_contabilidade_lucro.setText('+' + str(lucro))
			self.label_contabilidade_lucro.setStyleSheet('color: rgb(138, 226, 52)')
		######################################


	def precos(self):

		self.lineEdit_precos_material.setFocus()

		# checa se o usuario só ta entrando na pagina preços
		# ou se ta pedindo pra mudar algum preço
		if self.sender().text() != 'PREÇOS':
			material = ' '.join(self.lineEdit_precos_material.text().upper().split())
			novo_preco = self.lineEdit_precos_novo_preco.text().replace(',', '.')
			
			try:
				novo_preco = float(novo_preco)

				if not material:
					self.mensagem_erro('faltou passar o nome do material')
				else:
					encontrou_material = False
					for i in tabela_precos:
						if material == i.split(',')[0]:
							encontrou_material = True
							preco_antigo = float(i.split(',')[1])
							if novo_preco == preco_antigo:
								self.mensagem_erro('novo preço igual a preço antigo')
							else:
								msg = QMessageBox()
								msg.setText(f'deseja realizar operação?\n{material} de {preco_antigo} para {novo_preco}')
								msg.setStandardButtons(QMessageBox.Ok | QMessageBox.No)
								x = msg.exec()
								if x == QMessageBox.Ok:
									tabela_precos[tabela_precos.index(i)] = f'{material},{novo_preco}\n'
									with open(precos_path, 'w') as p:
										for item in tabela_precos:
											p.write(item)

									self.lineEdit_precos_material.clear()
									self.lineEdit_precos_novo_preco.clear()
									self.lineEdit_precos_material.setFocus()
								else:
									# print('else')
									pass

					if not encontrou_material:
						self.mensagem_erro('material não encontrado')
			except:
				self.mensagem_erro('novo preço foi passado errado\ntente escrevendo apenas números e ponto ou vírgula')
				novo_preco = 0

		self.tableWidget_precos.setRowCount(len(tabela_precos))
		for i in tabela_precos:
			for j in i.split(','):
				self.tableWidget_precos.setItem(
					tabela_precos.index(i), i.split(',').index(j), QTableWidgetItem(j)
					)


path = f'{os.path.expanduser("~")}/FerroVelho'

# scpipts
bat_path = f'{path}/scripts/main.bat'

# recursos .ui e .png
login_page_path = f'{path}/resources/LoginPage.ui'
admin_page_path = f'{path}/resources/AdminPage.ui'
icon_path = f'{path}/resources/icons/icon.png'

# arquivos de texto
precos_path = f'{path}/database/persistent/precos.txt'
contabilidade_path = f'{path}/database/persistent/contabilidade.txt'

# decide se vai para página de compras
# ou página do admin
escolheu_um_usuario = False


# limpa lixo de testes mal sucedidos
arg = argv[-1]
if arg == '-c':
	arq = os.listdir(f'{path}/database/temp')
	for i in arq:
		# if 'running' in i:
		os.remove(f'{path}/database/temp/{i}')


# não é interessante ter dois main.py, login.py e bot.py
# rodando simultaneamente
# só precisamos procurar autorização de login e bot
# pois main sempre encerra antes de bot
arquivos = os.listdir(f'{path}/database/temp')
if 'admin_running.txt' not in arquivos:
	open(f'{path}/database/temp/admin_running.txt', 'a').close()
	while True:
		arquivos = os.listdir(f'{path}/database/temp')
		if 'bot_running.txt' not in arquivos and 'telegram' not in [i.split('_')[0] for i in arquivos]:
			break

	# carrega tela de login
	login_app = QApplication([])
	login_window = MainWindow()
	login_window.show()
	login_app.exec()

	if escolheu_um_usuario == True:
		os.system(bat_path)
	elif escolheu_um_usuario == 'admin':

		with open(precos_path, 'r') as p:
			tabela_precos = p.readlines()

		# carrega tela do admin
		admin_app = QApplication([])
		admin_window = Administrador()
		admin_window.show()
		admin_app.exec()

		if escolheu_um_usuario == True:
			os.system(bat_path)

	os.remove(f'{path}/database/temp/admin_running.txt')

os._exit(0)
