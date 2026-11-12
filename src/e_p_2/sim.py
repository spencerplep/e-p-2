# contains siml\ulation utilities


import numpy as np
import pyqtgraph as pg


# Constants
u0 = 4 * np.pi * 1e-7  # Permeability of free space (H/m)
e0 = 8.854187817e-12  # Permittivity of free space (F/m)
c = 1 / np.sqrt(u0 * e0)  # Speed of light in vacuum (m/s)

class Simulation:
    def __init__(self, dx=None, dt=None, size=None, time_lim=None, source=None, s=None, f=10e6, plot_interval=1000):
        # Try to specify f at least.

        self.dx = dx            # X step
        self.dt = dt            # Time step
        self.size = size        # Space size in meterss
        self.time_lim = time_lim # Time limit
        if self.time_lim is None:
            self.time_lim = self.size / c *1.5
        self.source = source
        self.s = s
        self.plot_interval = plot_interval

        if self.s is None:
            self.s = 0.7
        
        self.f = f

        self.wave_length = c / self.f

        if self.dx is not None and self.dt is not None:
            print("S calculated as", c*self.dt/self.dx)

        if f is not None and self.dt is None:
            self.dt = 1 / (self.f * 50)
            print("Set dt automatically")

        if self.dt is not None and self.dx is None:
            self.dx = c * self.dt / self.s
            print("Set dx automatically")


    
        # initialize space array
        self.e = np.zeros(int(self.size / self.dx))

        print(self.e.shape)
        # self.e_offset = int(self.size/self.dx)
        self.e_last = self.e
        # er array
        self.er = np.ones_like(self.e)

        if self.source is not None:
            self.add_source(self.source['amp'], self.source['f'], self.source['t0'], self.source['cycles'])

    def add_slab(self, er, start, end):
        # Add a slab of material with relative permittivity er between start and end indices
            start_index = int(np.floor(start))
            end_index = int(np.ceil(end))

            self.er[start_index:end_index] = er

    def add_slab_m(self, er, start, end):
        self.add_slab(er, start/self.dx, end/self.dx)

    def add_source(self, amp, f, t0=None, cycles=3):
        
        if t0 is None:
            t0 = (1/f) * cycles

        self.source = {'amp': amp, 'f': f, 't0': t0, 'cycles': cycles}



def update(e, e_last, er, dt, dx):
    # Update the electric field using the finite-difference time-domain (FDTD) method
    c = 1 / np.sqrt(u0 * e0)  # Speed of light in vacuum (m/s)

    e_next = np.zeros_like(e)
    e_next[1:-1] = (c**2 * dt**2 / dx**2) * (e[2:] - 2 * e[1:-1] + e[:-2]) / er[1:-1] + 2 * e[1:-1] - e_last[1:-1]

    return e_next

def run_simulation(sim, plot=True):

    # Initialize variables
    e = sim.e.copy()
    e_last = sim.e_last.copy()
    er = sim.er.copy()
    dt = sim.dt
    dx = sim.dx
    # offset = sim.e_offset
    plot_interval = sim.plot_interval

    # Time-stepping loop
    t = 0
    time_step = 0

    # Apply source
    if sim.source is not None:
        t0 = sim.source['t0']
        amp = sim.source['amp']
        f = sim.source['f']
        cycles = sim.source['cycles']
        has_source = True
    else:
        has_source = False

    if plot:
        app = pg.mkQApp()
        window = pg.PlotWidget(title="FDTD Simulation")
        window.show()
        window.setYRange(-2, 2, padding=0)
        curve = window.plot(e, pen='b')

        # x = np.arange(0, sim.size, sim.dx)


    while t < sim.time_lim:
        # Update the electric field
        e_next = update(e, e_last, er, dt, dx)

        if has_source and t <= t0:
            source_value = amp * np.sin(2 * np.pi * f * t) * np.exp(-1/2*((t-t0/2)/(0.2))**2)/(0.2*np.sqrt(2*np.pi))/2
            e_next[0] = source_value
        else:
            e_next[0] = 0

        # Update fields for next iteration
        e_last[:] = e
        e[:] = e_next

        # Increment time
        t += dt
        time_step += 1
        # print(t)

        if plot:
            if time_step % (plot_interval) < dt:
                curve.setData(e)
                app.processEvents()


    
    return e








