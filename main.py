import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Object:
    def __init__(self, name, rad, colour, r, v):
        self.name = name
        self.r = np.array(r, dtype=np.float)
        self.v = np.array(v, dtype=np.float)
        self.plot = ax.scatter(
            r[0], r[1], color=colour, s=rad**2,
            edgecolors=None, zorder=10)
        self.rad = rad
        self.colour = colour
        self.xs = []
        self.ys = []
        self.line, = ax.plot([], [], color=colour, linewidth=1.4, alpha=0.3)


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
        self.plot_orbitals = False

    def add_object(self, object):
        self.objects.append(object)

    def update(self):
        dt = 0.5
        self.time += dt
        plots = []
        lines = []
        if len(self.objects) < 40:
            self.plot_orbitals = True
        for p in self.objects:
            if self.plot_orbitals:
                p.xs.append(p.r[0])
                p.ys.append(p.r[1])
                p.line.set_xdata(p.xs[-500:])
                p.line.set_ydata(p.ys[-500:])
                p.line.set_color(p.colour)
                lines.append(p.line)
            p.r += p.v * dt
            acc = -2.959e-4 * p.r / np.sum(p.r**2)**(3./2)
            p.v += acc * dt
            p.plot.set_offsets(p.r[:2])
            p.plot.set_sizes([p.rad**2])
            p.plot.set_color(p.colour)
            plots.append(p.plot)
        self.fuse_objects()

        self.clean_system()
        self.compute_mass()
        self.masssstamp.set_text('Mass: {:.2f}'.format(self.mass))
        self.nb_objectsstamp.set_text('Objects: {}'.format(len(self.objects)))
        return plots + lines + [self.masssstamp, self.nb_objectsstamp]

    def compute_mass(self):
        mass = 0
        for p in self.objects:
            mass += np.pi*p.rad**2
        self.mass = mass

    def fuse_objects(self):
        objects_to_fuse = self.objects[:]
        scaling_factor = 0.06/28
        positions = [p.r for p in objects_to_fuse]
        while len(objects_to_fuse) > 1:
            p1 = objects_to_fuse[0]
            positions.pop(0)
            index_closest, distance_closest = closest_node(p1.r, positions)
            p2 = objects_to_fuse[1 + index_closest]
            if distance_closest <= (p1.rad + p2.rad)*scaling_factor:
                m1 = np.pi*p1.rad**2
                m2 = np.pi*p2.rad**2
                meq, veq = momentum_conservation(
                    p1.v, p2.v,
                    m1, m2)
                p1.r = (m1*p1.r + m2*p2.r)/meq
                p1.rad = (meq/np.pi)**0.5
                p1.v = veq
                p2.rad = 0
                p1.colour = (m1*p1.colour + m2*p2.colour)/meq

                self.objects.remove(p2)
                objects_to_fuse.remove(p2)
                positions.pop(index_closest)
            objects_to_fuse.remove(p1)

    def clean_system(self):
        bound = 2
        for p in self.objects:
            if np.sum(p.r**2)**0.5 > bound:
                self.objects.remove(p)


def momentum_conservation(v1, v2, m1, m2):
    meq = m1 + m2
    veq = v1 / (1 + m2/m1) + v2 / (1 + m1/m2)
    return meq, veq


def closest_node(node, nodes):
    dist_2 = np.sum((np.asarray(nodes) - node)**2, axis=1)**0.5
    i = np.argmin(dist_2)
    return i, dist_2[i]


if __name__ == "__main__":
    fig = plt.figure(figsize=[6, 6])
    max_dim = 1
    ax = plt.axes([0., 0., 1., 1.], xlim=(-max_dim, max_dim), ylim=(-max_dim, max_dim))
    ax.set_aspect('equal')
    size_sun = 28
    Sun = Object("sun", rad=size_sun, colour='tab:orange', r=[0, 0, 0], v=[0, 0, 0])
    system = SolarSystem(Sun)

    # initialise positions and velocities
    for i in range(1000):
        radius = size_sun/2*np.random.uniform(low=0, high=0.25)
        pos = np.zeros(3)
        while np.sum(pos**2) < 0.25:
            pos = max_dim*np.random.uniform(low=-1, high=1, size=3)
            pos[2] = 0
        dist = np.linalg.norm(pos)
        range_vel = 0.005
        v0 = np.random.uniform(
            low=0.0175 - range_vel/2, high=0.0175 + range_vel/2)/(dist)**0.5
        vel = v0*np.array([-pos[1], pos[0], 0])/np.sum(pos**2)**0.5
        colour = np.random.uniform(low=0, high=1, size=3)
        obj = Object(str(i), radius, colour, pos, vel)
        system.add_object(obj)

    def animate(i):
        return system.update()

    ani = animation.FuncAnimation(fig, animate, repeat=True, frames=200, blit=True, interval=5,)
    plt.show()
