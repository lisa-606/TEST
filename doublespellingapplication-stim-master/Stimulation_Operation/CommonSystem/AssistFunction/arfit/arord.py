import numpy as np


def arord(R, m, mcor, ne, pmin, pmax):

    imax = pmax - pmin

    sbc = np.mat(np.zeros((1, imax+1)),dtype=complex)
    fpe = np.mat(np.zeros((1, imax+1)),dtype=complex)
    logdp = np.mat(np.zeros((1, imax+1)),dtype=complex)
    np_m = np.mat(np.zeros((1, imax+1)))

    np_m[0, imax] = m * pmax + mcor

    R22 = R[int(np_m[0, imax]):int(np_m[0, imax])+m, int(np_m[0, imax]):int(np_m[0, imax])+m]

    invR22 = np.linalg.inv(R22)
    Mp = invR22 * invR22.H

    logdp[0, imax] = 2 * np.log(np.abs(np.prod(np.diag(R22))))

    i = imax
    for p in range(pmax, pmin - 1, -1):
        np_m[0, i] = m * p +mcor
        if p < pmax:
            Rp = R[int(np_m[0, i]):int(np_m[0, i]) + m, int(np_m[0, imax]):int(np_m[0, imax]) + m]
            L = np.mat(np.linalg.cholesky(np.identity(m) + Rp * Mp * Rp.H)).H
            N = np.linalg.inv(L.H) * (Rp * Mp)  # !!!!!!!!!!!!!!!!!
            Mp = Mp - N.H * N
            logdp[0, i] = logdp[0, i + 1] + 2 * np.log(np.abs(np.prod(np.diag(L)))+0j)

        sbc[0, i] = logdp[0, i] / m - np.log(ne) * (ne - np_m[0, i]) / ne

        fpe[0, i] = logdp[0, i] / m - np.log(ne*(ne-np_m[0, i])/(ne + np_m[0, i]) + 0j)

        i = i - 1

    return sbc, fpe, logdp, np_m
