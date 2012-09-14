import sys
import os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Librerias.Conversor import Conversor

def print_test(nombre,resultado):
	if resultado:
		print nombre + "OK"
	else:
		print nombre + "ERROR"
		
def prueba_decodificar_bpfs():
	c = Conversor()
	
	_comprobar_decodificacion("10000000",-128,c)	
	_comprobar_decodificacion("11111111",-1,c)	
	_comprobar_decodificacion("00000000",0,c)	
	_comprobar_decodificacion("10000001",-127,c)	
	_comprobar_decodificacion("01111111",127,c)
	
def _comprobar_decodificacion(numero,esperado,conversor):
	resultado_esperado = esperado
	resultado = conversor.decodificar_bpfs(numero,len(numero))
	print_test("Prueba conversor decodifica "+numero+" en "+str(resultado_esperado)+":  ",resultado == resultado_esperado)
	
def prueba_codificar_bpfs():
	c = Conversor()
	
	_comprobar_codificacion(-128,"10000000",c)	
	_comprobar_codificacion(-1,"11111111",c)	
	_comprobar_codificacion(0,"00000000",c)	
	_comprobar_codificacion(-127,"10000001",c)	
	_comprobar_codificacion(127,"01111111",c)
	
def _comprobar_codificacion(numero,esperado,conversor):
	resultado_esperado = esperado
	resultado = conversor.codificar_bpfs(numero,len(esperado))
	print_test("Prueba conversor codifica  "+str(numero)+" en "+resultado_esperado+":  ",resultado == resultado_esperado)

if __name__ == "__main__":
	prueba_decodificar_bpfs()
	prueba_codificar_bpfs()
