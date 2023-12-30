#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sqlite3

from PyQt5 import uic, QtGui
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QLabel

from functions import round_cents, data, hora
from functions import session_cash_amount, decide_target_history
from functions import handle_database_files, atualiza_registro


# janela principal do programa onde são realizadas as compras
class MainWindow(QMainWindow):
	
	def __init__(self, *args, **kwargs):

		super(QMainWindow, self).__init__(*args, **kwargs)
		uic.loadUi(ui_path, self)

		self.setWindowIcon(QtGui.QIcon(icon_path))
		# self.resize(800, 500)
		# self.resize(1400, 540)
		self.showMaximized()

		# atalho pra fechar o programa
		####### self.ctrl_nM = QShortcut(QtGui.QKeySequence('Ctrl+w'), self)
		####### self.ctrl_nM.activated.connect(lambda: self.close())

		self.id_venda = 0

		self.tabela_precos = {}
		self.material_atual = []

		self.label_statusBar_nome.setText(nome_usuario)
		self.label_statusBar_gasto.setText(f'GASTOS DO DIA: {session_cash_amount(historico_alvo)}')

		# define foco em lineEdit
		self.lineEdit.setFocus()
		# self.lineEdit.editingFinished.connect(lambda: self.lineEdit.setFocus())
		# self.lineEdit_outro_material.setFocus()
		# self.lineEdit_outro_material.editingFinished.connect(lambda: self.lineEdit_outro_material.setFocus())
		self.lineEdit_outro_material.returnPressed.connect(lambda: self.lineEdit_outro_preco.setFocus())
		self.lineEdit_outro_preco.returnPressed.connect(self.outro_material)

		# conecta remoção de item das listas
		self.listWidget.clicked.connect(self.remove_item_das_listas)
		self.listWidget_2.clicked.connect(self.remove_item_das_listas)
		self.listWidget_3.clicked.connect(self.remove_item_das_listas)

		# conecta todos os botões #
		self.pushButton_outro_ok.clicked.connect(self.outro_material)

		self.pushButton_feito.clicked.connect(self.conclui_compra)
		self.pushButton_cancelar.clicked.connect(self.cancela_compra)

		botoes = [
			self.pushButton,
			self.pushButton_2, self.pushButton_3, self.pushButton_4,
			self.pushButton_5, self.pushButton_6, self.pushButton_7,
			self.pushButton_8, self.pushButton_9, self.pushButton_10,
			self.pushButton_11, self.pushButton_12, self.pushButton_13,
			self.pushButton_14, self.pushButton_15, self.pushButton_16,
			self.pushButton_17, self.pushButton_18, self.pushButton_19,
			self.pushButton_20, self.pushButton_21, self.pushButton_22,
			self.pushButton_23, self.pushButton_24, self.pushButton_25,
			self.pushButton_26, self.pushButton_27, self.pushButton_28,
			self.pushButton_29, self.pushButton_30, self.pushButton_31,
			self.pushButton_32, self.pushButton_33, self.pushButton_34,
			self.pushButton_35, self.pushButton_36, self.pushButton_37,
			self.pushButton_38, self.pushButton_39, self.pushButton_40
		]

		for botao in botoes:
			botao.clicked.connect(self.adiciona_item_as_listas)
			botao.clicked.connect(lambda: self.lineEdit.setFocus())
			self.lineEdit.setFocus()

		self.listWidget.clicked.connect(lambda: self.lineEdit.setFocus())
		self.listWidget_2.clicked.connect(lambda: self.lineEdit.setFocus())
		self.listWidget_3.clicked.connect(lambda: self.lineEdit.setFocus())
		self.pushButton_outro_ok.clicked.connect(lambda: self.lineEdit.setFocus())
		self.pushButton_feito.clicked.connect(lambda: self.lineEdit.setFocus())
		self.pushButton_cancelar.clicked.connect(lambda: self.lineEdit.setFocus())
		###########################

		# carrega tabela de preços #
		try:
			with open(precos_path, 'r') as pr:
				
				p = pr.readlines()

				for i in p:
					self.tabela_precos[i.split(',')[0]] = float(i.split(',')[1])

				erro = []
				# erro de nome incorreto em preco.txt não é detectado direto pelo python
				# vê se todos os nomes dos botões tem um correspondente preço no arquivo
				for botao in botoes:
					if botao.text() not in self.tabela_precos and botao.text():
						erro.append(str(botao.text()))
				# provoca um erro pro programa não ser executado
				if erro:
					raise ValueError(erro)

		except Exception as e:
			
			self.mensagem_erro(f'erro no arquivo precos.txt\n-- {e}')
			
			os.remove(f'{path}/database/temp/main_running.txt')
			os._exit(0)
		############################

		# carrega tool tips (preço do material do botao)
		for botao in botoes:
			botao.setToolTip(str(self.tabela_precos[botao.text()]))
			# botao.setToolTipDelay(500)

	###### def mouseReleaseEvent(self, QMouseEvent):
	######	if QMouseEvent.button() == Qt.RightButton:
	######	self.close()
		
	# fecha o programa se apertar esc
	###### def keyPressEvent(self, keyEvent):
	###### 	super(QMainWindow, self).keyPressEvent(keyEvent)
	###### 	if keyEvent.key() == Qt.Key_Escape:
	###### 		self.close()


	def mensagem_erro(self, erro):
		msgBox = QMessageBox()
		msgBox.setWindowTitle('ERRO')
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText(erro)
		returnValue = msgBox.exec()


	def printa_valores_atuais(self):
		
		valor_atual = 0

		for i in range(len(self.material_atual)):
			valor_atual += self.material_atual[i][2]

		# impede de valores de serem printados como 0
		if valor_atual:
			self.label_valor_total.setText(str(round_cents(valor_atual)))
		else:
			self.label_valor_total.setText('')


	def cancela_compra(self):
		
		self.material_atual = []

		self.listWidget.clear()
		self.listWidget_2.clear()
		self.listWidget_3.clear()

		self.lineEdit.clear()
		self.label_valor_total.setText('')

	
	def remove_item_das_listas(self):

		# detecção de clique nas listas
		_list = [
			self.listWidget.selectedItems(),
			self.listWidget_2.selectedItems(),
			self.listWidget_3.selectedItems()
		]
		# listas
		_list2 = [self.listWidget, self.listWidget_2, self.listWidget_3]
		
		# item de _list não nulo
		_item = [i for i in _list if i][0]

		# localiza lista clicada - qt object	
		_target = _list2[_list.index(_item)]
		# localiza linha clicada
		_row = _target.row(_item[0])

		# remove linha clicada das 3 listas #
		self.listWidget.takeItem(_row)
		self.listWidget_2.takeItem(_row)
		self.listWidget_3.takeItem(_row)

		# deleta item clicado dos materiais atuais com base no indice
		del(self.material_atual[int(_target.indexFromItem(_item[0]).row())])
		
		self.printa_valores_atuais()

		# limpa seleção das listas - barra azul em cima da lista selecionada #
		for i in range(self.listWidget.count()):
			for j in _list2:
				j.clearSelection()


	def adiciona_item_as_listas(self):

		try:
			# verifica entrada do usuário ao tentar converte-la para float
			_kg_material = float(self.lineEdit.text().replace(',', '.'))
			# pega nome do botão clicado
			_material = self.sender().text()

			# verifica se o botão tem informação atrelada 
			if _material:
				_valor = _kg_material*self.tabela_precos[_material]
			else:
				raise Exception('botão sem material atrelado')

			self.material_atual.append((_kg_material, _material, round(_valor, 2)))

			# adiciona itens às listas
			self.listWidget.addItem(str(_kg_material))
			self.listWidget_2.addItem(_material) 
			self.listWidget_3.addItem(str(round(_valor, 2)))

			self.lineEdit.clear()

			self.printa_valores_atuais()
		
		except Exception as e:
			self.lineEdit.clear()
			self.mensagem_erro('escreva apenas números como peso do material\n' + str(e))


	def outro_material(self):
		
		try:
			_material = self.lineEdit_outro_material.text().upper()
			_kg_material = float(self.lineEdit.text().replace(',', '.'))

			if _material:
				_material = '*' + self.lineEdit_outro_material.text()
			else:
				raise Exception('escreva nome do material')

			_preco = float(self.lineEdit_outro_preco.text().replace(',', '.'))

			_valor = _kg_material*_preco

			self.material_atual.append((_kg_material, _material, round(_valor, 2)))

			# adiciona itens às listas
			self.listWidget.addItem(str(_kg_material))
			self.listWidget_2.addItem(_material) 
			self.listWidget_3.addItem(str(round_cents(_valor)))

			self.lineEdit.clear()
			self.lineEdit_outro_material.clear()
			self.lineEdit_outro_preco.clear()

			self.printa_valores_atuais()

		except Exception as e:
			self.mensagem_erro('erro no preço ou peso do material\n'+str(e))


	def conclui_compra(self):

		if self.label_valor_total.text():
			atualiza_registro(ajuste_investimento=self.label_valor_total.text())

		# telegram, historico geral, historico individual, contabilidade
		handle_database_files(nome_usuario, self.id_venda, self.material_atual)

		self.id_venda += 1
		self.material_atual = []

		self.label_statusBar_idVenda.setText(f'COMPRAS REALIZADAS: {self.id_venda}')
		self.label_statusBar_ultimoValor.setText(f'VALOR DA COMPRA ANTERIOR: {self.label_valor_total.text()}')

		self.label_statusBar_gasto.setText(f'GASTOS DO DIA: {session_cash_amount(historico_alvo)}')

		self.lineEdit.clear()

		self.listWidget.clear()
		self.listWidget_2.clear()
		self.listWidget_3.clear()

		self.label_valor_total.setText('')

		## -- backup -- ##
		if self.id_venda % 15 == 0:
			os.system(f'cp -r {path}/database {path}/backups/{data()}_{self.id_venda//15}')


