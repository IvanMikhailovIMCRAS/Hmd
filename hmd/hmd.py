import hoomd
import hoomd.md
import numpy as np

cell = hoomd.md.nlist.Cell(buffer=0.4)
lj = hoomd.md.pair.LJ(nlist=cell)
lj.params[('A', 'A')] = dict(epsilon=1, sigma=1)
lj.r_cut[('A', 'A')] = 2.5

integrator = hoomd.md.Integrator(dt=0.005)
integrator.forces.append(lj)
bussi = hoomd.md.methods.thermostats.Bussi(kT=1.5)
nvt = hoomd.md.methods.ConstantVolume(filter=hoomd.filter.All(), thermostat=bussi)
integrator.methods.append(nvt)

gpu = hoomd.device.GPU()
sim = hoomd.Simulation(device=gpu, seed=200)
sim.operations.integrator = integrator

# Place particles on simple cubic lattice.
N_per_side = 14
N = N_per_side ** 3
L = 20
xs = np.linspace(0, 0.9, N_per_side)
x, y, z = np.meshgrid(xs, xs, xs)
coords = np.array(
(x.ravel(), y.ravel(), z.ravel())).T
print(len(coords))

# One way to define an initial system state is
# by defining a snapshot and using it to
# initialize the system state.
snap = hoomd.Snapshot()
snap.particles.N = N
snap.configuration.box = hoomd.Box.cube(L)
snap.particles.position[:] = (coords - 0.5) * L
snap.particles.types = ['A']
sim.create_state_from_snapshot(snap)

# Set up output
gsd = hoomd.write.GSD(trigger=100, filename='trajectory.gsd')
sim.operations.writers.append(gsd)
log = hoomd.logging.Logger()
log += lj
gsd.log = log




# The tutorial describes how to construct an initial configuration 'init.gsd'.
# sim.create_state_from_gsd(filename='init.gsd')
sim.state.thermalize_particle_momenta(filter=hoomd.filter.All(), kT=1.5)
sim.run(1e4)
