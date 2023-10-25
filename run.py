import hoomd
from hoomd import md
import numpy as np


nl = hoomd.md.nlist.Cell(buffer = 0.4)
dpd = md.pair.DPD(default_r_cut=1.0, kT=1.0, nlist=nl)
dpd.params[('A', 'A')] = dict(A=10.0, gamma = 4.5)
dpd.params[('A', 'B')] = dict(A=33.7, gamma = 4.5)
dpd.params[('B', 'B')] = dict(A=25.0, gamma = 4.5)
dpd.params[('A', 'W')] = dict(A=75.0, gamma = 20.0)
dpd.params[('B', 'W')] = dict(A=26.3, gamma = 4.5)
dpd.params[('W', 'W')] = dict(A=25.0, gamma = 4.5)

harmonic = hoomd.md.bond.Harmonic()
harmonic.params['AA'] = dict(k=128.0, r0=0.5)
harmonic.params['BB'] = dict(k=4222.6, r0=0.4125)
harmonic.params['AB'] = dict(k=4222.6, r0=0.4125)

cosinesq = hoomd.md.angle.CosineSquared()
cosinesq.params['AAA'] = dict(k=2*30.0, t0=np.pi)
cosinesq.params['AAB'] = dict(k=2*30.0, t0=np.pi)
cosinesq.params['ABB'] = dict(k=2*16.4946, t0=130.0*np.pi/180)
cosinesq.params['BBB'] = dict(k=2*16.4946, t0=130.0*np.pi/180)

gpu = hoomd.device.GPU()
sim = hoomd.Simulation(device=gpu, seed=200)
sim.create_state_from_gsd(filename='init_config.gsd')
integrator = hoomd.md.Integrator(dt=0.01)

nve = hoomd.md.methods.ConstantVolume(filter=hoomd.filter.All())
sim.operations.integrator = integrator
sim.operations.integrator.methods = [nve]
integrator.forces.append(dpd)
integrator.forces.append(harmonic)
integrator.forces.append(cosinesq)

# Set up output
gsd = hoomd.write.GSD(trigger=20, filename='output.gsd')
sim.operations.writers.append(gsd)
log = hoomd.logging.Logger()
log += dpd
gsd.log = log

sim.state.thermalize_particle_momenta(filter=hoomd.filter.All(), kT=0.0)
sim.run(5e4)