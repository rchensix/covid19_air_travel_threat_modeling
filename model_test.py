# Ruiqi Chen
# July 29, 2020

import unittest

import model

class TestSEIRModel(unittest.TestCase):
    def test_initialization(self):
        init_conditions = {
            'San Francisco-Oakland-Berkeley CA MSA': (4731802, 0, 1, 0),
            'San Jose-Sunnyvale-Santa Clara CA MSA': (1990658, 0, 2, 0),
        }
        seir = model.SEIRTwoStepModel(0, t_incubation=3, t_infectious=10, start_mmyy='01-20',
                                       start_day=20, init_conditions=init_conditions)
        # Check populations set using initial conditions
        population = seir.population['San Francisco-Oakland-Berkeley CA MSA'][0]
        self.assertEqual(population[0], '01-20')
        self.assertEqual(population[1], 20)
        self.assertEqual(population[2], 4731802)
        self.assertEqual(population[3], 0)
        self.assertEqual(population[4], 1)
        self.assertEqual(population[5], 0)
        population = seir.population['San Jose-Sunnyvale-Santa Clara CA MSA'][0]
        self.assertEqual(population[0], '01-20')
        self.assertEqual(population[1], 20)
        self.assertEqual(population[2], 1990658)
        self.assertEqual(population[3], 0)
        self.assertEqual(population[4], 2)
        self.assertEqual(population[5], 0)
        # Check population set using default population data
        population = seir.population['New York-Newark-Jersey City NY-NJ-PA MSA'][0]
        self.assertEqual(population[0], '01-20')
        self.assertEqual(population[1], 20)
        self.assertEqual(population[2], 19216182)
        self.assertEqual(population[3], 0)
        self.assertEqual(population[4], 0)
        self.assertEqual(population[5], 0)

if __name__ == '__main__':
    unittest.main()