# tela final em que o usuario escolhe se continuará na mesma sessão
# da proxima vez que entrar, ou se vai mudar de sessão
# sessão é o histórico ao qual vai ser destinado as compras
# e o dia de trabalho
class ChangeUser(QMainWindow):
	
	def __init__(self, *args, **kwargs):

		super(QMainWindow, self).__init__(*args, **kwargs)
		uic.loadUi(change_user_path, self)

		self.setWindowIcon(QtGui.QIcon(icon_path))

		self.setFixedSize(372, 190)

		# usuario muda sessao
		self.pushButton.clicked.connect(self.still_remove)
		# usuario continua
		self.pushButton_2.clicked.connect(self.still_add)

	def caixa_da_sessao(self):
		caixa = session_cash_amount(historico_alvo)
		msgBox = QMessageBox()
		msgBox.setText(f'gastos do dia encerrado em: {caixa}')
		returnValue = msgBox.exec()

	def still_remove(self):
		arquivos = os.listdir(f'{path}/database/temp')
		if f'{nome_usuario[0]}_still.txt' in arquivos:
			os.remove(f'{path}/database/temp/{nome_usuario[0]}_still.txt')
		self.caixa_da_sessao()
		self.close()

	def still_add(self):
		# nao tem necessidade de abrir still dnv, mas por segurança é feito
		open(f'{path}/database/temp/{nome_usuario[0]}_still.txt', 'a').close()
		self.close()
	
	def closeEvent(self, event: QtGui.QCloseEvent):
		# checa se um dos botoes sim ou nao enviaram o sinal
		if self.sender():
			event.accept()
		# bloqueia o fechamento caso o botao x tenha enviado o sinal
		else:
			event.ignore()
	
	def changeEvent(self, event):
		if event.type() == QEvent.WindowStateChange:
			if self.windowState() & Qt.WindowMinimized:
				self.activateWindow()


path = f'{os.path.expanduser("~")}/FerroVelho'
arquivos = os.listdir(f'{path}/database/temp')

ui_path = f'{path}/resources/MainWindow.ui'
change_user_path = f'{path}/resources/LastPage.ui'
icon_path = f'{path}/resources/icons/icon.png'

precos_path = f'{path}/database/persistent/precos.txt'
historico_geral_path = f'{path}/database/persistent/historico_geral.txt'

main_running_path = f'{path}/database/temp/main_running.txt'

historico_alvo, historico_path = decide_target_history()

nome_usuario = historico_alvo.split('/')[-1]

# criar running.txt e historicos
open(main_running_path, 'a').close()
open(historico_path, 'a').close()
open(historico_geral_path, 'a').close()

app = QApplication([])
window = MainWindow()
window.show()
app.exec()

change_user_app = QApplication([])
change_user_window = ChangeUser()
change_user_window.show()
change_user_app.exec()

os.remove(f'{path}/database/temp/main_running.txt')
os.remove(f'{path}/database/temp/{nome_usuario[0]}.txt')
os._exit(0)
