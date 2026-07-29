from mesa.discrete_space import CellAgent

class Ant(CellAgent):
    def __init__(self, model, cell):
        super().__init__(model)
        self.role = None
        self.cell = cell

    def move(self):
        cell = self.cell.neighborhood.select_random_cell()
        self.cell = cell

class Queen(Ant):
    def __init__(self, model, cell):
        super().__init__(model, cell)
        self.role = 'queen'

class FoodSource(CellAgent):
    def __init__(self, model, cell, max_food, growth_rate=1):
        super().__init__(model)
        self.cell = cell
        self.max_food = max_food
        self.food_amt = max_food
        self.growth_rate = growth_rate

    def grow(self):
        self.food_amt = min(self.max_food, self.food_amt * self.growth_rate)