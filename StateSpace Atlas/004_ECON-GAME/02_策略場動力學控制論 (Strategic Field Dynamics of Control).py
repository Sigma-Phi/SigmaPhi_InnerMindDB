這是一個基於**策略場動力學控制論 (SFDC)** 構建的基礎計算模型。此模型使用 Langevin 方程的離散化形式（歐拉-馬力歐方法）來模擬系統狀態在策略空間中的演化。
### Python 計算模型：SFDC 模擬器
```python
import numpy as np
import matplotlib.pyplot as plt

class StrategicFieldDynamics:
    def __init__(self, alpha, beta, sigma, dt=0.01, steps=1000):
        """
        alpha: 策略擴張推力
        beta: 約束壓縮力
        sigma: 隨機波動強度 (G)
        """
        self.alpha = alpha
        self.beta = beta
        self.sigma = sigma
        self.dt = dt
        self.steps = steps
        
    def drift(self, x):
        """
        定義漂移項 F(X_t): 傾向於擴張與收縮的平衡
        這裡假設一個簡單的勢能場 V(x) = beta/2 * x^2 - alpha * ln(1 + x^2)
        """
        return - (self.beta * x) + (self.alpha * x / (1 + x**2))

    def simulate(self, x0=0.5):
        history = [x0]
        x = x0
        for _ in range(self.steps):
            # dX_t = F(X_t)dt + G * dW_t
            f = self.drift(x)
            dw = np.random.normal(0, np.sqrt(self.dt))
            x += f * self.dt + self.sigma * dw
            history.append(x)
        return np.array(history)

# --- 模擬設定 ---
# 比較不同參數下的演化狀態
sim1 = StrategicFieldDynamics(alpha=1.5, beta=1.0, sigma=0.2) # 擴張相
sim2 = StrategicFieldDynamics(alpha=0.5, beta=1.5, sigma=0.2) # 收縮相
sim3 = StrategicFieldDynamics(alpha=1.0, beta=1.0, sigma=0.5) # 臨界/噪聲相

h1 = sim1.simulate()
h2 = sim2.simulate()
h3 = sim3.simulate()

# --- 繪圖呈現 ---
plt.figure(figsize=(10, 6))
plt.plot(h1, label='Expansion Phase (a > b)')
plt.plot(h2, label='Compression Phase (b > a)')
plt.plot(h3, label='Critical/Noise Phase (a ~ b)')
plt.title("Strategic Field Dynamics Simulation")
plt.xlabel("Time Step")
plt.ylabel("Strategy State (X_t)")
plt.legend()
plt.grid(True)
plt.show()

```
### 模型說明與邏輯擴展
 1. **漂移函數 drift(x)**：
   * 我將系統勢能設定為一個非線性結構。當 alpha 高時，函數會產生「排斥」原點的趨勢（擴張）；當 beta 高時，函數會將狀態「吸引」回原點（收縮）。
   * 這是為了體現你在理論中提到的「策略空間」邊界效應。
 2. **隨機項 dW_t**：
   * 使用了 np.random.normal(0, np.sqrt(dt)) 來模擬布朗運動（Wiener Process）。這反映了你在理論中提到的資訊不完整與突發擾動。
 3. **可擴展性建議**：
   * **多代理系統 (MAS)**：如果你想將此模型推廣到 N 個行動體，可以將 x 改為一個大小為 N 的向量，並在 drift 函數中加入一個交互矩陣 A_{ij} 來計算「權力梯度」對單個行動體 X_i 的影響。
   * **回饋延遲 (\tau)**：你可以引入一個 collections.deque 結構來記錄過去的狀態，讓當前的漂移 drift 取決於 history[t - tau] 而非 history[t]，這將直接模擬延遲帶來的系統振盪或不穩定性。
此代碼提供了一個基礎的框架，你可以直接執行並透過修改 alpha 與 beta 的數值來觀察系統如何從穩定收斂轉向發散或混沌漂移。
