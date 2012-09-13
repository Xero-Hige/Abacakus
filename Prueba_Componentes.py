import subprocess
import time
import datetime

def correr_pruebas():

	p = subprocess.Popen(["python","./Pruebas/Pruebas_Decodificacion.py"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	
	output = p.communicate()[0]
	
	p = subprocess.Popen(["python","./Pruebas/Pruebas_Conversor.py"], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	
	output += p.communicate()[0]
	
	output = output.split("\n")
	
	salida = ""
	for x in output:
		if ("ERROR" in x):
			salida += x+"\n"
	
	return p.returncode, salida
	
ret, output = correr_pruebas()
print "Pruebas fallidas: "
print output
raw_input()
