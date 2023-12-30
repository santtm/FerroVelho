# Import module
import sqlite3
  
conn = sqlite3.connect('test.db')

cursor = conn.cursor()
  
# table = """
# CREATE TABLE DOUGLAS_HISTORY(PESO VARCHAR(255),
# ITEM VARCHAR(255), PREÇO VARCHAR(255), HORA VARCHAR(255));
# """

# cursor.execute(table)

# ['xx-xx-xxxx,peso,item,valor,hora', 'yy-yy-yyyy,peso,item,valor,hora']
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
# 	return historico

# cursor.execute('''INSERT INTO ITO_HISTORY VALUES ('1.0','HD','100.0','21:52:02')''')

# conn.commit()

print(list(cursor.execute('''SELECT * FROM ITO_HISTORY''')))

conn.close()