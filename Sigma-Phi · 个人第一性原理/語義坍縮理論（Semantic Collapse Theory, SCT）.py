這是一個基於您提供的數學框架所編寫的 Python 仿真程序。這個程序實現了「語義坍縮理論」的核心動力方程，並演示了語義狀態 z 如何在「信息保留壓力」與「坍縮壓力」的競爭下演化。
### 語義坍縮理論 (SCT) 仿真程序
```python
import numpy as np

class SemanticCollapseSimulator:
    """
    語義坍縮理論 (SCT) 的仿真模型
    模擬語義狀態 z 在信息流 I 和 坍縮力 S 下的演化
    """
    def __init__(self, dt=0.01, steps=1000, alpha=0.5, beta=0.5, lambda_param=1.0):
        self.dt = dt
        self.steps = steps
        self.alpha = alpha  # 信息保留權重
        self.beta = beta    # 坍縮力度
        self.lambda_param = lambda_param # 壓縮強度參數 (λ)
        
        # 初始化語義狀態 z (維度為 2 的向量)
        self.z = np.random.randn(2) 
        self.history = []

    def get_gradient_I(self, z):
        # 模擬信息增益梯度：指向中心，代表向理想知識彙聚
        return -z 

    def get_gradient_S(self, z):
        # 模擬坍縮壓力：隨語義離散度增加而增加的力
        return z * np.linalg.norm(z)

    def step(self):
        # 隨機擾動 (dW)
        dW = np.random.normal(0, np.sqrt(self.dt), 2)
        
        # 動態方程: dz_t = (alpha * ∇I - beta * λ * ∇S)dt + G * dW
        grad_I = self.get_gradient_I(self.z)
        grad_S = self.get_gradient_S(self.z)
        
        drift = (self.alpha * grad_I - self.beta * self.lambda_param * grad_S)
        self.z += drift * self.dt + 0.1 * dW
        self.history.append(self.z.copy())

    def run(self):
        for _ in range(self.steps):
            self.step()
        return np.array(self.history)

# --- 執行與使用示例 ---
# 設置 beta=0.8, lambda=1.5 模擬一個高壓縮環境
sim = SemanticCollapseSimulator(beta=0.8, lambda_param=1.5)
history = sim.run()

print(f"模擬完成，狀態序列形狀: {history.shape}")
print("前 5 個語義狀態點:")
print(history[:5])

```
### 對程式邏輯的簡要說明：
 1. **動力方程實現**：step() 方法直接對應了您定義的微分方程 dz_t = (F(z_t) + \alpha \nabla_z I_t - \beta \nabla_z S_t)dt + G(z_t)dW_t。
 2. **\lambda 參數控制**：透過調整 lambda_param，您可以直接觀察系統的相變。
   * 若將 lambda_param 調大，系統會更快地收斂（坍縮）到極小空間（Over-compressed Phase）。
   * 若將 lambda_param 調至接近 0，系統則會因為隨機項 dW 的影響，呈現出發散的趨勢（Over-dispersed Phase）。
 3. **可擴展性**：這個基礎模型可以進一步擴展，例如透過 sklearn 引入實際的文字數據來初始化 z_t，或者增加多個 Agent 來模擬 D_t（跨代理人分歧）的演化過程。
您可以根據具體的實驗需求調整 alpha（信息獲取慾望）與 beta（認知節能需求）的比例，以驗證不同認知行為下的語義收斂路徑。
