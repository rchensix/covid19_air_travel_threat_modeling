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

    def test_stepping(self):
        init_conditions = {
            'San Francisco-Oakland-Berkeley CA MSA': (4731802, 0, 1, 0),
            'San Jose-Sunnyvale-Santa Clara CA MSA': (1990658, 0, 2, 0),
        }
        seed = 0
        seir = model.SEIRTwoStepModel(seed, t_incubation=3, t_infectious=10, start_mmyy='01-20',
                                       start_day=20, init_conditions=init_conditions)
        print(seir.population['San Jose-Sunnyvale-Santa Clara CA MSA'])
        print(seir.population['New York-Newark-Jersey City NY-NJ-PA MSA'])
        seir.step_airplane(0.05, 0.85)
        print(seir.population['San Jose-Sunnyvale-Santa Clara CA MSA'])
        print(seir.population['New York-Newark-Jersey City NY-NJ-PA MSA'])
        seir.step_metro(0.05)
        print(seir.population['San Jose-Sunnyvale-Santa Clara CA MSA'])
        print(seir.population['New York-Newark-Jersey City NY-NJ-PA MSA'])

    def test_20_day_log(self):
        init_conditions = {
            'San Francisco-Oakland-Berkeley CA MSA': (4731802, 0, 10, 0),
            'San Jose-Sunnyvale-Santa Clara CA MSA': (1990658, 0, 10, 0),
        }
        seed = 0
        seir = model.SEIRTwoStepModel(seed, t_incubation=3, t_infectious=10, start_mmyy='01-20',
                                      start_day=20, init_conditions=init_conditions)
        print(seir.population['San Jose-Sunnyvale-Santa Clara CA MSA'][-1])
        print(seir.population['New York-Newark-Jersey City NY-NJ-PA MSA'][-1])
        num_steps = 20
        for i in range(num_steps):
            seir.step_airplane(0.05, 0.85)
            seir.step_metro(0.05)
        print(seir.population['San Jose-Sunnyvale-Santa Clara CA MSA'][-1])
        print(seir.population['New York-Newark-Jersey City NY-NJ-PA MSA'][-1])
        log_path = 'data/test_20_day_log.txt'
        seir.write_to_log_file(log_path)

if __name__ == '__main__':
    unittest.main()