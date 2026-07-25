import matplotlib
matplotlib.use('TkAgg')  
import matplotlib.pyplot as plt
import mesa
import numpy as np
import pandas as pd
import seaborn as sns
from mesa.discrete_space import CellAgent, OrthogonalMooreGrid

import visualization as vis

class Ant(CellAgent):
    def __init__(self, model, cell):
        super().__init__(model)
        self.role = None
        self.cell = cell

    def move(self):
        cell = self.cell.neighborhood.select_random_cell()
        if cell.is_empty:
            self.cell = cell

class Queen(Ant):
    def __init__(self, model, cell):
        super().__init__(model, cell)
        self.role = 'queen'

class Colony(mesa.Model):
    def __init__(self, ants_num, width, height, queen_num=1, seed=None):
        super().__init__(seed=seed)
        self.grid = OrthogonalMooreGrid((width, height), torus=True, random=self.random)
        self.ants_num = ants_num
        self.queen_num = queen_num
        Ant.create_agents(self, self.ants_num, self.random.choices(self.grid.all_cells.cells, k=self.ants_num))
        Queen.create_agents(self, self.queen_num, self.random.choices(self.grid.all_cells.cells, k=self.queen_num))

    def step(self):
        self.agents.shuffle_do('move')

if __name__ == '__main__':
    model = Colony(10, 100, 100)

    vis.visualize(model, 200)
