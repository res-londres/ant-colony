import model
import visualization as vis

if __name__ == '__main__':
    model = model.Colony(50, 25)

    vis.animate(model, 200)
