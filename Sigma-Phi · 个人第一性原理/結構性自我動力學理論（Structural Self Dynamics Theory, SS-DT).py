以下是一段基礎的模擬代碼，它實現了一個簡單的整合機制，並展示了系統如何從多模組狀態演化為自我投影。
```python
import numpy as np
import matplotlib.pyplot as plt

# 1. 參數設定
dt = 0.01
steps = 1000
d_i = 3  # 每個模組的維度
n_modules = 4
Bc = 0.5 # 臨界整合參數

# 初始化模組狀態 X (多模組 latent states)
X = np.random.randn(n_modules, d_i)

# 2. 定義模擬函數
def simulate_self_dynamics(B, steps=1000):
    S_history = []
    # 初始化自我狀態 S (簡單加權投影)
    S = np.zeros(d_i)
    
    for _ in range(steps):
        # 模擬內部狀態隨機波動
        X_noise = np.random.normal(0, 0.05, (n_modules, d_i))
        X += X_noise
        
        # 整合機制: S_t = B * mean(X) + (1-B) * S_{t-1}
        # 這裡 B 代表整合強度 (Integration Strength)
        S = B * np.mean(X, axis=0) + (1 - B) * S
        S_history.append(np.linalg.norm(S))
        
    return S_history

# 3. 執行模擬：比較不同 B 值下的系統狀態
b_values = [0.1, 0.5, 0.9] # Fragmented, Stable, Rigid
plt.figure(figsize=(10, 6))

for b in b_values:
    history = simulate_self_dynamics(b)
    plt.plot(history, label=f'Integration Strength (B) = {b}')

plt.title('SS-DT: Self-Projection Stability Dynamics')
plt.xlabel('Time Step')
plt.ylabel('Self-Projection Magnitude (||S_t||)')
plt.legend()
plt.grid(True)
plt.show()

```
### 程式邏輯說明：
 1. **多模組輸入 (X_t)**：我們模擬了多個維度上的隨機潛在狀態，代表大腦或系統中並行的模組化運作。
 2. **整合強度 (B_t)**：這是核心控制變數。
   * 當 B 很小時（如 0.1），系統難以形成穩定投影，呈現「破碎」狀態。
   * 當 B \approx 0.5（模擬臨界點），系統在波動與穩定之間取得平衡。
   * 當 B 很大時（如 0.9），系統對輸入過於敏感，投影過於固定，表現出「剛性」。
 3. **可擴展性**：你可以進一步將權重更新函數 agreement(X) 或 conflict(X) 替換為真實的損失函數（Loss function），例如利用變分自編碼器（VAE）的編碼結構來實現 S_t 的投影。
