import numpy as np
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.AssistFunction.arfit.arord import arord
from doubleSpellingApplication.Stimulation_Operation.CommonSystem.AssistFunction.arfit.arqr import arqr


def arfit(v, pmin, pmax, selector, no_const):

    n, m = v.shape
    if type(pmin) is not int or type(pmax) is not int:
        print("error: Order must be integer.")

    if pmax < pmin:
        print("error: PMAX must be greater than or equal to PMIN.")

    if selector is None:
        mcor = 1
        selector = 'sbc'

    elif no_const is None:
        if selector is 'zero':
            mcor = 0
            selector = 'sbc'
        else:
            mcor = 1
    else:
        if no_const is 'zero':
            mcor = 0
        else:
            print("error: Bad argument. Usage:  [w,A,C,SBC,FPE,th]=AR(v,pmin,pmax,SELECTOR,''zero'')")

    ne = n - pmax
    npmax = m * pmax + mcor

    if ne <= npmax:
        print("Time series too short.")

    R, scale = arqr(v, pmax, mcor)

    sbc, fpe, logdp, notuse = arord(R, m, mcor, ne, pmin, pmax)

    val = eval(selector).min(0)
    iopt = np.argmin(eval(selector))

    popt = pmin + iopt  # !!!!!!!!!!
    np_m = (m) * popt + mcor  # !!!!!!!!!!!

    R11 = R[0:np_m, 0:np_m]
    R12 = R[0:np_m, npmax:npmax+m]
    R22 = R[np_m:npmax+m, npmax:npmax+m]

    if np_m > 0:
        if mcor == 1:
            con = scale[1:npmax+m] / scale[0]  # !!!!!!!!!!
            R11[:,0] = R11[:, 0] * con
        Aaug = (np.linalg.inv(R11)*R12).H

        if mcor == 1:
            w = Aaug[:, 0]*con
            A = Aaug[:, 1:np_m]
        else:
            w = np.mat(np.zeros((m, 1)))
            A = Aaug  # np.mat(np.zeros((0, 0)))
    else:
        w = np.mat(np.zeros((m, 1)))
        A = np.mat(np.zeros((0, 0)))

    dof = ne - np_m
    C = R22.H * R22 / dof

    invR11 = np.linalg.inv(R11)
    if mcor == 1:
        invR11[0, :] = invR11[0, :] * con

    Uinv = invR11 * invR11.H
    th =np.hstack((np.mat(dof),np.mat(np.zeros((1, Uinv.shape[1]-1)))))
    th = np.vstack((th, Uinv))
    return w, A, C, sbc, fpe, th
