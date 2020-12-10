from main import Object, SolarSystem, max_dim, fig
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

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
    print(i, end='\r')
    return system.update()


def create_gif(nb_of_objects, filename):
    system.plot = False
    while len(system.objects) > nb_of_objects:
        print(len(system.objects), end='\r')
        system.update()
    system.plot = True
    ani = animation.FuncAnimation(fig, animate,  blit=True, frames=300)
    ani.save(filename, writer='imagemagick', fps=30)


print('Creating early ages animation')
create_gif(1000, 'docs/animation_early.gif')

print('Creating mid ages animation')
create_gif(50, 'docs/animation_mid.gif')


print('Creating stable animation')
create_gif(10, 'docs/animation_stable.gif')
