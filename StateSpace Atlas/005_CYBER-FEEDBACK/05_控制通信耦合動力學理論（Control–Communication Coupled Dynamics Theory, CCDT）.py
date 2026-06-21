這是一個基於**CCDT（控制通信耦合動力學理論）** 所編寫的 Python 模擬腳本。它使用了微分方程離散化的方式，模擬了系統在特定控制強度（\alpha）、通信強度（\beta）與耦合係數（\kappa）下的行為。
### Python 模擬腳本 (ccdt_simulation.py)
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_ccdt_simulation(alpha=0.5, beta=0.5, kappa=0.3, steps=1000, dt=0.01):
    """
    CCDT 模擬模型
    dX_t = (-alpha * X_t + kappa * H_t) dt + sigma * dW_t
    dH_t = (-beta * H_t + kappa * X_t) dt + sigma * dW_t
    """
    # 初始化
    X = np.zeros(steps)
    H = np.zeros(steps)
    X[0], H[0] = 0.5, 0.5  # 初始狀態
    sigma = 0.05           # 隨機擾動強度

    for t in range(1, steps):
        # 確定性動力學 + 隨機擾動
        dX = (-alpha * X[t-1] + kappa * H[t-1]) * dt + sigma * np.random.normal()
        dH = (-beta * H[t-1] + kappa * X[t-1]) * dt + sigma * np.random.normal()
        
        X[t] = X[t-1] + dX
        H[t] = H[t-1] + dH
        
    return pd.DataFrame({'Time': range(steps), 'Coherence': X, 'Entropy': H})

# 執行模擬
data = run_ccdt_simulation(alpha=0.6, beta=0.4, kappa=0.35)

# 繪圖
plt.figure(figsize=(10, 6))
plt.plot(data['Time'], data['Coherence'], label='Structural Coherence (X)')
plt.plot(data['Time'], data['Entropy'], label='Communication Entropy (H)')
plt.title('CCDT System Dynamics')
plt.xlabel('Time Step')
plt.ylabel('Magnitude')
plt.legend()
plt.grid(True)
plt.show()

```
### 如何使用此代碼來驗證您的理論：
 1. **驗證相變（Section IV）：**
   * 嘗試將 alpha=0.9, beta=0.1，觀察系統是否呈現「高控制低通信」的平穩態。
   * 嘗試將 alpha=0.1, beta=0.9，觀察系統是否出現高波動的「創新/變動」態。
 2. **模擬臨界耦合（Section V）：**
   * 當您設置 \alpha \cdot \beta \approx \kappa 時，您可以觀察兩條曲線（X 與 H）是否出現趨近一致的同步化現象（Synchronization）。
 3. **擴充為時滯模型（Section VI）：**
   * 若要加入「回饋延遲 \tau」，您需要使用 collections.deque 來存儲過去的狀態值，並將 X[t-1] 替換為 X[t - int(tau/dt)]，這將能精確模擬出理論中提及的「崩解態」。
這個腳本提供了一個可運行的基礎。
