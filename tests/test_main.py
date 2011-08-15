import sys
from os.path import join, abspath, dirname
sys.path.append(abspath(join(dirname(__file__), '..')))

import unittest
from arcondicionado.arcondicionado import *

class TestAmbiente(unittest.TestCase):

  def setUp(self):
    self.ambiente = Ambiente(30)

  def test_aumenta_temperatura_gradualmente(self):
    self.ambiente.temperatura = 20
    for minuto in range(100):
      if minuto < 20:
        self.assertTrue(self.ambiente.aumenta_temperatura_gradualmente())
      else:
        self.assertFalse(self.ambiente.aumenta_temperatura_gradualmente())
    self.assertEqual(self.ambiente.temperatura, 30)

class TestHardware(unittest.TestCase):

  def setUp(self):
    ambiente = Ambiente(30)
    self.ar_condicionado = Hardware(ambiente, 22)

  def test_reduz_um_grau(self):
    self.ar_condicionado.ambiente.temperatura = 30
    self.ar_condicionado.reduz_um_grau()
    self.assertEqual(self.ar_condicionado.ambiente.temperatura, 29)

class TestControlador(unittest.TestCase):

  def setUp(self):
    ambiente = Ambiente(30)
    self.controlador = Controlador()

  def test_refrigera(self):
    dados = self.controlador.refrigera(30, 20)
    self.assertEqual(dados[0], 22)
    self.assertEqual(dados[1], 1.3)
    pass

  def test_refrigera_temperatura_maior_que_atual(self):
    dados = self.controlador.refrigera(30, 32)
    self.assertEqual(dados[0], 30)
    self.assertEqual(dados[1], 0)

  def test_refrigera_margem_erro(self):
    dados = self.controlador.refrigera(30, 28)
    self.assertEqual(dados[0], 30)
    self.assertEqual(dados[1], 0)

  def test_refrigera_por_360_minutos(self):
    c = self.controlador
    dados = c.refrigera(30, 20)
    for x in range(360):
      c.ar_condicionado.ambiente.aumenta_temperatura_gradualmente()
      dados = c.refrigera(c.ar_condicionado.ambiente.temperatura, c.ar_condicionado.temp_desejada)

    self.assertEqual(dados[0], 22)
    self.assertEqual(dados[1], 19.3)

if __name__ == '__main__':
  unittest.main()
