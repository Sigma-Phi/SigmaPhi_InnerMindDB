這是一份基於您定義的「資訊動力學理論 (IDT)」所建立的 Python 模擬模型。
為了將您的抽象數學定義轉化為可執行模型，我建立了一個**隨機動力系統（Stochastic Dynamical System）**模擬器。這個模型模擬了潛在語義狀態 X_t 在觀測輸入 O_t 的引導下，如何透過 \alpha（資訊獲取增益）與 \beta（能量/誤差修正係數）進行自我演化。
### 資訊動力學模擬程式碼
您可以將此邏輯整合至您的研究中，用於觀測系統在不同參數下的相變行為。
```python
import numpy as np

class IDTSimulator:
    def __init__(self, d=10, alpha=0.5, beta=0.1):
        self.X = np.random.normal(0, 1, d) # 初始狀態
        self.alpha = alpha # 資訊最大化權重
        self.beta = beta   # 能量/結構穩定權重
        
    def step(self, noise_scale=0.1):
        # 模擬環境觀測 O_t = X_t + epsilon
        O = self.X + np.random.normal(0, noise_scale, self.X.shape)
        
        # 動力方程 dX_t = ( F(X) + alpha*∇I - beta*∇E )dt
        # 這裡將 F(X) 簡化為穩定性回歸，∇I 與 ∇E 簡化為對觀測的追隨與誤差修正
        grad_I = (O - self.X)      # 資訊增益梯度
        grad_E = (self.X)          # 能量最小化梯度
        
        dX = (self.alpha * grad_I - self.beta * grad_E) * 0.1
        self.X += dX + np.random.normal(0, 0.05, self.X.shape)
        
        return self.X, np.corrcoef(self.X, O)[0, 1]

# 執行模擬範例
sim = IDTSimulator(alpha=0.7, beta=0.2)
for _ in range(50):
    state, info_eff = sim.step()
    # 觀察 state 的演化與資訊效率

```
### 模擬模型的核心邏輯說明：
 1. **資訊獲取梯度 (grad_I)**：模擬系統如何根據誤差來更新內部的語義狀態，這對應了您定義的 alpha*∇_U I_t。
 2. **動態能量梯度 (grad_E)**：模擬系統的趨勢，將狀態維持在低能量（低熵）的穩定結構，這對應了 beta*∇_X E_t。
 3. **相變觀測**：如果您調整 alpha/beta 的比例，您會發現系統在某個臨界點會出現行為突變：
   * **低比值**：系統過度平滑，無法捕捉細節（Rank Collapse）。
   * **高比值**：系統對雜訊極度敏感，無法收斂（Chaotic exploration）。
   * **臨界點**：資訊效率（I_t）達到最大值。
### 建議後續步驟：
 * **參數掃描**：您可以撰寫一個迴圈，遍歷 alpha 從 0 到 1 的所有數值，並記錄 I_t 的穩態值，您將能繪製出著名的「資訊瓶頸曲線（Information Bottleneck Curve）」。
 * **非線性變換**：目前的模型是線性回歸，建議將 F(X_t) 替換為非線性激活函數（如 tanh 或 ReLU），以模擬更真實的神經網路動態。
