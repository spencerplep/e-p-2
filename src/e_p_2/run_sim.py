from e_p_2 import sim


fs = 20e6
wavelength = 3e8 / fs

simulation = sim.Simulation(plot_interval = 10, s=0.4, size=600, dt=1e-10, dx=1e-1, f=fs)

simulation.add_source(amp=1, f=fs, cycles=10)

d = 2.96
offset = 150

simulation.add_slab_m(2, offset, offset+d)
simulation.add_slab_m(3, offset+d, offset+2*d)
simulation.add_slab_m(2, offset+2*d, offset+3*d)



sim.run_simulation(simulation)