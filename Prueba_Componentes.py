import subprocess
import time
import datetime
import select
import sys

def correr_pruebas():
	
	output = ""
	
	output += ejecutar_comando(["python","./Pruebas/Pruebas_Decodificacion.py"])[1]
	
	output += ejecutar_comando(["python","./Pruebas/Pruebas_Conversor.py"])[1]
	
	output = output.split("\n")

	salida = ""
	for x in output:
		if ("ERROR" in x):
			salida += x+"\n"
	
	return salida	

	
def ejecutar_comando(cmd):

	p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	
	output = ""
	p_timeout = 20 #Tiempo maximo de ejecucion
	q_timeout = 05 #Tiempo maximo sin respuesta por parte del stdout del proceso
	
	tiempo_inicio = time.time()
	
	while True:
		if p.poll() != None: #Se da solo si el proceso termino por si mismo
			for linea in  p.stdout: #Cargo por si quedo salida sin procesar
				output += linea
			break
		
		if (time.time() - tiempo_inicio) > p_timeout: #Se supera el tiempo maximo de ejecucion
			p.terminate()
			for linea in p.stdout: #Esto es seguro porque se forzo el fin del proceso
				output += linea
			
			output += "---TIMEOUT-2---\n"
			break
			
		#Para Unix
		'''
		lista = select.select([p.stdout],[],[],q_timeout)
		
		if lista[0] == []: #Se da si no hay salida para leer, por lo que se supone salto por timeout
			output += "---TIMEOUT-1---\n"
			break
		else:
			output += lista[0][0].readline() #Se puede leer a lo sumo de a una, si se usa un for se puede colgar leyendo continuamente la salida
		'''
		#Para Win
		output += p.stdout.readline()

	return p.returncode, output
	
output = correr_pruebas()
print "Pruebas fallidas: "
print output
raw_input()
