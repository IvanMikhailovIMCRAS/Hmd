import hoomd
from hoomd import md


nl = hoomd.md.nlist.Cell(buffer = 0.4)
dpd = md.pair.DPD(default_r_cut=1.0, kT=1.0, nlist=nl)
dpd.params[('A', 'A')] = dict(A=25.0, gamma = 4.5)
dpd.params[('A', 'B')] = dict(A=25.0, gamma = 4.5)
dpd.params[('B', 'B')] = dict(A=25.0, gamma = 4.5)
dpd.params[('A', 'W')] = dict(A=25.0, gamma = 4.5)
dpd.params[('B', 'W')] = dict(A=25.0, gamma = 4.5)
dpd.params[('W', 'W')] = dict(A=25.0, gamma = 4.5)

harmonic = hoomd.md.bond.Harmonic()
harmonic.params['AA'] = dict(k=128.0, r0=0.5)
harmonic.params['BB'] = dict(k=4222.6, r0=0.4125)
harmonic.params['AB'] = dict(k=4222.6, r0=0.4125)

# angle = hoomd.md.angle.Harmonic()
# angle.params['CCC'] = dict(k=2*58.35, t0=112.7 * pi / 180)
# angle.params['CCH'] = dict(k=2*37.5, t0=110.7 * pi / 180)
# angle.params['HCH'] = dict(k=2*33.0, t0=107.8 * pi / 180)

# harmonic = hoomd.md.bond.harmonic()
# harmonic.bond_coeff.set('polymer', k=330.0, r0=0.84)
gpu = hoomd.device.GPU()
sim = hoomd.Simulation(device=gpu, seed=200)
sim.create_state_from_gsd(filename='init_config.gsd')
integrator = hoomd.md.Integrator(dt=0.01)

nve = hoomd.md.methods.ConstantVolume(filter=hoomd.filter.All())
sim.operations.integrator.methods = [nve]
sim.operations.integrator = integrator
integrator.forces.append(dpd)

# Set up output
gsd = hoomd.write.GSD(trigger=100, filename='output.gsd')
sim.operations.writers.append(gsd)
log = hoomd.logging.Logger()
log += dpd
gsd.log = log


sim.state.thermalize_particle_momenta(filter=hoomd.filter.All(), kT=1.0)
sim.run(1e3)