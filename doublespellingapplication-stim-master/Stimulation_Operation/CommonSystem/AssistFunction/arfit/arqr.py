import numpy as np


def arqr(v, p, mcor):
    n, m = v.shape

    ne = n - p
    np_m = m * p + mcor
    K = np.mat(np.zeros((ne, np_m+m)),dtype=complex)
    if mcor == 1:
        K[:, 0] = np.ones((ne, 1))

    for j in range(1, p+1):
        K[:, mcor+m*(j-1):mcor+m*j] = v[p-j:n-j, :]

    K[:, np_m:np_m + m] = v[p:n, :]
    q = np_m + m
    delta = (q**2 + q + 1) * np.finfo(np.float64).eps  # !!!!!!!!!!!
    scale = np.sqrt(delta) * np.sqrt(np.sum(np.power(K, 2), axis=0))

    Q, R = np.linalg.qr(np.vstack((K, np.diag(np.array(scale).squeeze()))), mode='complete')
    R = np.mat(np.triu(R),dtype=complex)

    return R, scale