

class Conversor(object):
	"""Conversor de numeros"""

	TABLA_HEXA = { "0":0 , "1": 1 , "2":2 , "3":3 , "4":4 ,
				   "5":5 , "6":6 , "7":7 , "8":8 , "9":9 ,
				   "A":10, "B":11 ,"C":12 ,"D":13,"E":14,"F":15}
				
	TABLA_DECIMAL_A_HEXA = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
	
	TABLA_DECIMAL_A_BINARIO = ["0000","0001","0010","0011","0100","0101","0110","0111","1000","1001","1010","1011","1100","1101","1110","1111"]

	def __init__(self):
		return
	
	def decimal_a_hexa(self , parametro):
		if (parametro < 0):
			parametro *= -1
			
		if (parametro == 0):
			return "0"
		
		auxiliar = []
		
		while ((parametro / 16) != 0) or ((parametro % 16) != 0):		
			auxiliar.append (parametro % 16)
			parametro = parametro / 16
		
		auxiliar = auxiliar [::-1]
		
		resultado = ""
		
		for x in auxiliar:
			resultado += self.TABLA_DECIMAL_A_HEXA[x]
		
		return resultado
		
	def hexa_a_decimal(self , parametro):
		parametro_reordenado = parametro[::-1]
		i = 0
		resultado = 0
		
		while (i < len(parametro_reordenado)):
			valor = self.TABLA_HEXA[parametro_reordenado [i]]
			resultado += valor * (16 ** i)
			i += 1
		
		return resultado
		
	def hexa_a_binario(self , parametro):
		resultado = ""
		for x in parametro:
			numero = self.TABLA_HEXA[x]
			resultado += self.TABLA_DECIMAL_A_BINARIO[numero]
		
		return resultado
		
	def binario_a_hexa(self , parametro):
		resultado = ""
		auxiliar = ""
		for x in parametro:
			auxiliar += x
			if len(auxiliar) == 4:
				numero = self.TABLA_DECIMAL_A_BINARIO.index(auxiliar)
				resultado = self.TABLA_DECIMAL_A_HEXA[numero]
				auxiliar = ""
		
		return resultado
		
	def binario_a_decimal(self,parametro):
		hexa = self.binario_a_hexa(parametro)
		return self.hexa_a_decimal(hexa)
		
	def decimal_a_binario(self,parametro):
		hexa = self.decimal_a_hexa(parametro)
		return self.hexa_a_binario(hexa)
		
	def decodificar_bpfs(self , numero_binario , bits):
		es_negativo = False
		bits -= 1
		if (numero_binario == ("1"+("0"*bits))):
			return -1 * (2 ** bits)
		if (numero_binario[0] == "1"):
			es_negativo = True
			numero_binario = self._complemento_a_1(numero_binario)
		numero = self.binario_a_decimal(numero_binario)
		if (es_negativo):
			numero *= -1
			
		return numero
		
	def codificar_bpfs(self , numero, tamanio):
		binario = self.decimal_a_binario(numero)
		llenar = tamanio - len(binario)
		if binario[0] == "1":
			binario ==( "0"*llenar + binario )
		else:
			binario ==( "1"*llenar + binario )
			
		if (numero < 0) :
			binario = self._complemento_a_1(binario)
			
		return binario
			
	def negar_binario(self,numero_binario):
		resultado = ""
		for x in numero_binario:
			if (x == "1"):
				resultado += "0"
			elif (x == "0"):
				resultado += "1"
			else:
				raise ValueError
		
		return resultado
			
	def sumar_binario(self,a,b):
		a = self.binario_a_decimal(a)
		b = self.binario_a_decimal(b)
		return self.decimal_a_binario(a+b)
		
	def _complemento_a_1(self,numero):
		numero = self.negar_binario(numero)
		return self.sumar_binario(numero,"1") [-1*len(numero):]