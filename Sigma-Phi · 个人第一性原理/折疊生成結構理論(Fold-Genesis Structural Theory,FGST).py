為了將 **Fold-Genesis Structural Theory (FGST)** 轉化為可執行的 Python 模擬程式，我們將系統建模為一個離散時間的隨機動力系統。
這裡使用 numpy 來模擬狀態演化，透過隨機遊走（Random Walk）加上折疊回流機制，觀察系統在不同折疊率下的行為。
### Python 實作：FGST 數值模擬器
```python
import numpy as np
import matplotlib.pyplot as plt

class FGST_Simulator:
    def __init__(self, steps=1000, alpha=0.1, beta=0.05, gamma=0.02):
        self.steps = steps
        self.alpha = alpha  # 展開驅動
        self.beta = beta    # 穩定係數
        self.gamma = gamma  # 折疊回流
        
        # 狀態初始化 (G, E, F, D)
        self.X = np.zeros((steps, 4))
        self.X[0] = [1.0, 0.5, 0.5, 0.1] # 初始狀態

    def step_dynamics(self, t):
        # 取出當前狀態
        g, e, f, d = self.X[t]
        
        # 計算理解效率 R_t
        r_t = f / (e + d + 1e-6)
        
        # 動力學模擬：簡化版梯度下降
        # 展開增加複雜度，折疊減少複雜度，漂移是殘差
        de = self.alpha * np.random.normal(0.5, 0.2) # 隨機展開
        df = self.gamma * (r_t - 1.0) * f            # 折疊回流機制
        dd = self.beta * (abs(r_t - 1.0))            # 漂移隨不平衡累積
        
        # 更新下一狀態
        self.X[t+1] = [g, max(0, e + de), max(0, f + df), d + dd]

    def run(self):
        for t in range(self.steps - 1):
            self.step_dynamics(t)
        return self.X

# 執行模擬
sim = FGST_Simulator()
data = sim.run()

# 繪製模擬結果
plt.figure(figsize=(10, 6))
plt.plot(data[:, 1], label='Expansion (E)')
plt.plot(data[:, 2], label='Folding (F)')
plt.title("FGST System Evolution: Expansion vs Folding")
plt.xlabel("Time Step")
plt.ylabel("Magnitude")
plt.legend()
plt.show()

```
### 理論執行邏輯解析
這個程式碼體現了 FGST 的幾個核心計算邏輯：
 1. **狀態向量更新**：self.X 陣列維護了系統在 t 時間的四維坐標，這是所有計算的基礎。
 2. **回流機制（Feedback Loop）**：
   * 程式中的 df = self.gamma * (r_t - 1.0) * f 實現了您定義的臨界折疊回流。當 R_t > 1（過折疊）時，折疊力會減弱；當 R_t < 1（過展開）時，折疊力會增強，這正是系統趨向「臨界態」的動力源。
 3. **結構漂移（Drift Calculation）**：
   * dd = self.beta * (abs(r_t - 1.0)) 體現了漂移隨效率偏差而擴大的特性，這模擬了如果不進行有效折疊，系統誤差會不斷積累的現象。
