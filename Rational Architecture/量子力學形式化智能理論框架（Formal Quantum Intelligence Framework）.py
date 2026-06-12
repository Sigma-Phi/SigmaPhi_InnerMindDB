這是一個非常經典且適合進行計算模擬的物理系統：**雙擺（Double Pendulum）的混沌運動模擬**。
雙擺系統對初始條件非常敏感（這就是著名的「蝴蝶效應」），只需要簡單的物理公式，就能模擬出極其複雜、美觀且不可預測的動態軌跡。
這個腳本使用了 scipy 來解微分方程，並用 matplotlib 製作成**動態動畫**。
### 🐍 雙擺模擬 Python 程式碼
你可以直接複製以下程式碼，並在安裝好必要的套件後執行：
```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import matplotlib.animation as animation

# --- 1. 物理參數設定 ---
G = 9.81   # 重力加速度 (m/s^2)
L1 = 1.0   # 第一根擺桿長度 (m)
L2 = 1.0   # 第二根擺桿長度 (m)
M1 = 1.0   # 第一個擺錘質量 (kg)
M2 = 1.0   # 第二個擺錘質量 (kg)

# --- 2. 定義運動微分方程 (拉格朗日力學簡化) ---
def double_pendulum_deriv(t, y):
    """
    y = [theta1, omega1, theta2, omega2]
    回傳各自的導數 [d_theta1, d_omega1, d_theta2, d_omega2]
    """
    t1, w1, t2, w2 = y
    delta = t1 - t2
    
    # 矩陣公式簡化計算雙擺的角加速度
    den1 = L1 * (2 * M1 + M2 - M2 * np.cos(2 * t1 - 2 * t2))
    den2 = L2 * (2 * M1 + M2 - M2 * np.cos(2 * t1 - 2 * t2))
    
    dt1 = w1
    dw1 = (-G * (2 * M1 + M2) * np.sin(t1) - M2 * G * np.sin(t1 - 2 * t2) - 
           2 * np.sin(delta) * M2 * (w2**2 * L2 + w1**2 * L1 * np.cos(delta))) / den1
    
    dt2 = w2
    dw2 = (2 * np.sin(delta) * (w1**2 * L1 * (M1 + M2) + 
           G * (M1 + M2) * np.cos(t1) + w2**2 * L2 * M2 * np.cos(delta))) / den2
    
    return [dt1, dw1, dt2, dw2]

# --- 3. 初始狀態與時間設定 ---
# 初始角度 (弧度)，這裡設定接近水平釋放
theta1_init = np.radians(90.0)
omega1_init = np.radians(0.0)
theta2_init = np.radians(90.0)
omega2_init = np.radians(0.0)

y0 = [theta1_init, omega1_init, theta2_init, omega2_init]

# 模擬時間：0 到 20 秒，共 1000 個時間點
t_span = (0, 20)
t_eval = np.linspace(0, 20, 1000)

# --- 4. 執行數值積分 (計算模擬核心) ---
sol = solve_ivp(double_pendulum_deriv, t_span, y0, t_eval=t_eval, method='RK45')

# 提取計算結果
t1_res, t2_res = sol.y[0], sol.y[2]

# 將極座標轉換為直角座標 (X, Y) 用於繪圖
x1 = L1 * np.sin(t1_res)
y1 = -L1 * np.cos(t1_res)
x2 = x1 + L2 * np.sin(t2_res)
y2 = y1 - L2 * np.cos(t2_res)

# --- 5. 製作動畫 ---
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-(L1 + L2 + 0.2), L1 + L2 + 0.2)
ax.set_ylim(-(L1 + L2 + 0.2), L1 + L2 + 0.2)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_title("Double Pendulum Simulation")

# 建立動畫元件
line, = ax.plot([], [], 'o-', lw=2, color='#1f77b4', markersize=8) # 擺桿與擺錘
trace, = ax.plot([], [], '-', lw=1, color='#ff7f0e', alpha=0.7)    # 第二個擺錘的運動軌跡

x2_trace, y2_trace = [], []

def init():
    line.set_data([], [])
    trace.set_data([], [])
    return line, trace

def animate(i):
    # 更新擺桿位置
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]
    line.set_data(thisx, thisy)
    
    # 更新軌跡 (只保留過去150個時間點，避免畫面太亂)
    x2_trace.append(x2[i])
    y2_trace.append(y2[i])
    if len(x2_trace) > 150:
        x2_trace.pop(0)
        y2_trace.pop(0)
    trace.set_data(x2_trace, y2_trace)
    
    return line, trace

# 執行動畫
ani = animation.FuncAnimation(
    fig, animate, init_func=init, frames=len(t_eval),
    interval=20, blit=True, repeat=True
)

plt.show()

```
### 🛠️ 執行前準備
如果你尚未安裝相關的數學與繪圖套件，請先在終端機（Terminal / Command Prompt）執行以下指令：
```bash
pip install numpy scipy matplotlib

```
### 💡 程式亮點與調整建議
 1. **數值積分器 (solve_ivp)**：程式採用了常用的 RK45（龍格-庫塔法）來精準求解非線性微分方程。
 2. **改變初始值**：你可以試著修改 theta1_init 或 theta2_init（例如改成 90.1 度），你會發現只要差一點點，幾秒後的運動軌跡就會完全不同，這就是**混沌現象**。
