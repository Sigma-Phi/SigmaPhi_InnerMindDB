為了將「非理性決策場動力學」轉化為可計算模型，我們可以使用 **Euler-Maruyama 方法** 來模擬隨機微分方程。
此 Python 程式碼模擬了決策狀態 X_t 隨時間演化的過程，並引入了相變控制變量，您可以調整參數以觀察系統從「穩定理性」到「非理性漂移」的動態變化。
### Python 模型：NRDFD 模擬器
```python
import numpy as np
import matplotlib.pyplot as plt

def simulate_nrdfd(steps=1000, dt=0.01, f_strength=1.0, g_strength=0.5):
    """
    模擬非理性決策場動力學
    dX_t = F(X_t)dt + G(X_t)dW_t
    """
    x = np.zeros(steps)
    x[0] = 0.5  # 初始決策狀態
    
    # 內在驅動力 F: 假設傾向於回歸理性平衡點 0 (負回饋)
    def F(x_t):
        return -f_strength * x_t
    
    # 噪聲放大函數 G: 隨狀態變化的波動
    def G(x_t):
        return g_strength * (1 + 0.5 * x_t**2)
    
    for t in range(1, steps):
        dw = np.random.normal(0, np.sqrt(dt))
        dx = F(x[t-1]) * dt + G(x[t-1]) * dw
        x[t] = x[t-1] + dx
        
    return x

# --- 模擬不同場景 ---
# 1. 穩定理性區 (F >> G)
rational = simulate_nrdfd(f_strength=2.0, g_strength=0.1)
# 2. 非理性漂移區 (G >> F)
irrational = simulate_nrdfd(f_strength=0.1, g_strength=1.0)

# 繪圖展示
plt.figure(figsize=(10, 5))
plt.plot(rational, label="Rational Phase (F >> G)")
plt.plot(irrational, label="Non-Rational Drift (G >> F)")
plt.axhline(0, color='black', linestyle='--', alpha=0.3)
plt.title("NRDFD: Decision State Evolution")
plt.xlabel("Time Step")
plt.ylabel("State X_t")
plt.legend()
plt.show()

```
### 模型參數實作建議
 1. **擴充維度**：若要模擬多個個體的互動，可以將 X_t 改為向量，並加入一個**耦合項（Coupling Term）**，例如 \sum_{j} J_{ij}(X_j - X_i)，用以模擬社交共振（群體行為）。
 2. **動態調整**：您可以將 f_strength 和 g_strength 設定為與外部輸入 O_t 相關的變數，例如設定 g_strength = constant * O_t，這樣當外部資訊壓力（如市場崩盤）增加時，系統將自動進入高波動區。
 3. **潛在動態結構視覺化**：理解這種隨機過程的勢能面變化，對於解釋決策崩潰至關重要。
### 執行指南
 * **環境需求**：需安裝 numpy 與 matplotlib。
 * **數值穩定性**：若模擬過程中出現發散，請減小 dt（時間步長）。
 * **臨界點檢測**：您可以計算每一段時間窗內的變異數（Variance），當變異數超過設定閾值時，即觸發程式碼中的「相變警告」。
這個模型目前是一個基礎的 **Ornstein-Uhlenbeck 過程變體**。
