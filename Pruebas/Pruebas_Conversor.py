import sys
import os
sys.path.insert(0,os.path.join(__file__, '..', '..'))

from Librerias.Conversor import Conversor as Conversor

def print_test(nombre,resultado):
	if resultado:
		print nombre + "OK"
	else:
		print nombre + "ERROR"
		
def prueba_convertir_hexa_decimal():
	c = Conversor()
	
	_comprobar_conversion("1",1,c)


def _comprobar_conversion_hexa_decimal(numero,esperado,conversor):
	resultado_esperado = esperado
	resultado = conversor.hexa_a_decimal(numero)
	print_test("Prueba conversor decodifica "+numero+" en "+str(resultado_esperado)+":  ",resultado == str(resultado_esperado))

		
if __name__ == "__main__":
	pass
