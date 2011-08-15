import math
from config import *

class Ambiente:

  def __init__(self, temperatura):
    self.temperatura_inicial = self.temperatura = temperatura

  def aumenta_temperatura_gradualmente(self):
    if self.__valida_aumento_temperatura():
      self.temperatura += AUMENTO_TEMP_POR_MINUTO
      return True
    else:
      return False
  
  def __valida_aumento_temperatura(self):
    return self.temperatura < self.temperatura_inicial and self.temperatura + AUMENTO_TEMP_POR_MINUTO <= self.temperatura_inicial
    
class Hardware:

  def __init__(self, ambiente, temp_desejada):
    self.ambiente = ambiente 
    self.temp_desejada = temp_desejada

  def reduz_um_grau(self):
    self.ambiente.temperatura -= 1

class Controlador:

  def __init__(self):
    self.custo_total = 0
    self.temperatura = 0
    self.ar_condicionado = False 

  def refrigera(self, temp_atual, temp_desejada):
    self.temperatura = temp_atual =  int(math.ceil(temp_atual))
    temp_desejada = int(math.ceil(temp_desejada))

    if temp_atual > temp_desejada + TOLERANCIA_TEMPERATURA:
      if not self.ar_condicionado:
        self.__liga_ar_condicionado(temp_atual, temp_desejada)
      self.__reajusta_temperatura()

    return (self.temperatura, round(self.custo_total, 2))

  def __liga_ar_condicionado(self, temp_atual, temp_desejada):
    ambiente = Ambiente(temp_atual)
    self.ar_condicionado = Hardware(ambiente, temp_desejada)
    self.custo_total += CUSTO_LIGAR

  def __reajusta_temperatura(self):
    temp_inicial = int(math.ceil(self.ar_condicionado.ambiente.temperatura))
    temp_final = self.ar_condicionado.temp_desejada + TOLERANCIA_TEMPERATURA
    for x in xrange(temp_inicial, temp_final, -1):
      self.ar_condicionado.reduz_um_grau()
      self.custo_total += CUSTO_GRAU
      self.temperatura = self.ar_condicionado.ambiente.temperatura    

def main():
  c = Controlador()
  dados = c.refrigera(30, 20)

  if c.ar_condicionado:
    for x in range(360):
      c.ar_condicionado.ambiente.aumenta_temperatura_gradualmente()
      dados = c.refrigera(c.ar_condicionado.ambiente.temperatura, c.ar_condicionado.temp_desejada)

  print "Temperatura final: %d" % dados[0]
  print "Custo total: %.2f" % dados[1]

if __name__ == '__main__':
  main()      