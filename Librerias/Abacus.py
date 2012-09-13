import csv

class Abbacus (object):

	ac  =  ""
	ri = ""
	rpi =  "300"
	
	memoria = {}
	
	TAMANIO_CELDA = 16 #en bits
	CARACTERES_HEXA = TAMANIO_CELDA / 4
	
	def carga_inmediata (self , parametro):
		if (self.hexa_a_binario(parametro)[0] == "1"):
			parametro = "F" + parametro
		else:
			parametro = "0" + parametro
		
		self.ac = parametro
		
	def carga (self , parametro):
		self.ac = self.memoria[parametro]
		
	def almacenar (self , parametro):
		self.memoria[parametro] = self.ac

	def suma (self , direccion_parametro):
		parametro = self.memoria[direccion_parametro]
		hexa = self.sumar_hexa(self.ac,parametro)[-1 * CARACTERES_HEXA:]
		while len(hexa) < (self.TAMANIO_CELDA / CARACTERES_HEXA):
			hexa = "0"+hexa
		self.ac = hexa
		
	def not_ac (self , parametro):
		binario = self.hexa_a_binario(self.ac)
		binario = self.negar_binario (binario)
		self.ac = self.binario_a_hexa(binario)

        def bifurcar_igual_0 (self , parametro):
		numero = self.hexa_a_binario(self.ac)
		
		if (self.decodificar_bpf(numero) == 0):
			self.rpi = parametro
			
	def bifurcar_mayor_0 (self , parametro
		numero = self.hexa_a_binario(self.ac)
		if (self.decodificar_bpf(numero) > 0):
			self.rpi = parametro
	
	def bifurcar_menor_0 (self , parametro):
		numero = self.hexa_a_binario(self.ac)
		if (self.decodificar_bpf(numero) < 0):
			self.rpi = parametro
			
	def fin_programa (self , parametro):
		self.guardar()
		os._exit(1)

	def busqueda_instrucion(self):
		self.ri  = self.memoria[self.rpi]
		self.rpi = self.sumar_hexa(self.rpi,"1")
	
	def ejecutar_instruccion(self):
		instruccion = self.INSTRUCCIONES[self.ri[0]]
		instruccion(self,self.ri[1:])
	
	def sumar_hexa(self , numero1 , numero2):
		a = self.hexa_a_decimal(numero1)
		b = self.hexa_a_decimal(numero2)
		return self.decimal_a_hexa(a+b)[-1 * CARACTERES_HEXA:]
		
	def negar_binario(self , numero):
		resultado = ""
		for x in numero:
			if (x == "1"):
				resultado += "0"
			elif (x == "0"):
				resultado += "1"
			else:
				raise ValueError
		
		return resultado
		
	def guardar(self):
		claves = self.memoria.keys()
		claves.sort()
		
		a = open("./resultado.out","w")
		for clave in claves:
			a.write(clave+" "+self.memoria[clave]+"\n")
			
		a.close()
		
	def correr_programa(self , path):
		archivo = open(path)
		
		reader = csv.reader(archivo,delimiter=" ")
		
		for linea in reader:
			self.memoria[linea[0]] = linea[1]
		
		archivo.close()
		
		while True:
			self.busqueda_instrucion()
			self.ejecutar_instruccion()

	INSTRUCCIONES = { "0":carga_inmediata,
	"1":carga,
	"2":almacenar,
	"3":suma,
	"4":None,
	"5":None,
	"6":not_ac,
	"7":bifurcar_igual_0,
	"8":bifurcar_mayor_0,
	"9":bifurcar_menor_0,
	"A":None,
	"B":None,
	"C":None,
	"D":None,
	"E":None,
	"F":fin_programa}