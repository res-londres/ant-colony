import model
import visualization as vis

if __name__ == '__main__':
    model = model.Colony(1, 10)

    vis.animate(model, 500)
