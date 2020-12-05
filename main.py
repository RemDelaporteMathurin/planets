import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Object:
    def __init__(self, name, rad, color, r, v):
        self.name = name
        self.r = np.array(r, dtype=np.float)
        self.v = np.array(v, dtype=np.float)
        self.plot = ax.scatter(
            r[0], r[1], color=color, s=rad**2,
            edgecolors=None, zorder=10)
        self.rad = rad


class SolarSystem:
    def __init__(self, thesun):
        self.thesun = thesun
        self.objects = []
        self.time = 0

    def add_object(self, object):
        self.objects.append(object)

    def update(self):
        dt = 0.1
        self.time += dt
        plots = []
        for p in self.objects:
            p.r += p.v * dt
            acc = -2.959e-4 * p.r / np.sum(p.r**2)**(3./2)
            p.v += acc * dt
            p.plot.set_offsets(p.r[:2])
            p.plot.set_sizes([p.rad**2])
            plots.append(p.plot)
        self.fuse_objects()
        print(len(self.objects), end="\r")
        return plots

    def fuse_objects(self):
        for p1 in self.objects:
            for p2 in self.objects:
                if p2 != p1:
                    # TODO detect when objects are touching
                    u = p2.r - p1.r
                    u_norm = np.sum(u**2)**0.5
                    if u_norm < 0.1:
                        meq, veq = momentum_conservation(p1.v, p2.v, p1.rad, p2.rad)
                        p1.rad = (p1.rad**2 + p2.rad**2)**0.5
                        p1.v = veq
                        p2.rad = 0
                        self.objects.remove(p2)

    def clean_system(self):
        bound = 3
        for p in self.objects:
            if np.sum(p.r**2)**0.5 > bound:
                self.objects.remove(p)


def momentum_conservation(v1, v2, m1, m2):
    meq = m1 + m2
    veq = v1 / (1 + m1/m2) + v2 / (1 + m2/m1)
    return meq, veq


fig = plt.figure(figsize=[6, 6])
max_dim = 2
ax = plt.axes([0., 0., 1., 1.], xlim=(-max_dim, max_dim), ylim=(-max_dim, max_dim))
ax.set_aspect('equal')
size_sun = 28
Sun = Object("sun", rad=size_sun, color='tab:orange', r=[0, 0, 0], v=[0, 0, 0])
system = SolarSystem(Sun)

# initialise positions and velocities
for i in range(300):
    radius = size_sun/2*np.random.uniform(low=0, high=0.2)
    pos = np.zeros(3)
    while np.sum(pos**2) < 1:
        pos = max_dim*np.random.uniform(low=-1, high=1, size=3)
        pos[2] = 0

    v0 = np.random.uniform(low=0, high=0.05)
    vel = v0*np.array([-pos[1], pos[0], 0])/np.sum(pos**2)**0.5
    obj = Object(str(i), radius, 'black', pos, vel)
    system.add_object(obj)


def animate(i):
    return system.update()


ani = animation.FuncAnimation(fig, animate, repeat=True, frames=200, blit=True, interval=10,)
plt.show()
