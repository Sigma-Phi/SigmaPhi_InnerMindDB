# -*- coding: utf-8 -*-
"""
RCD (Redundancy Compression Dynamics)
可計算模型化版本
將理論轉為可模擬的簡化 stochastic dynamical system
"""

import numpy as np

# =========================
# 1. 系統參數（可調）
# =========================
class RCDParams:
    def __init__(self):
        # 壓縮強度
        self.C = 1.0
        
        # 初始冗餘生成率
        self.R0 = 1.0
        
        # 噪聲強度
        self.sigma = 0.2
        
        # 折疊效率
        self.eta = 0.5
        
        # 時間步長
        self.dt = 0.01


# =========================
# 2. 系統狀態
# =========================
class RCDState:
    def __init__(self, R_init=1.0, S_init=1.0):
        # 冗餘密度 R
        self.R = R_init
        
        # 語義熵 S
        self.S = S_init
        
        # 壓縮後有效表示密度 X
        self.X = 1.0


# =========================
# 3. 動力學核心
# =========================
class RCDSystem:
    def __init__(self, params: RCDParams):
        self.p = params

    def step(self, state: RCDState):
        """
        dR = (冗餘生成 - 壓縮消減 + 噪聲)
        dS = (冗餘增加語義熵，壓縮降低語義熵)
        """

        # ---- 冗餘生成（內生）----
        redundancy_growth = 0.5 * state.R

        # ---- 壓縮作用（外生控制）----
        compression = self.p.C * state.R * self.p.eta

        # ---- 噪聲（W_t）----
        noise = self.p.sigma * np.random.randn()

        # =========================
        # 冗餘動態
        # =========================
        dR = (redundancy_growth - compression) * self.p.dt + noise * np.sqrt(self.p.dt)
        state.R += dR
        state.R = max(state.R, 0.0)  # 防止負值

        # =========================
        # 語義熵動態
        # S ~ 冗餘增加不確定性，壓縮降低不確定性
        # =========================
        dS = (0.3 * state.R - 0.5 * self.p.C) * self.p.dt
        state.S += dS
        state.S = max(state.S, 0.0)

        # =========================
        # 有效表示 X（壓縮結果）
        # =========================
        state.X = state.R / (1.0 + self.p.C)

        return state


# =========================
# 4. 相變判定
# =========================
def regime(state: RCDState, params: RCDParams):
    if params.C < state.R:
        return "HIGH_REDUNDANCY"
    elif abs(params.C - state.R) < 0.2:
        return "CRITICAL"
    elif params.C > state.R and params.C < 2 * state.R:
        return "COMPRESSED"
    elif params.C >= 2 * state.R:
        return "COLLAPSE"
    else:
        return "UNKNOWN"


# =========================
# 5. 模擬器
# =========================
def simulate(steps=500):
    params = RCDParams()
    system = RCDSystem(params)
    state = RCDState()

    history_R = []
    history_S = []
    history_X = []
    history_regime = []

    for _ in range(steps):
        state = system.step(state)

        history_R.append(state.R)
        history_S.append(state.S)
        history_X.append(state.X)
        history_regime.append(regime(state, params))

    return {
        "R": np.array(history_R),
        "S": np.array(history_S),
        "X": np.array(history_X),
        "regime": history_regime
    }


# =========================
# 6. Lyapunov 能量函數
# =========================
def lyapunov(state: RCDState, params: RCDParams):
    """
    V = R - C + σ
    """
    return state.R - params.C + params.sigma


# =========================
# 7. 主程式測試
# =========================
if __name__ == "__main__":
    result = simulate(steps=1000)

    print("Final R:", result["R"][-1])
    print("Final S:", result["S"][-1])
    print("Final X:", result["X"][-1])
    print("Final Regime:", result["regime"][-1])
