import unittest
import src.Game as Game

class Test(unittest.TestCase):
    def test_value(self):
        e = Game.Event()
        o = [100, 0, 350, 50, 550]
        #sprawdzenie metody score
        self.assertEqual(e.score([80, 450, 20], o), 0)
        self.assertEqual(e.score([125, 450, 20], o), 1)
        self.assertEqual(e.score([140, 450, 20], o), 1)
        #sprawdzenie metody collision
        self.assertEqual(e.collision([20, 150, 20], o), 0)
        self.assertEqual(e.collision([90, 150, 20], o), 1)
        self.assertEqual(e.collision([90, 360, 20], o), 1)
        self.assertEqual(e.collision([120, 360, 20], o), 1)
        self.assertEqual(e.collision([50, 450, 20], o), 0)
        self.assertEqual(e.collision([120, 450, 20], o), 0)
        self.assertEqual(e.collision([90, 540, 20], o), 1)
        self.assertEqual(e.collision([120, 540, 20], o), 1)
        self.assertEqual(e.collision([50, 700, 20], o), 0)
        self.assertEqual(e.collision([90, 700, 20], o), 1)
        self.assertEqual(e.collision([50, 790, 20], o), 1)
