from lprec import lpTransform
import numpy as np
import struct


def test_adj():
    N = 512
    Nproj = int(3*N/2)
    Nslices = 1
    filter_type = 'None'
    cor = N / 2
    interp_type = 'cubic'
    gpu = 0

    f = np.float32(np.random.random([Nslices, N, N]))
    R = np.float32(np.random.random([Nslices, Nproj, N]))

    lp = lpTransform.lpTransform(
        N, Nproj, Nslices, filter_type, cor, interp_type)
    lp.precompute(1)
    lp.initcmem(1, gpu)

    Rf = lp.fwd(f, gpu)
    frec = lp.adj(R, gpu)
    Rrec = lp.fwd(frec, gpu)

    # scale test
    RR = lp.fwd(lp.adj(R, gpu), gpu)
    scale = np.sum(np.float64(R*RR))/np.sum(np.float64(RR*RR))

    # dot product test
    sum1 = sum(np.float64(np.ndarray.flatten(Rrec)*np.ndarray.flatten(R)))
    sum2 = sum(np.float64(np.ndarray.flatten(frec)*np.ndarray.flatten(frec)))
    err = np.linalg.norm(sum1-sum2)/np.linalg.norm(sum2)
    print([scale, err])
    return [scale, err]


if __name__ == '__main__':
    test_adj()
