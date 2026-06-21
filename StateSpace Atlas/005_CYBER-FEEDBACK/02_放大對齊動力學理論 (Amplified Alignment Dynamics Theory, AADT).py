這是一個關於 **放大對齊動力學理論 (AADT)** 的 Python 計算模型實現。
本模型採用 **基於代理人的模擬 (Agent-Based Modeling, ABM)** 方法，將系統中的狀態定義為多維空間中的個體。透過計算個體間的對齊程度來迭代演化，進而觀察從 Diffuse State 到 Lock-in State 的相變過程。
### Python 實作程式碼
```python
import numpy as np
import matplotlib.pyplot as plt

class AADT_Simulation:
    def __init__(self, num_agents=100, alpha=0.5, beta=0.3, steps=200):
        self.num_agents = num_agents
        self.alpha = alpha  # 放大係數
        self.beta = beta    # 抑制係數
        self.steps = steps
        # 初始化個體狀態 (在 -1 到 1 的一維空間)
        self.states = np.random.uniform(-1, 1, num_agents)
        self.history = []

    def calculate_alignment_density(self):
        # 以平均狀態的偏離度倒數作為對齊密度的代理指標
        return 1 / (np.std(self.states) + 0.1)

    def run(self):
        for _ in range(self.steps):
            self.history.append(self.states.copy())
            
            # 計算當前對齊密度
            A = self.calculate_alignment_density()
            
            # 核心動力方程: dX = (alpha * A - beta) * X + noise
            # 簡化模擬: 趨向於群體中心 (對齊) 的力
            center = np.mean(self.states)
            noise = np.random.normal(0, 0.05, self.num_agents)
            
            # 演化規則
            self.states += (self.alpha * A - self.beta) * (center - self.states) * 0.1 + noise
            
            # 邊界限制
            self.states = np.clip(self.states, -1, 1)

    def plot_results(self):
        plt.figure(figsize=(10, 6))
        for i in range(self.num_agents):
            plt.plot([h[i] for h in self.history], color='blue', alpha=0.1)
        plt.title(f"AADT Evolution (Alpha: {self.alpha}, Beta: {self.beta})")
        plt.xlabel("Time Steps")
        plt.ylabel("Agent States")
        plt.show()

# --- 執行模擬 ---
# 設置 alpha > beta 進入正回饋階段
sim = AADT_Simulation(alpha=0.8, beta=0.2)
sim.run()
sim.plot_results()

```
### 模型說明
 1. **狀態向量 (X_t)**：在程式中以 self.states 表示，代表代理人在決策空間的位置。
 2. **核心動力 (F(X_t))**：透過 (self.alpha * A - self.beta) * (center - self.states) 實現。這表示當對齊密度 (A) 足夠大時，系統會產生一個「向心力」，將離散狀態強行拉向群體共識。
 3. **相變模擬**：
   * 若你將 alpha 設得遠大於 beta，你會看到所有線條迅速收斂到中心（鎖定態）。
   * 若你將 beta 設得大於 alpha，個體狀態將維持在隨機分布（擴散態）。
### 進階優化建議
 * **高維擴展**：將 self.states 從一維向量改為 (num_agents, dimension) 的矩陣，即可模擬在多維度決策空間下的對齊效應。
 * **動態 (U_t)**：可以在 run 的迴圈中加入 if 判斷，例如當 step > 100 時改變 beta，模擬外部政策干預（如打破壟斷或引入競爭）對系統路徑依賴的破壞。
