from mesa.discrete_space import CellAgent

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