import numpy as np
import matplotlib.pyplot as plt

# =========================
# CCNPT - Channel Capacity Control Network Phase Transition Model
# =========================

class CCNPTSystem:
    def __init__(self,
                 capacity=100.0,
                 alpha=0.05,   # pressure growth rate
                 beta=0.08,    # control response strength
                 gamma=0.06,   # network coupling growth
                 noise=0.5,
                 seed=42):

        np.random.seed(seed)

        # Base parameters
        self.C = capacity

        # State variables
        self.P = 10.0     # pressure P_t
        self.U = 5.0      # control field U_t
        self.K = 1.0      # connectivity K_t

        # parameters
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.noise = noise

        # history
        self.history = {
            "P": [],
            "U": [],
            "K": [],
            "regime": []
        }

    # -------------------------
    # Phase detection (order parameter λ_t)
    # -------------------------
    def phase(self):
        lam = self.P / (self.C + 1e-9)

        if lam < 0.7:
            return "EXPANSION"
        elif lam < 1.1:
            return "CONTROL"
        else:
            return "NETWORK"

    # -------------------------
    # Control dynamics U_t
    # -------------------------
    def update_control(self):
        # control reacts to pressure but saturates
        self.U += self.beta * (self.P - self.U)

        # saturation
        self.U = np.clip(self.U, 0, self.C)

    # -------------------------
    # Network dynamics K_t
    # -------------------------
    def update_network(self):
        regime = self.phase()

        if regime == "NETWORK":
            growth = self.gamma * (self.P - self.C)
        elif regime == "CONTROL":
            growth = self.gamma * 0.3 * (self.P / self.C)
        else:
            growth = self.gamma * 0.05

        noise = np.random.randn() * self.noise
        self.K += growth + noise

        # prevent collapse
        self.K = max(self.K, 0.1)

    # -------------------------
    # Pressure dynamics P_t
    # -------------------------
    def update_pressure(self):
        # external inflow + stochasticity
        inflow = self.alpha * self.P

        # control reduces pressure
        dissipation = 0.03 * self.U

        noise = np.random.randn() * self.noise

        self.P += inflow - dissipation + noise

        # avoid negative
        self.P = max(self.P, 0.1)

    # -------------------------
    # one simulation step
    # -------------------------
    def step(self):
        self.update_pressure()
        self.update_control()
        self.update_network()

        self.history["P"].append(self.P)
        self.history["U"].append(self.U)
        self.history["K"].append(self.K)
        self.history["regime"].append(self.phase())

    # -------------------------
    # run simulation
    # -------------------------
    def run(self, T=200):
        for _ in range(T):
            self.step()
        return self.history


# =========================
# Visualization
# =========================

def plot_results(history):
    P = history["P"]
    U = history["U"]
    K = history["K"]

    t = np.arange(len(P))

    plt.figure(figsize=(12, 6))

    plt.plot(t, P, label="Pressure P_t", linewidth=2)
    plt.plot(t, U, label="Control U_t", linewidth=2)
    plt.plot(t, K, label="Network K_t", linewidth=2)

    plt.axhline(y=100, linestyle="--", color="gray", label="Capacity C")

    plt.title("CCNPT Simulation: Pressure-Control-Network Phase Transition")
    plt.xlabel("Time")
    plt.ylabel("State Value")
    plt.legend()
    plt.grid(True)

    plt.show()


# =========================
# Example run
# =========================

if __name__ == "__main__":
    system = CCNPTSystem(capacity=100)

    history = system.run(T=300)

    plot_results(history)

    # Print final regime
    print("Final regime:", history["regime"][-1])
