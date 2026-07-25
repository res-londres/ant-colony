import model
import visualization as vis

if __name__ == '__main__':
    model = model.Colony(100, 100, 100)

    vis.visualize(model, 200)
