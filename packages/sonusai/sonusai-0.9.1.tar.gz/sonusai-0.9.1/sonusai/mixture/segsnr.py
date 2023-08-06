import numpy as np

from sonusai.mixture.mixdb import MRecord
from sonusai.mixture.mixdb import MixtureDatabase


def generate_segsnr(mixdb: MixtureDatabase,
                    mrecord: MRecord,
                    target_audio: np.ndarray,
                    noise_audio: np.ndarray,
                    compute: bool = True,
                    frame_based: bool = False) -> np.ndarray:
    """Generate segmental SNR."""
    from pyaaware import ForwardTransform

    from sonusai.utils import int16_to_float

    if not compute:
        return np.empty(0, dtype=np.single)

    fft = ForwardTransform(N=mixdb.ftransform.N, R=mixdb.ftransform.R, ttype=mixdb.ftransform.ttype)

    if frame_based:
        segsnr = np.empty(mrecord.samples // mixdb.ftransform.R, dtype=np.single)
    else:
        segsnr = np.empty(mrecord.samples, dtype=np.single)

    frame = 0
    for offset in range(0, mrecord.samples, mixdb.ftransform.R):
        indices = slice(offset, offset + mixdb.ftransform.R)

        target_energy = fft.energy_t(int16_to_float(target_audio[indices]))
        noise_energy = fft.energy_t(int16_to_float(noise_audio[indices]))

        if noise_energy == 0:
            snr = np.single(np.inf)
        else:
            snr = np.single(target_energy / noise_energy)

        if frame_based:
            segsnr[frame] = snr
            frame += 1
        else:
            segsnr[indices] = snr

    return segsnr
