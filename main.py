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
        self.mass = 0
        self.masssstamp = \
            ax.text(
                .03, .94, 'Mass: ', color='b',
                transform=ax.transAxes, fontsize='x-large')
        self.nb_objectsstamp = \
            ax.text(
                .03, .84, 'Objects: ', color='b',
                transform=ax.transAxes, fontsize='x-large')

    def add_object(self, object):
        self.objects.append(object)

    def update(self):
        dt = 0.5
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

        self.clean_system()
        self.compute_mass()
        self.masssstamp.set_text('Mass: {:.2f}'.format(self.mass))
        self.nb_objectsstamp.set_text('Objects: {}'.format(len(self.objects)))
        return plots + [self.masssstamp, self.nb_objectsstamp]

    def compute_mass(self):
        mass = 0
        for p in self.objects:
            mass += np.pi*p.rad**2
        self.mass = mass

    def fuse_objects(self):
        for p1 in self.objects:
            for p2 in self.objects:
                if p2 != p1:
                    u = p2.r - p1.r
                    u_norm = np.sum(u**2)**0.5
                    scaling_factor = 0.06/28
                    if u_norm <= (p1.rad + p2.rad)*scaling_factor:
                        meq, veq = momentum_conservation(
                            p1.v, p2.v,
                            np.pi*p1.rad**2, np.pi*p2.rad**2)
                        p1.rad = (meq/np.pi)**0.5
                        p1.v = veq
                        p2.rad = 0
                        self.objects.remove(p2)

    def clean_system(self):
        bound = 2
        for p in self.objects:
            if np.sum(p.r**2)**0.5 > bound:
                self.objects.remove(p)


def momentum_conservation(v1, v2, m1, m2):
    meq = m1 + m2
    veq = v1 / (1 + m2/m1) + v2 / (1 + m1/m2)
    return meq, veq


if __name__ == "__main__":
    fig = plt.figure(figsize=[6, 6])
    max_dim = 1
    ax = plt.axes([0., 0., 1., 1.], xlim=(-max_dim, max_dim), ylim=(-max_dim, max_dim))
    ax.set_aspect('equal')
    size_sun = 28
    Sun = Object("sun", rad=size_sun, color='tab:orange', r=[0, 0, 0], v=[0, 0, 0])
    system = SolarSystem(Sun)

    # initialise positions and velocities
    for i in range(200):
        radius = size_sun/2*np.random.uniform(low=0, high=0.5)
        pos = np.zeros(3)
        while np.sum(pos**2) < 0.25:
            pos = max_dim*np.random.uniform(low=-1, high=1, size=3)
            pos[2] = 0

        v0 = np.random.uniform(low=0, high=0.05)
        vel = v0*np.array([-pos[1], pos[0], 0])/np.sum(pos**2)**0.5
        obj = Object(str(i), radius, 'black', pos, vel)
        system.add_object(obj)

    def animate(i):
        return system.update()

    ani = animation.FuncAnimation(fig, animate, repeat=True, frames=200, blit=True, interval=5,)
    plt.show()
