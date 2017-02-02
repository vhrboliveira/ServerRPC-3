from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import psycopg2
import xmlrpclib
from datetime import datetime
import threading


# -------------- Conecta ao Banco de Dados -------------- #
conectarBd = psycopg2.connect("dbname=sakuray user=vitor password=vitor")
#Cursor para operar no Banco
cursor = conectarBd.cursor()
# -------------- Conecta ao Banco de Dados -------------- #


# -------------- Strings para inserir, selecionar e deletar tuplas do Banco de Dados -------------- #
banco_inserir_post = "insert into post (usuario,topico,texto) values (%s,%s,%s)"
banco_inserir_follow = "insert into follow (usuario,topico) values (%s,%s)"
banco_deletar_follow = "delete from follow where usuario = %s and topico = %s"
banco_select_posts = "select usuario,topico,texto from post where datahora >= %s and topico in ( select topico from follow where usuario = %s)"
banco_select_postsTop = "select usuario,topico,texto from post where datahora >= %s and topico in ( select topico from follow where usuario = %s) and topico = %s"
# -------------- Strings para inserir, selecionar e deletar tuplas do Banco de Dados -------------- #

# Informa o id do Servidor para mandar junto com a resposta, assim o cliente sabe qual Servidor atendeu a requiscao
def mandarString():
	return " (servidor " + str(numero) + ")"

# -------------- FUNCOES RPC -------------- #

# O disparador chama essa funcao para saber se o Servidor esta online
def isOn():
	return 1

# Boas vindas hehehe
def sucesso():
	return "Conectado ao Servidor"

# Como usar o blog
def apresentar():
	#Strings para ajudar o usuario
	help1 = " post(@username,#topic,text)     |  follow(@username,#topic)\n"
	help4 = " ----------------------------------------------------------------\n"
	help5 = "\n                          Formato:                     \n"
	help2 = " unsubscribe(@username,#topic)   |  retrievetime(@username,date)\n"
	help3 = " retrievetopic(@username,#topic,date)\n"

	apresenta = "\n        Bem vindo ao Blog RPC, digite quit para sair,\n"
	apresenta2 = "       caso tenha duvidas digite help para saber mais.\n"

	return (apresenta+apresenta2+help5+help4+help1+help2+help3+help4)

#Insere no banco de dados o post do usuario.
def postar(usuario, topico, texto):	
	cursor.execute(banco_inserir_post, (usuario,topico,texto))
	conectarBd.commit()
	return "Postado com sucesso" + mandarString()

#Insere no banco de dados que tal usuario segue tal topico
def seguir(usuario,topico):
	cursor.execute(banco_inserir_follow,(usuario,topico)) #Faz a insercao
	conectarBd.commit()									  #Valida a operacao
	return "Voce esta seguindo o topico " + topico + mandarString()

#Remove do banco de dados um topico que o usuario segue
def parardeSeguir(usuario,topico):
	cursor.execute(banco_deletar_follow, (usuario,topico))
	conectarBd.commit()
	return "Voce parou de seguir o topico "  + topico + mandarString()

#Retorna do banco de dados todos posts feitos a partir de tal data
#Lembrar que sao topico que o usuario segue
def mostrarPost(usuario,datahora):
	cursor.execute(banco_select_posts,(datahora,usuario))
	tuplas = cursor.fetchall()	
	return tuplas

#Retorna do banco de dados todos posts feitos a partir de tal data

#O usuario informa o tipo de topico e ele deve segui-lo
def mostrarPostTop(usuario,topico,datahora):
	cursor.execute(banco_select_postsTop,(datahora,usuario,topico))
	tuplas = cursor.fetchall()
	return tuplas
# -------------- FUNCOES RPC -------------- #


# -------------- Dados do Servidor -------------- #
global porta
porta = input("Porta: ")
global numero
numero = input("id: ")
global ip 
ip = "localhost"
# -------------- Dados do Servidor -------------- #






# -------------- Criar o servidor -------------- #
class ServerThread(threading.Thread):
    def __init__(self):
         threading.Thread.__init__(self)
         self.servidor = SimpleXMLRPCServer((ip,porta))
         self.servidor.register_function(sucesso,"sucesso")
         self.servidor.register_function(apresentar,"apresentar")
         self.servidor.register_function(postar,"postar")
         self.servidor.register_function(isOn,"isOn")
	 self.servidor.register_function(seguir,"seguir")
	 self.servidor.register_function(parardeSeguir,"parardeSeguir")
         self.servidor.register_function(mostrarPost,"mostrarPost")
         self.servidor.register_function(mostrarPostTop,"mostrarPostTop")
         
         print ("Servidor criado na porta", porta)   

    def run(self):
         self.servidor.serve_forever()

server = ServerThread()
server.start()
# -------------- Criar o servidor -------------- #

# -------------- Obter conexao do Disparador -------------- #
portaDis = raw_input("Porta do Disparador: ")
ipDis="localhost"
url = "http://" + ipDis + ":" + portaDis + "/"

disparador =  xmlrpclib.ServerProxy(url)
# -------------- Obter conexao do Disparador -------------- #


a = str (porta)
print(disparador.setInfo(numero,1,ip,a))

entrada = raw_input("-> ")
while(entrada!='asudhasuduas'):
	if(entrada=='quit'):
		print(disparador.quit(numero))
	if(entrada=='info'):
		print(disparador.statusEspelho(numero))

	

	entrada = raw_input("-> ")
