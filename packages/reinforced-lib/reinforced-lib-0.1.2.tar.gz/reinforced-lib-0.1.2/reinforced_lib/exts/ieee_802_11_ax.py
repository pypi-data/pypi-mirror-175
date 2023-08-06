import gym.spaces
import numpy as np
from jax.scipy.special import erf

from reinforced_lib.exts import BaseExt, observation, parameter


class IEEE_802_11_ax(BaseExt):
    """
    IEEE 802.11ax [1]_ extension. Provides data rates (in Mb/s) for consecutive MCS (modulation and coding scheme)
    modes, minimal SNR (signal-to-noise ratio) for each MCS, approximated collision probability for a given number
    of transmitting stations, and approximated transmission success probability for a given SNR and all MCS modes.

    References
    ----------
    .. [1] "IEEE Standard for Information Technology--Telecommunications and Information Exchange between Systems
       Local and Metropolitan Area Networks--Specific Requirements Part 11: Wireless LAN Medium Access Control
       (MAC) and Physical Layer (PHY) Specifications Amendment 1: Enhancements for High-Efficiency WLAN,"
       in IEEE Std 802.11ax-2021 (Amendment to IEEE Std 802.11-2020) , vol., no., pp.1-767,
       19 May 2021, doi: 10.1109/IEEESTD.2021.9442429.

    """

    observation_space = gym.spaces.Dict({
        'time': gym.spaces.Box(0.0, np.inf, (1,)),
        'n_successful': gym.spaces.Box(0, np.inf, (1,), np.int32),
        'n_failed': gym.spaces.Box(0, np.inf, (1,), np.int32),
        'n_wifi': gym.spaces.Box(1, np.inf, (1,), np.int32),
        'power': gym.spaces.Box(-np.inf, np.inf, (1,)),
        'cw': gym.spaces.Discrete(32767),
        'mcs': gym.spaces.Discrete(12)
    })

    _wifi_modes_rates = np.array([
        7.3,
        14.6,
        21.9,
        29.3,
        43.9,
        58.5,
        65.8,
        73.1,
        87.8,
        97.5,
        109.7,
        121.9
    ], dtype=np.float32)

    _wifi_phy_rates = np.array([
        6.8,
        13.6,
        20.4,
        27.2,
        40.8,
        54.6,
        61.3,
        68.1,
        81.8,
        90.9,
        101.8,
        112.5
    ], dtype=np.float32)

    _wifi_modes_snrs = np.array([
        -0.0105,
        2.92567,
        6.04673,
        8.98308,
        12.5948,
        16.4275,
        17.9046,
        19.6119,
        23.5752,
        24.8097,
        31.2291,
        33.1907,
    ], dtype=np.float32)

    @observation(observation_type=gym.spaces.Box(0.0, np.inf, (len(_wifi_modes_rates),)))
    def rates(self, *args, **kwargs) -> np.ndarray:
        return self._wifi_modes_rates

    @observation(observation_type=gym.spaces.Box(-np.inf, np.inf, (len(_wifi_modes_snrs),)))
    def min_snrs(self, *args, **kwargs) -> np.ndarray:
        return self._wifi_modes_snrs

    @observation(observation_type=gym.spaces.Box(-np.inf, np.inf, (len(_wifi_modes_rates),)))
    def context(self, *args, **kwargs) -> np.ndarray:
        return self.rates()

    @observation(observation_type=gym.spaces.Box(0.0, 1.0, (1,)))
    def collision_probability(self, n_wifi: int, *args, **kwargs) -> float:
        return 0.154887 * np.log(1.03102 * n_wifi)

    @observation(observation_type=gym.spaces.Box(0.0, 1.0, (len(_wifi_modes_rates),)))
    def success_probability(self, snr: float, *args, **kwargs) -> np.ndarray:
        return 0.5 * (1 + erf(2 * (snr - self._wifi_modes_snrs)))

    @observation(observation_type=gym.spaces.Discrete(len(_wifi_modes_rates)))
    def action(self, mcs: int, *args, **kwargs) -> int:
        return mcs

    @observation(observation_type=gym.spaces.Box(-np.inf, np.inf, (1,)))
    def reward(self, mcs: int, n_successful: int, n_failed: int, *args, **kwargs) -> float:
        if n_successful + n_failed > 0:
            return self._wifi_phy_rates[mcs] * n_successful / (n_successful + n_failed)
        else:
            return 0.0

    @parameter(parameter_type=gym.spaces.Box(1, np.inf, (1,), np.int32))
    def n_arms(self) -> int:
        return self.n_mcs()

    @parameter(parameter_type=gym.spaces.Box(1, np.inf, (1,), np.int32))
    def n_mcs(self) -> int:
        return len(self._wifi_modes_rates)

    @parameter(parameter_type=gym.spaces.Box(-np.inf, np.inf, (1,)))
    def min_snr(self) -> float:
        return 0.0

    @parameter(parameter_type=gym.spaces.Box(-np.inf, np.inf, (1,)))
    def max_snr(self) -> float:
        return 40.0

    @parameter(parameter_type=gym.spaces.Box(-np.inf, np.inf, (1,)))
    def initial_power(self) -> float:
        return 16.0206
