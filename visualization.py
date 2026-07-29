import matplotlib
matplotlib.use('TkAgg')  
import matplotlib.pyplot as plt
import numpy as np

from agents import *

def animate(model, steps=50, pause=0.1):
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 20))

    paused = False
    step = 0

    def handle_key(event):
        nonlocal paused
        if event.key == ' ':
            paused = not paused 

    fig.canvas.mpl_connect('key_press_event', handle_key)
      
    while step < steps:
        if not paused:
            model.step()
            
            ants_plot(model, ax1, step)
            food_plot(model, ax2, step)
            
            plt.pause(pause)
            step += 1
        else:
            plt.pause(0.1)
    
    plt.ioff()
    plt.show()

def ants_plot(model, ax, step):
    antmap = np.zeros((model.width, model.height))
    positions = []
    appearance = Appearance()
    
    for cell in model.grid.all_cells:
        count = len(cell.agents)
        antmap[cell.coordinate] = count

        for agent in cell.agents:
            if isinstance(agent, Ant):
                positions.append(cell.coordinate)
                appearance.determine(agent)

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
    ax.set_title(f"Ant Colony - Step {step+1}")

def food_plot(model, ax, step):
    foodmap = np.zeros((model.width, model.height))
    for cell in model.grid.all_cells:
        food_total = 0
        for agent in cell.agents:
            if isinstance(agent, FoodSource):  
                food_total += agent.food_amt
        foodmap[cell.coordinate] = food_total

    ax.clear()
        
    im = ax.imshow(foodmap.T, cmap='Greens', alpha=0.8,
                    extent=[-0.5, model.grid.width-0.5, -0.5, model.grid.height-0.5],
                    origin='lower', vmin=0, vmax=10)

    ax.set_xlim(-0.5, model.grid.width - 0.5)
    ax.set_ylim(-0.5, model.grid.height - 0.5)
    ax.set_title(f"Food Map - Step {step+1}")

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