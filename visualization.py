import matplotlib
matplotlib.use('TkAgg')  
import matplotlib.pyplot as plt
import numpy as np



def visualize(model, steps=50, pause=0.1):
    plt.ion()
    fig, ax = plt.subplots(figsize=(20, 20))
    
    for step in range(steps):
        model.step()
        
        antmap = np.zeros((model.grid.width, model.grid.height))
        positions = []
        appearance = Appearance()
        
        for cell in model.grid.all_cells:
            x, y = cell.coordinate
            count = len(cell.agents)
            antmap[cell.coordinate] = count

            for ant in cell.agents:
                positions.append([x, y])
                appearance.determine(ant)

        positions = np.array(positions)
        
        ax.clear()
        
        im = ax.imshow(antmap.T, cmap='YlOrRd', alpha=0.6, 
                        extent=[-0.5, model.grid.width-0.5, -0.5, model.grid.height-0.5],
                        origin='lower', vmin=0, vmax=5)
        
        if len(positions) > 0:
            ax.scatter(positions[:, 0], positions[:, 1], 
                        c=appearance.colors, s=appearance.sizes, alpha=0.8)
        
        ax.set_xlim(-0.5, model.grid.width - 0.5)
        ax.set_ylim(-0.5, model.grid.height - 0.5)
        ax.set_title(f"Step {step+1}")
        
        plt.pause(pause)
    
    plt.ioff()
    plt.show()

class Appearance:
    def __init__(self):
        self.colors = list()
        self.sizes = list()

    def determine(self, ant):
        if ant.role == 'queen':
            self.colors.append('gold')
            self.sizes.append(80)
        else:
            self.colors.append('red')
            self.sizes.append(20)