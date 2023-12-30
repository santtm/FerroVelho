++++++                         ARQUIVOS                         ++++++

+++ permanentes +++

'precos.txt' tem uma tabela de preços dos materiais no formato
	material 1,100
	material 2,150
	etc
	em que o nome do material vem antes da virgula
	e o preço vem depois

+++ temporarios +++

tanto 'I.txt' quanto 'D.txt' indicam quem vai rodar o programa
	ito e douglas respectivamente

'main_runnning.txt' é um meio de comunicação entre (I) e (II)
	pois é o jeito de (I) avisar pra (II) que parou de rodar, pra
	(II) parar também
	
'admin_running.txt' é o jeito de (III) se comunicar consigo mesmo
	impedindo dois (III) executarem simultaneamente
	
'bot_runnning.txt' é um meio de comunicação entre (II) e (III)
	pois é o jeito de (II) registrar que parou de rodar
	permitindo a execução de um novo (III)
		isso impede de dois (II) e (I) rodarem simultaneamente

'telegram_n.txt' é provavelmente a forma mais
	satisfatória de enviar as informações pelo telegram
	
	se (II) fosse executado dentro de (I) ao invés de
	paralelamente (e trocando informações via txt),
	(II) consumiria todo o processamento alocado pra (I)
	congelando o app enquanto as mensagens não fossem enviadas

	rodando (II) independentemente faz o linux alocar
	processamentos diferentes pros dois scripts, então nenhum
	congela o outro

++++++                             main (I)                             ++++++

+++ reconhecimento de usuário +++

procura-se pelo arquivo 'D.txt' no diretório /flow, caso estiver lá
	lista-se os arquivos de /flow/DOUGLAS
	se o arquivo 'still.txt' for encontrado, o histórico correspondente
	a essa sessão é o último histórico disponível (ordenado por data)
	caso não for encontrado, gera-se um novo histórico com o nome
	data_de_hoje.txt
	
	ao fechar o app é perguntado se o usuário vai mudar de sessão
	se selecionar 'sim', o caixa do dia é mostrado e o arquivo 'still.txt'
	é apagado
	caso for ecolhido 'não' o app apenas fecha
	
++++++                             bot (II)                             ++++++

ao inicio da exeução é criado 'bot_running.txt' e ao final dela esse
	arquivo é excluído

o programa roda em looping
	listando todos os arquivos presentes no diretório /FerroVelho/flow/

caso o arquivo 'main_running.txt' for um destes, ele continua rodando
	caso contrário ele encerra sua execução

se for detectado algum arquivo com início 'telegram'
	todo seu conteúdo é enviado pelo telegram para a conta pré configurada,
	depois o arquivo é apagado

os arquivos com início 'telegram' são 'telegram_n.txt'
	em que n representa a enésima compra feita pelo app

	ex. depois da compra 14 é gerado o arquivo 'telegram_14.txt'
		com todo o conteúdo da compra
		depois da compra 15 é gerado o arquivo 'telegram_15.txt'
		com todo o conteúdo da compra
		etc
		
++++++                             login (III)                             ++++++
