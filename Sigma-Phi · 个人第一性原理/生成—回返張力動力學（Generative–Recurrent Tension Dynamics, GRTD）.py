這是一個基於 **GRTD (Generative–Recurrent Tension Dynamics)** 理論所編寫的 Python 模擬框架。
我使用了 numpy 來實現受控隨機動力系統，並模擬一個簡化的 d 維空間認知代理。此代碼包含了系統狀態演化、控制驅動力平衡以及相變監測。
```python
import numpy as np
import matplotlib.pyplot as plt

class GRTDSimulator:
    """
    生成—回返張力動力學 (GRTD) 模擬器
    模擬認知系統在生成與回返驅動下的狀態演化
    """
    def __init__(self, d=10, alpha=1.0, beta=1.0):
        self.d = d              # 狀態維度
        self.alpha = alpha      # 生成強度
        self.beta = beta        # 回返強度
        self.X = np.random.randn(d) # 初始狀態 X_t

    def step(self, dt=0.01):
        # 模擬生成力: 驅動擴張 (exploration)
        # 這裡簡化為隨機擾動後的梯度效應
        U_G = np.random.randn(self.d) * self.alpha
        
        # 模擬回返力: 驅動壓縮 (compression/stabilization)
        # 傾向於將狀態拉向原點 (穩定性)
        U_V = -self.X * self.beta
        
        # 更新狀態 (dX_t = F(...)dt + G(X_t)dW_t)
        # 簡化方程: dX = (U_G + U_V)dt + noise
        noise = np.random.normal(0, 0.1, self.d) * np.sqrt(dt)
        self.X += (U_G + U_V) * dt + noise
        
        # 計算張力指標 T_t = ||U_G||^2 - ||U_V||^2
        tension = np.linalg.norm(U_G)**2 - np.linalg.norm(U_V)**2
        spread = np.var(self.X)
        
        return tension, spread

# --- 模擬執行 ---
def run_simulation():
    steps = 1000
    # 測試臨界區域: alpha/beta 比例
    sim = GRTDSimulator(alpha=1.0, beta=0.8) 
    
    tensions = []
    spreads = []
    
    for _ in range(steps):
        t, s = sim.step()
        tensions.append(t)
        spreads.append(s)
        
    # 視覺化結果
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(tensions, label='Tension (T_t)')
    plt.axhline(0, color='r', linestyle='--')
    plt.title("Generative–Recurrent Tension Index")
    
    plt.subplot(1, 2, 2)
    plt.plot(spreads, label='Representational Spread (S_t)', color='green')
    plt.title("Representational Spread")
    plt.show()

if __name__ == "__main__":
    run_simulation()

```
### 程式邏輯說明：
 1. **狀態空間 (X_t)**：由 d 維的向量表示，模擬認知系統的表示空間。
 2. **控制向量 (U_t^G, U_t^V)**：
   * U_G 模擬探索驅動，隨機且傾向於增加系統的方差（Spread）。
   * U_V 模擬回返驅動，與狀態值負相關，起到穩定器（Stabilizer）作用。
 3. **張力索引 (T_t)**：計算兩者平方模長的差值。當 T_t > 0 時，系統處於擴張狀態；當 T_t < 0 時，系統處於收斂狀態。
 4. **動力演化**：透過 dt 進行離散化數值積分。
