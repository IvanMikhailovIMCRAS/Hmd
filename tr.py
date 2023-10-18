import gsd.hoomd
traj = gsd.hoomd.open('trajectory.gsd')
# print(len(traj))

frame = traj[0]
print(frame.configuration.step)
print(frame.particles.N)
print(frame.particles.position)
print(frame.particles.types)
print(f'связи -{frame.bonds.group}')


# for el in traj:
#     print(el.configur)
