from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import xmlrpclib
from datetime import datetime
import threading

# ---------------------------- VARIAVEIS ---------------------------- #
global ip
global porta

# Quantidade de requisicoes atendias por cada servidor
global qnt1
global qnt2

qnt1 = 0
qnt2 = 0
# ---------------------------- VARIAVEIS ---------------------------- #

# ---------------------------- FUNCOES "PRIVADAS" ---------------------------- #
# Cria as variaveis que definem o status dos Servidores
def criarVariaveis():	
	global s1status	
	global s2status
	s1status = 0
	s2status = 0

# Mostra quais servidores estao online
def status():
	texto=""

	if s1status==1:
		texto = "Servidor 1 esta online e "
	else: texto = "Servidor 1 esta offline e "

	if s2status==1:
		texto = texto + "Servidor 2 esta online"
	else: texto = texto + "Servidor 2 esta offline"

	return texto

# Faz a conexao RPC com o Servidor 1 na variavel s1
def definirS1(ip,porta):
	global s1status
	global s1
	s1status = 1
	url = "http://" + ip + ":" + porta + "/"
	s1 =  xmlrpclib.ServerProxy(url)
	

# Faz a conexao RPC com o Servidor 2 na variavel s2
def definirS2(ip,porta):
	global s2status	
	global s2
	s2status = 1
	url = "http://" + ip + ":" + porta + "/"
	s2 =  xmlrpclib.ServerProxy(url)


#Testar conexao com o servidor
def testarConexao1():
	try:
		s1.apresentar()
	except:
		print("Ouve um erro no Servidor 1")
		encerrarServidor(1)
		return 0
	else:
		print("Nao ouve erro no Servidor 1")
		return 1
	

def testarConexao2():
	try:
		s2.apresentar()
	except:
		print("Ouve um erro no Servidor 2")
		encerrarServidor(2)
		return 0
	else:
		print("Nao ouve erro no Servidor 2")
		return 1


	
# ---------------------------- FUNCOES "PRIVADAS" ---------------------------- #

# ---------------------------- FUNCOES RPC ---------------------------- #

# Servidor avisa que vai ficar off
def encerrarServidor(serv):
	if serv==1:
		global s1
		global s1status
		s1status = 0

	if serv==2:
		global s2
		global s2status
		s2status = 0

	return ""

# Boas vindas hehe
def sucesso():
	return "Conectado ao Disparador"

# Definir cada servidor e sua situacao
def setInfo(ide,status,ip,porta):
	if ide==1 and status==1:
		definirS1(ip,porta)
		print("Conectado ao Servidor 1")
		return "Disparador sabe que esta online"

	if  ide==2 and status==1:
		definirS2(ip,porta)
		print("Conectado ao Servidor 2")
		return "Disparador sabe que esta online"

# Informar a situacao do outro Servidor quando um Servidor pedir
def outroServidor(serv):

	texto1 = ""
	texto2 = ""

	if s1status==1:
		texto1 = "O outro Servidor esta online"
	else: texto1 = "O outro Servidor esta offline"

	if s2status==1:
		texto2 = "O outro Servidor esta online"
	else: texto2 = "O outro Servidor esta offline"

	if serv==1:
		return texto2
	else: return texto1

# Enumerar quantidade de requisicoes atendidas por cada servidor, se tiver somente um o nenhum a contagem para.
def incrementar(serv):
	if serv == 2:
		copia = qnt2
		global qnt2
		qnt2 = copia + 1
	elif serv == 1:
		copia = qnt1
		global qnt1
		qnt1 = copia + 1


def postar(usuario,topico,texto):

	global s1status
	s1status = testarConexao1()
	global s2status
	s2status = testarConexao2()	

	#Caso os dois servidores estejam online
	if s1status == 1 and s2status==1:
		if qnt1 > qnt2:
			incrementar(2)
			return s2.postar(usuario,topico,texto)
		else:
			incrementar(1)
			return s1.postar(usuario,topico,texto)

	elif s1status == 1 and s2status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s1.postar(usuario,topico,texto)
	elif s2status == 1 and s1status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s2.postar(usuario,topico,texto)
	else: return "Nenhum Servidor esta Online"
	

