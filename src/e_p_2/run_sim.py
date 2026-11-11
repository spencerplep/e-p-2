from e_p_2 import sim


fs = 10e9

simulation = sim.Simulation(plot_interval = 1, size=5, dt=1e-12, dx=1e-6,f=fs)

simulation.add_source(amp=1, f=fs, cycles=5)
simulation.add_slab_m(10, 2.5, 2.5+1)

sim.run_simulation(simulation)