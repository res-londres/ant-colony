from mesa.discrete_space import CellAgent

class Ant(CellAgent):
    def __init__(self, model, cell):
        super().__init__(model)
        self.role = None
        self.cell = cell
        self.energy = 50 # test val

    def move(self):
        best_food = 0
        target_cell = None
        
        for cell in [self.cell] + list(self.cell.neighborhood):
            for agent in cell.agents:
                if isinstance(agent, FoodSource):
                    if agent.food_amt > best_food:
                        best_food = agent.food_amt
                        target_cell = cell
        
        if target_cell is not None:
            # more food = more likely to go there
            # less food = more likely to wander
            wander_chance = 1.0 / (best_food + 1)  
            
            if self.random.random() > wander_chance:  
                self.cell = target_cell
            else: 
                self.cell = self.cell.neighborhood.select_random_cell()
        else:
            self.cell = self.cell.neighborhood.select_random_cell()

    def eat(self):
        for agent in self.cell.agents:
            if isinstance(agent, FoodSource):
                if agent.food_amt > 0.01:
                    max_consumption = 2 # todo: add appetite val for each ant
                    consumed_food = min(agent.food_amt - 0.01, max_consumption) # test consumption val
                    agent.food_amt -= consumed_food
                    self.energy += consumed_food
    
    def manage_action(self):
        if self.energy < 15: # test threshold
            self.eat()
        self.move()
        self.energy -= 1 # test val

class Queen(Ant):
    def __init__(self, model, cell):
        super().__init__(model, cell)
        self.role = 'queen'

class FoodSource(CellAgent):
    def __init__(self, model, cell, max_food, growth_rate=1.01):
        super().__init__(model)
        self.cell = cell
        self.max_food = max_food
        self.food_amt = max_food
        self.growth_rate = growth_rate

    def grow(self):
        self.food_amt = max(0.1, min(self.max_food, self.food_amt * self.growth_rate))