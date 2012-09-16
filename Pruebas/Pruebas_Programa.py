import subprocess
import time
import datetime
import select
import sys
import os

DIRECTORIO_PROGRAMA = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PATH_PROGRAMA = os.path.join(DIRECTORIO_PROGRAMA, 'PyOrga.py')
PATH_CARPETA_SCRIPTS = os.path.join(DIRECTORIO_PROGRAMA, 'Scripts Abbacus')

def print_test(nombre,resultado):
	if resultado:
		print nombre + "OK"
	else:
		print nombre + "ERROR"
		
def ejecutar_comando(cmd):

	p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	
	output = ""
	p_timeout = 60 #Tiempo maximo de ejecucion
	q_timeout = 35 #Tiempo maximo sin respuesta por parte del stdout del proceso
	
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
		
def prueba_correr_suma():
	script = os.path.join(PATH_CARPETA_SCRIPTS, "ejemplo_suma_1.aba")
	cmd = ["python",PATH_PROGRAMA,"-v","-c",script]
	returncode, output = ejecutar_comando(cmd)
	print_test("Correr suma 1: ","600 0005" in output)
	
if __name__ == "__main__":
	prueba_correr_suma()
