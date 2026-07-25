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
        self.cell = cell

    def move(self):
        cell = self.cell.neighborhood.select_random_cell()
        if cell.is_empty:
            self.cell = cell

class Colony(mesa.Model):
    def __init__(self, num, width, height, seed=None):
        super().__init__(seed=seed)
        self.grid = OrthogonalMooreGrid((width, height), torus=True, random=self.random)
        self.num = num
        Ant.create_agents(self, self.num, self.random.choices(self.grid.all_cells.cells, k=self.num))

    def step(self):
        self.agents.shuffle_do('move')

if __name__ == '__main__':
    model = Colony(100, 100, 100)

    vis.visualize(model, 200)
