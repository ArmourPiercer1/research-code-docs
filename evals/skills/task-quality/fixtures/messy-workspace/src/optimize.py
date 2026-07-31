import numpy as np

def objective(x):
    # placeholder objective; TODO real space-charge model
    return np.sum(x**2)

def optimize(x0, steps=100):
    x = np.array(x0, dtype=float)
    for _ in range(steps):
        x -= 0.01 * 2 * x   # gradient step
    return x

if __name__ == "__main__":
    print(optimize([3.0, -2.0, 1.5]))
