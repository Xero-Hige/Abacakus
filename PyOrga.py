import argparse

def obtener_argumentos():
	parser = argparse.ArgumentParser(prog='PyOrga')
	
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-v", "--verbose", action="store_true", help="La salida se da por el stdout")
	group.add_argument("-q", "--quiet", action="store_true", help="La salida se da por el archivo de salida estandar")
	
	parser.add_argument("-c","--correr",help = "Corre un script abacus",default="",type=str,dest="script")
	parser.add_argument("-s","--salida",help = "Especifica el archivo de salida estandar",default="salida.out",type=str,dest="salida")
	
	return parser.parse_args()

def main ():
	argumentos = obtener_argumentos()

if __name__ == "__main__":
	main()
