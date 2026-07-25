import mesa
from mesa.discrete_space import OrthogonalMooreGrid

from agents import *

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