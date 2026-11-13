from e_p_2 import sim
import numpy as np
import matplotlib.pyplot as plt




c = 3e8


# fs = np.linspace(1, 40e6, 101)
fs = np.linspace(15e6, 25e6, 51)
# fs = np.array([20e6])
gammas = np.zeros_like(fs)
g_test = []

for idx, f in zip(range(len(fs)), fs):

    wavelength = c / f
    d = 2.96
    offset = 400

    pack_len = 10 * wavelength

    stop_time = (offset + pack_len)/c

    simulation = sim.Simulation(size=1000, dt=1e-10, dx=1e-1, f=f, time_lim=stop_time)

    simulation.add_source(amp=1, f=f, cycles=10)



    simulation.add_slab_m(2, offset, offset+d)
    simulation.add_slab_m(3, offset+d, offset+2*d)
    simulation.add_slab_m(2, offset+2*d, offset+3*d)



    e = sim.run_simulation(simulation, plot=False)
    
    gammas[idx] = np.max(e[int((offset-pack_len*0.6)/simulation.dx):int((offset-pack_len*0.4)/simulation.dx)])
    g_test.append(e)


plt.plot(fs/1e6, gammas)
# plt.plot(np.linspace(0, 1, len(g_test[0])), g_test[0])
plt.xlabel('Frequency (MHz)')
plt.ylabel('|Gamma|')
# plt.ylabel('E-Field Amplitude')
# plt.xlabel('Distance in meters')
plt.show()