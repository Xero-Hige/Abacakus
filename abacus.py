import csv

class Abbacus (object):
        ac  =  ""
        ri = ""
        rpi =  "300"

        memoria = {}

        TABLA_HEXA = { "0":0 , "1": 1 , "2":2 , "3":3 , "4":4 ,
                       "5":5 , "6":6 , "7":7 , "8":8 , "9":9 ,
                       "A":10, "B":11 ,"C":12 ,"D":13,"E":14,"F":15}

        TABLA_DECIMAL_A_HEXA = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]

        TABLA_DECIMAL_A_BINARIO = ["0000","0001","0010","0011","0100","0101","0110","0111","1000","1001","1010","1011","1100","1101","1110","1111"]

        TAMANIO_CELDA = 16 #en bits

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
                hexa = self.sumar_hexa(self.ac,parametro)[-4:]
                while len(hexa) < (self.TAMANIO_CELDA / 4):
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

        def bifurcar_mayor_0 (self , parametro):
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

        def decimal_a_hexa(self , parametro):
                auxiliar = []

                while ((parametro / 16) != 0) or  ((parametro % 16) != 0):
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

        def decodificar_bpf(self , numero_binario):
                es_negativo = False
                if (numero_binario == ("1"+("0"*15))):
                        return -128
                if (numero_binario[0] == "1"):
                        es_negativo = True
                        numero_binario = self.complemento_a_1(numero_binario)
                numero = self.binario_a_decimal(numero_binario)
                if (es_negativo):
                        numero *= -1

                return numero
                        

        def codificar_bpf(self , numero):
                binario = self.decimal_a_binario(numero)
                binario = completar_binario(binario)

                if (numero < 0) :
                        binario = self.complemento_a_1(binario)

        def busqueda_instrucion(self):
                self.ri  = self.memoria[self.rpi]
                self.rpi = self.sumar_hexa(self.rpi,"1")

        def ejecutar_instruccion(self):
                print self.ri
                instruccion = self.INSTRUCCIONES[self.ri[0]]
                instruccion(self,self.ri[1:])

        def sumar_hexa(self , numero1 , numero2):
                a = self.hexa_a_decimal(numero1)
                b = self.hexa_a_decimal(numero2)
                return self.decimal_a_hexa(a+b)[-4:]

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

a = Abbacus()

a.correr_programa("./suma_abbacus.aba")

