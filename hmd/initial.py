import numpy as np
import gsd
import gsd.hoomd
import hoomd

print(gsd.version.version)

L = 15.0
N_a = 5
N_b = 3
N_pol = 100
N_wat = int(L**3 * 3  - (N_a+N_b) * N_pol)
N = N_wat + (N_a+N_b) * N_pol
types_id = np.zeros(N, dtype = int)
coords = np.zeros(shape = (N, 3))
bonds = []
angles = []
k_a = 128.0
k_b = 4222.6
l_a = 0.5
l_b = 0.4125
k_theta_a = 30.0
k_theta_b = 32.9892
theta_0 = 130.0

def rand_vec(length):
    r = 0.5 - np.random.random(3)
    sum = np.sum(r**2)
    r = r/sum * length
    return r

def periodic_box(coords, box):
    for i in range(3):
        if abs(coords[i]) > 0.5 * box:
            coords[i] = coords[i] - np.sign(coords[i]) * box
    return coords

iter = -1
for i in range(N_pol):
    iter += 1
    coords[iter] = L/2 - L*np.random.random(3)
    types_id[iter] = 0
    for j in range(1, N_a):
        iter += 1
        coords[iter] = periodic_box(coords[iter-1] + rand_vec(l_a), L)
        types_id[iter] = 0
        bonds.append([iter-1, iter])
        angles.append([iter-1, iter, iter+1])


    for j in range(0, N_b):
        iter += 1
        coords[iter] = periodic_box(coords[iter-1] + rand_vec(l_b), L)
        types_id[iter] = 1
        bonds.append([iter-1, iter])
        if j < N_b - 1:
            angles.append([iter-1, iter, iter+1])
    
for i in range(N_wat):
    iter += 1
    coords[iter] =  L/2 - L*np.random.random(3)
    types_id[iter] = 2

bonds = np.array(bonds)
angles = np.array(angles)

snapshot = gsd.hoomd.Frame()
snapshot.particles.N = N
snapshot.configuration.box = hoomd.Box.cube(L)
snapshot.bonds.N = len(bonds)
snapshot.angles.N = len(angles)

snapshot.configuration.box = [L, L, L, 0, 0, 0]
snapshot.particles.types = ['A', 'B', 'W']
snapshot.bonds.types = ['AA', 'AB', 'BB']
snapshot.angles.types = ['AAA', 'AAB', 'ABB', 'BBB']

snapshot.particles.typeid = types_id
snapshot.particles.position = coords[:]
snapshot.particles.mass = np.array([1.0] * N)
snapshot.bonds.group = bonds
snapshot.bonds.typeid = np.zeros(len(bonds))
for i in range(len(bonds)):
    snapshot.bonds.typeid[i] = types_id[bonds[i, 0]] + types_id[bonds[i, 1]]
snapshot.angles.group = angles
snapshot.angles.typeid = np.zeros(len(angles))
for i in range(len(angles)):
    snapshot.angles.typeid[i] = types_id[angles[i, 0]] + types_id[angles[i, 1]] + types_id[angles[i, 2]]

with gsd.hoomd.open(name='init_config.gsd', mode='w') as f:
    f.append(snapshot)

print(coords)