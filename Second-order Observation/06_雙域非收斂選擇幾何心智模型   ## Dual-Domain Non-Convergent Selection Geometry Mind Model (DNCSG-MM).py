為了將「雙域非收斂選擇幾何心智模型 (DNCSG-MM)」轉化為可執行的計算模型，我們需要使用 **隨機微分方程 (SDE)** 的數值模擬方法。
以下是一個基於 numpy 的簡化實現。此模型模擬了一個概念空間中，注意力 U_t 如何影響概念點在吸引盆地 \mathcal{A}(x) 中的遷移與跳變。
### DNCSG-MM Python 模擬框架
```python
import numpy as np
import matplotlib.pyplot as plt

class DNCSG_Model:
    def __init__(self, dim=2, dt=0.01):
        self.dim = dim
        self.dt = dt
        self.X = np.random.randn(dim)  # 初始狀態
        
    def attractor_potential(self, x):
        """定義雙吸引盆地勢能: V(x) = (x^2 - 1)^2"""
        return (np.sum(x**2) - 1)**2

    def gradient_F(self, x):
        """概念張力場: 勢能的負梯度"""
        # 簡單的雙阱勢梯度
        return -4 * x * (np.sum(x**2) - 1)

    def step(self, U_t, noise_level=0.1):
        """
        模擬心智演化: dX_t = F(X_t, U_t)dt + G(dW_t)
        U_t: 注意力控制，正值會拉平勢能（發散），負值會加深盆地（收斂）
        """
        # 引入注意力對曲率的改變
        F = self.gradient_F(self.X) + U_t * self.X
        dW = np.random.normal(0, np.sqrt(self.dt), self.dim)
        
        # 狀態更新
        self.X += F * self.dt + noise_level * dW
        return self.X

# --- 模擬執行 ---
model = DNCSG_Model()
history = []

# 模擬認知過程: 從收斂狀態 -> 調整注意力 -> 觸發跳變
for i in range(1000):
    # 前 500 步：高聚焦 (U_t < 0)，後 500 步：發散搜索 (U_t > 0)
    u_t = -0.5 if i < 500 else 0.5 
    state = model.step(U_t=u_t)
    history.append(state.copy())

# --- 視覺化 ---
history = np.array(history)
plt.figure(figsize=(10, 5))
plt.plot(history[:, 0], label='Conceptual Dimension 1')
plt.plot(history[:, 1], label='Conceptual Dimension 2')
plt.title("DNCSG-MM: Non-Convergent Cognitive Path")
plt.xlabel("Time Step (t)")
plt.ylabel("Selection Geometry State ($X_t$)")
plt.legend()
plt.show()

```
### 模型參數實作說明
 1. **狀態空間 (X_t)**：在此程式碼中，我們將概念空間簡化為二維向量，代表兩個核心概念維度。
 2. **勢能場 (V(X_t))**：利用雙阱勢函數模擬「吸引盆地」。當勢能越深，系統越難跳出該思考模式（Convergent）。
 3. **注意力控制 (U_t)**：
   * **U_t < 0（收斂模式）**：增強勢能梯度，將思維鎖定在特定領域。
   * **U_t > 0（發散模式）**：平滑勢能場，使得系統更容易跨越障礙，進入新的吸引盆地（Insight）。
 4. **隨機擾動 (dW_t)**：模擬人類思維中的隨機性與外部干擾，這是防止系統陷入絕對停滯並觸發「拓撲重連」的必要條件。
### 下一步演進建議
若要進一步強化此計算模型，建議引入以下組件：
 * **殘留記憶場 (\rho_t)**：引入一個長短期記憶緩衝（buffer），記錄過去的軌跡，並將其轉化為下一時刻的勢能場偏移，實現「認知慣性」。
 * **拓撲檢測算法**：在模擬過程中加入對流形連通性的檢測（如 Persistence Homology），以量化記錄「Insight Event」發生的具體時刻。