def apresentar():
	if s1status == 1 and s2status==1:
		if qnt1 > qnt2:
			incrementar(2)
			return s2.apresentar()
		else:
			incrementar(1)
			return s1.apresentar()

	elif s1status == 1 and s2status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s1.apresentar()
	elif s2status == 1 and s1status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s2.apresentar()
	else: return "Nenhum Servidor esta Online"

def seguir(usuario,topico):

	global s1status
	s1status = testarConexao1()
	global s2status
	s2status = testarConexao2()	

	#Caso os dois servidores estejam online
	if s1status == 1 and s2status==1:
		if qnt1 > qnt2:
			incrementar(2)
			return s2.seguir(usuario,topico)
		else:
			incrementar(1)
			return s1.seguir(usuario,topico)

	elif s1status == 1 and s2status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s1.seguir(usuario,topico)
	elif s2status == 1 and s1status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s2.seguir(usuario,topico)
	else: return "Nenhum Servidor esta Online"

def parardeSeguir(usuario,topico):

	global s1status
	s1status = testarConexao1()
	global s2status
	s2status = testarConexao2()	

	#Caso os dois servidores estejam online
	if s1status == 1 and s2status==1:
		if qnt1 > qnt2:
			incrementar(2)
			return s2.parardeSeguir(usuario,topico)
		else:
			incrementar(1)
			return s1.parardeSeguir(usuario,topico)

	elif s1status == 1 and s2status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s1.parardeSeguir(usuario,topico)
	elif s2status == 1 and s1status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s2.parardeSeguir(usuario,topico)
	else: return "Nenhum Servidor esta Online"

def mostrarPost(usuario,datahora):

	global s1status
	s1status = testarConexao1()
	global s2status
	s2status = testarConexao2()	

	#Caso os dois servidores estejam online
	if s1status == 1 and s2status==1:
		if qnt1 > qnt2:
			incrementar(2)
			return s2.mostrarPost(usuario,datahora)
		else:
			incrementar(1)
			return s1.mostrarPost(usuario,datahora)

	elif s1status == 1 and s2status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s1.mostrarPost(usuario,datahora)
	elif s2status == 1 and s1status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s2.mostrarPost(usuario,datahora)
	else: return "Nenhum Servidor esta Online"

def mostrarPostTop(usuario,topico,datahora):

	global s1status
	s1status = testarConexao1()
	global s2status
	s2status = testarConexao2()	

	#Caso os dois servidores estejam online
	if s1status == 1 and s2status==1:
		if qnt1 > qnt2:
			incrementar(2)
			return s2.mostrarPostTop(usuario,topico,datahora)
		else:
			incrementar(1)
			return s1.mostrarPostTop(usuario,topico,datahora)

	elif s1status == 1 and s2status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s1.mostrarPostTop(usuario,topico,datahora)
	elif s2status == 1 and s1status!=1:
		# Nao incrementar, pois qnd um servidor voltar deve-se manter o valor antigo
		return s2.mostrarPostTop(usuario,topico,datahora)
	else: return "Nenhum Servidor esta Online"







# ---------------------------- FUNCOES RPC ---------------------------- #

ip = "localhost"
porta = input("Porta: ")

# -------------- Criar o Disparador -------------- #
class ServerThread(threading.Thread):
    def __init__(self):
         threading.Thread.__init__(self)
         self.disparador = SimpleXMLRPCServer((ip,porta))
         self.disparador.register_function(sucesso,"sucesso") #just return a string
         self.disparador.register_function(setInfo,"setInfo")
         self.disparador.register_function(encerrarServidor,"quit")
         self.disparador.register_function(outroServidor,"statusEspelho")
         self.disparador.register_function(postar,"postar")
       	 self.disparador.register_function(apresentar,"apresentar")
	 self.disparador.register_function(seguir,"seguir")
	 self.disparador.register_function(parardeSeguir,"parardeSeguir")
         self.disparador.register_function(mostrarPost,"mostrarPost")
         self.disparador.register_function(mostrarPostTop,"mostrarPostTop")
         print ("Disparador criado na porta", porta)   

    def run(self):
         self.disparador.serve_forever()

disp = ServerThread()
disp.start()
# -------------- Criar o Disparador -------------- #

criarVariaveis()


# -------------- Prompt Disparador -------------- #
entrada = raw_input("-> ")
while(entrada!='sadasuhduash'):
	if entrada=='info':
		testarConexao1()
		testarConexao2()
		print(status())
	


	entrada = raw_input("-> ")
# -------------- Prompt Disparador -------------- #




