import mesa
import numpy as np
from mesa.discrete_space import OrthogonalMooreGrid
from perlin_noise import PerlinNoise

from agents import *

class Colony(mesa.Model):
    def __init__(self, ants_num, width, height=None, queen_num=1, seed=None, terrain_seed=0):
        super().__init__(seed=seed)
        self.width = width
        self.height = width if height is None else height
        self.ants_num = ants_num
        self.queen_num = queen_num
        self.grid = OrthogonalMooreGrid((self.width, self.height), torus=True, random=self.random)
        
        Ant.create_agents(self, self.ants_num, self.random.choices(self.grid.all_cells.cells, k=self.ants_num))
        Queen.create_agents(self, self.queen_num, self.random.choices(self.grid.all_cells.cells, k=self.queen_num))

        self.foodmap = self._generate_foodmap(seed=terrain_seed)
        self._place_food()

    def _generate_foodmap(self, seed=0):
        ''' generate foodmap using perlin noise '''
        foodmap = np.zeros((self.width, self.height))
    
        noise = PerlinNoise(octaves=4, seed=seed)
        
        scale = 0.01
        for x in range(self.width):
            for y in range(self.height):
                noise_value = noise([x * scale, y * scale])
                foodmap[x][y] = noise_value

        min_val = foodmap.min()
        max_val = foodmap.max()
        foodmap = (foodmap - min_val) / (max_val - min_val) * 2 - 1
    
        return foodmap

    def _place_food(self):
        ''' place FoodSource agents on cells based on terrain value '''
        for cell in self.grid.all_cells.cells:
            x, y = cell.coordinate
            noise_value = self.foodmap[x][y]
            food_amt = self._scale_noise_to_food(noise_value) # 1 to 10
            
            if food_amt > 0:
                growth_rate = 1.0 + (food_amt / 10) * 0.05 # 1.0 to 1.05
                FoodSource.create_agents(
                    self, 
                    1, 
                    cell, 
                    max_food=food_amt,
                    growth_rate=growth_rate
                )

    def _scale_noise_to_food(self, noise_value):
        ''' convert noise value (-1 to 1) to a food amount (0 to 10) '''
        max_food = 10
        normalized = (noise_value + 1) / 2  # change range from (-1 to 1) to (0 to 1)
        power = 3.00                        # higher power -> more barren areas
        scaled = normalized ** power        # 
        if scaled < 0.1:
            return 0
        food_amt = scaled * max_food
        return food_amt

    def step(self):
        self.agents_by_type[FoodSource].do('grow')
        ants = self.agents.select(lambda a: isinstance(a, Ant))
        ants.shuffle_do('manage_action')
        dead = ants.select(lambda a: a.energy <= 0)
        for agent in dead:
            agent.remove()


