#plot.py

import numpy as np # importing the numpy library as np
import matplotlib.pyplot as plt # importing the matplotlib.pyplot library as plt

def plot_response(simpleback):
    
    res = simpleback.ImpME
    rho = 1e12 * np.abs(res.impedance)**2 / simpleback.freqs[:, None, None]
    rho_err = 1e12 * np.abs(res.error)**2 / simpleback.freqs[:, None, None]
    phi = np.angle(res.impedance, deg=True)
    rad_err = np.arcsin(res.error/abs(res.impedance))
    rad_err[np.isnan(rad_err)] = np.pi
    phi_err = np.rad2deg(rad_err)

    fig = plt.figure()
    ax = plt.subplot(2, 1, 1)
    ax.set_xscale("log", nonpositive='clip')
    ax.set_yscale("log", nonpositive='clip')
    ax.errorbar(simpleback.freqs, rho[:,0,0], yerr=rho_err[:,0,0], fmt='k.', label=r'$\rho_{xx}$')
    ax.errorbar(simpleback.freqs, rho[:,1,1], yerr=rho_err[:,1,1], fmt='g.', label=r'$\rho_{yy}$')
    ax.errorbar(simpleback.freqs, rho[:,0,1], yerr=rho_err[:,0,1], color='red', marker='s', label=r'$\rho_{xy}$')
    ax.plot(simpleback.freqs, rho[:,0,1], color='red')
    ax.errorbar(simpleback.freqs, rho[:,1,0], yerr=rho_err[:,1,0], color='blue', marker='s', label=r'$\rho_{yx}$')
    ax.plot(simpleback.freqs, rho[:,1,0], color='blue')
    plt.grid(axis='y')
    ax.invert_xaxis()
    plt.xlabel('freq')
    plt.ylabel(r'apparent resistivity  $\rho$ ($\Omega.m$)');
    plt.legend()

    plt.title(f'{simpleback.sampling}Hz sampling rate simpleback field prosessing.\n cod={simpleback.cod}, nper={simpleback.nper}, overlap={simpleback.overlap}, min_factor={simpleback.min_factor}, max_factor={simpleback.max_factor}, freqs={simpleback.freq_amount}')
    ax = plt.subplot(2, 1, 2)
    ax.set_xscale("log", nonpositive='clip')
    ax.errorbar(simpleback.freqs, phi[:,0,0], yerr=phi_err[:,0,0], fmt='k.', label=r'$\phi_{xx}$')
    ax.errorbar(simpleback.freqs, phi[:,1,1], yerr=phi_err[:,1,1], fmt='g.', label=r'$\phi_{yy}$')
    ax.errorbar(simpleback.freqs, phi[:,0,1], yerr=phi_err[:,0,1], color='red', marker='s', label=r'$\phi_{xy}$')
    ax.plot(simpleback.freqs, phi[:,0,1], color='red')
    ax.errorbar(simpleback.freqs, phi[:,1,0], yerr=phi_err[:,1,0], color='blue', marker='s', label=r'$\phi_{yx}$')
    ax.plot(simpleback.freqs, phi[:,1,0], color='blue')
    plt.yticks([180, 90, 0, -90, -180])
    plt.grid(axis='y')
    ax.invert_xaxis()
    plt.xlabel('freq')
    plt.ylabel(r'phase $\phi$ (degrees)');
    plt.legend()
    plt.ylim(-180, 180)
    
    return(fig)