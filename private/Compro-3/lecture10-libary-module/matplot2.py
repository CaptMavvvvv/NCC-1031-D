import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animations

fig, ax = plt.subplots()

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

line, = ax.plot(x,y)

def update(frame):
    line.set_ydata(np.sin(x+frame/10.0))
    return line,

ani = animations.FuncAnimation(fig,update,frames=100,interval=50,blit=True)
plt.show()