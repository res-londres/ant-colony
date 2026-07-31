import model
import visualization as vis

if __name__ == '__main__':
    model = model.Colony(50, 100)

    vis.animate(model, 500)
