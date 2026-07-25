import matplotlib
matplotlib.use('TkAgg')  
import matplotlib.pyplot as plt
import numpy as np

def visualize(model, steps=50, pause=0.1):
    plt.ion()
    fig, ax = plt.subplots(figsize=(20, 20))
    
    for step in range(steps):
        model.step()
        
        heatmap = np.zeros((model.grid.width, model.grid.height))
        positions = []
        
        for cell in model.grid.all_cells:
            x, y = cell.coordinate
            count = len(cell.agents)
            heatmap[cell.coordinate] = count
            if count > 0:
                positions.extend([(x, y)] * count)
        
        positions = np.array(positions)
        
        ax.clear()
        
        im = ax.imshow(heatmap.T, cmap='YlOrRd', alpha=0.6, 
                        extent=[-0.5, model.grid.width-0.5, -0.5, model.grid.height-0.5],
                        origin='lower', vmin=0, vmax=5)
        
        if len(positions) > 0:
            ax.scatter(positions[:, 0], positions[:, 1], 
                        c='darkblue', s=20, alpha=0.8)
        
        ax.set_xlim(-0.5, model.grid.width - 0.5)
        ax.set_ylim(-0.5, model.grid.height - 0.5)
        ax.set_title(f"Step {step+1}")
        
        plt.pause(pause)
    
    plt.ioff()
    plt.show()