# ============================================================
# Noise Folding Control System (NFCS)
# Computational Model Prototype
# ============================================================

import numpy as np

# ------------------------------------------------------------
# 1. System Parameters
# ------------------------------------------------------------

class NFCSConfig:
    def __init__(self):
        self.dt = 0.01              # time step
        self.T = 10.0               # total time

        # noise strength
        self.sigma = 0.5

        # control strength (U_t scale)
        self.alpha = 1.0

        # folding sensitivity
        self.beta = 1.0

        # critical resonance threshold
        self.omega_c = 1.0


# ------------------------------------------------------------
# 2. Core NFCS System
# ------------------------------------------------------------

class NoiseFoldingControlSystem:
    def __init__(self, config: NFCSConfig):
        self.cfg = config

    # --------------------------------------------------------
    # Drift term F(X_t, O_t, U_t)
    # --------------------------------------------------------
    def F(self, x, o, u):
        """
        Deterministic drift:
        - encourages local aggregation + folding
        """
        return -self.cfg.beta * x + self.cfg.alpha * u * np.tanh(o)

    # --------------------------------------------------------
    # Diffusion term G(X_t, O_t, U_t)
    # --------------------------------------------------------
    def G(self, x, o, u):
        """
        Stochastic intensity modulation
        """
        return self.cfg.sigma * (1.0 + 0.1 * np.abs(u))

    # --------------------------------------------------------
    # Observation operator O_t
    # --------------------------------------------------------
    def observe(self, x):
        """
        Partial noisy observation of system state
        """
        noise = np.random.normal(0, 0.1, size=x.shape)
        return x + noise

    # --------------------------------------------------------
    # Control policy U_t
    # --------------------------------------------------------
    def control(self, x, t):
        """
        Simple folding policy:
        tries to stabilize high-energy regions
        """
        return np.sin(t) * np.tanh(x)

    # --------------------------------------------------------
    # One simulation step
    # --------------------------------------------------------
    def step(self, x, t):
        o = self.observe(x)
        u = self.control(x, t)

        drift = self.F(x, o, u)
        diffusion = self.G(x, o, u) * np.random.normal(0, 1, size=x.shape)

        x_next = x + drift * self.cfg.dt + diffusion * np.sqrt(self.cfg.dt)

        return x_next, o, u


# ------------------------------------------------------------
# 3. Simulation Runner
# ------------------------------------------------------------

def run_simulation(dim=1):
    cfg = NFCSConfig()
    system = NoiseFoldingControlSystem(cfg)

    steps = int(cfg.T / cfg.dt)

    x = np.random.randn(dim)  # initial noise state

    trajectory = []

    for t in range(steps):
        time = t * cfg.dt
        x, o, u = system.step(x, time)

        trajectory.append({
            "t": time,
            "x": x.copy(),
            "o": o.copy(),
            "u": u.copy()
        })

    return trajectory


# ------------------------------------------------------------
# 4. Phase Detection (ω_c proxy)
# ------------------------------------------------------------

def detect_phase(trajectory):
    """
    Simple proxy:
    measures stability vs fluctuation ratio
    """

    xs = np.array([p["x"] for p in trajectory])

    variance = np.var(xs, axis=0).mean()
    mean_abs = np.mean(np.abs(xs))

    ratio = mean_abs / (variance + 1e-6)

    if ratio < 0.5:
        phase = "I: high-noise state"
    elif ratio < 1.0:
        phase = "II: folding onset"
    elif ratio < 2.0:
        phase = "III: resonant structure"
    else:
        phase = "IV: controlled condensation"

    return phase, ratio


# ------------------------------------------------------------
# 5. Example Run
# ------------------------------------------------------------

if __name__ == "__main__":
    traj = run_simulation(dim=1)

    phase, score = detect_phase(traj)

    print("NFCS Phase:", phase)
    print("Stability Score:", score)
