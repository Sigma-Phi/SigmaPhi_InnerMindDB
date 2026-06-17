# 📌 理論名稱：注意觸發式雙迴路場理論（Attentional Triggered Dual-Loop Field Theory, ATDLF）

---

# I. 系統形式化 (Formal System Construction)

## 中文定義
在 ATDLF 中，系統狀態 \(X_t\) 被定義為三元場結構：

\[
X_t = (A_t, S_t, \Phi_t)
\]

其中：
- \(A_t\)：注意場（是否進入可作用狀態）
- \(S_t\)：可觀測系統狀態
- \(\Phi_t\)：雙迴路選擇場（決定修正流或重構流）

系統並非持續回應輸入，而是由「注意觸發機制」決定是否進入動力學更新。  
當 \(A_t=0\) 時，系統凍結於潛在態；當 \(A_t=1\) 時，觸發場激活並決定流向分岔（correction vs reconfiguration）。

外部觀測 \(O_t\) 與控制 \(U_t\) 只有在注意場開啟時才被映射進內部動力學。  
隨機性來自注意閾值附近的觸發不確定性。

---

## English Definition
In ATDLF, the system state \(X_t\) is defined as a triplet field structure \((A_t, S_t, \Phi_t)\), where:
- \(A_t\) represents the attentional field,
- \(S_t\) the observable system state,
- \(\Phi_t\) the dual-loop selection field.

Dynamics are not continuously responsive but activated only when attention is triggered.  
When \(A_t=0\), the system remains in a latent frozen state; when \(A_t=1\), the trigger field activates and branches into correction or reconfiguration flows.

Observations and controls affect dynamics only under active attention.  
Stochasticity arises from threshold uncertainty in attention activation.

---

## 公式

\[
dX_t = F(X_t, O_t, U_t)dt + G(X_t, O_t, U_t)dW_t
\]

（其中 \(F\) 在 \(A_t=0\) 時退化為 0 場或慢漂移場）

---

# II. 關鍵變量映射 (Key Quantities Mapping)

## 中文列表
1. 注意場強度 \(A_t\)：系統是否進入可運作狀態的門控變量  
2. 觸發閾值 \(\theta_A\)：注意場從潛伏態轉為激活態的臨界條件  
3. 雙迴路選擇場 \(\Phi_t\)：決定修正流 vs 重構流的隱式控制勢  
4. 局部誤差張量 \(E_t\)：驅動修正流的穩定性偏差來源  
5. 結構漂移向量 \(R_t\)：累積後導向重構流的長期變形量  

## English List
1. Attention field intensity \(A_t\): gating variable for system activation  
2. Trigger threshold \(\theta_A\): critical condition for attention activation  
3. Dual-loop selection field \(\Phi_t\): latent control potential selecting flow mode  
4. Local error tensor \(E_t\): deviation driving correction dynamics  
5. Structural drift vector \(R_t\): long-term accumulation leading to reconfiguration  

---

# III. 動態演化方程 (Dynamics Evolution)

## 中文解釋
系統演化分為兩層：注意層與動力層。  
當注意場未被觸發時，系統處於低能耗漂移狀態；一旦觸發，系統進入雙迴路選擇機制。

若 \(E_t\) 主導，系統進入修正流以抑制局部偏差；  
若 \(R_t\) 累積超過結構閾值，則進入重構流重新定義系統拓撲。

因此，演化不是連續收斂，而是「事件驅動的相位跳躍」。

---

## English Explanation
The system evolves through two coupled layers: attentional gating and dynamic flow.  
When attention is inactive, the system remains in a low-energy drift state.  
Once triggered, a dual-loop mechanism activates.

If local error dominates, correction flow stabilizes deviations;  
if structural drift exceeds threshold, reconfiguration flow reshapes system topology.

Thus, evolution is not continuous convergence but event-driven phase jumps.

---

# IV. 系統相變結構 (Phase Transition Structure)

| Regime | 注意狀態 \(A_t\) | 主導動力 | 系統行為 | 相變條件 |
|--------|------------------|----------|----------|----------|
| 潛伏態 (Latent) | 0 | 無 | 凍結 / 慢漂移 | \(A_t < \theta_A\) |
| 修正流 (Correction Phase) | 1 | 局部誤差 \(E_t\) | 穩定化 | \(E_t < \lambda R_t\) |
| 重構流 (Reconfiguration Phase) | 1 | 結構漂移 \(R_t\) | 拓撲重寫 | \(R_t > \theta_R\) |
| 臨界態 (Critical Switching) | ≈1 | 混合 | 不穩定切換 | \(E_t \approx R_t\) |

---

# V. 核心定論 (Main Theorem)

## 中文
當注意場長時間維持在臨界閾值附近時，系統不再收斂於單一穩態，而會進入修正流與重構流之間的永續切換態（Persistent Switching Regime）。

## English
When the attentional field remains near its critical threshold, the system does not converge to a fixed point but enters a persistent switching regime between correction and reconfiguration flows.

---

# VI. 穩定性分析 (Lyapunov Stability)

## Lyapunov 函數

\[
V(X_t) = \alpha \|E_t\|^2 + \beta \|R_t\|
\]

其中：
- \(\alpha\)：修正抑制強度  
- \(\beta\)：重構驅動權重  

---

## 穩定條件

- 若 \(A_t=1\) 且 \(E_t\) 主導 → \(V \downarrow\)（局部穩定）  
- 若 \(R_t\) 主導 → \(V\) 非單調（結構漂移）  
- 若 \(A_t=0\) → \(V\) 凍結（no-update manifold）  

---

## 結論
系統穩定性不是單調下降，而是「分段 Lyapunov 收斂 + 結構跳變」。

---

# VII. 實證驗證方案 (Experimental Protocol)

1. 測量系統在「無輸入但突然改變」情境下的狀態跳變頻率  
2. 分析短期誤差修正 vs 長期結構變化的時間尺度分離  
3. 建立 attention proxy（注意力指標 / 資源分配變化）與行為激活關係  
4. 檢驗是否存在臨界閾值導致行為模式切換  
5. 比較 continuous model vs event-triggered model 的預測誤差差異  

---

# VIII. 可證偽預測 (Falsifiable Predictions)

1. 若注意指標持續高於閾值，系統仍可能保持完全不變（反例：連續模型失效）  
2. 系統變化事件呈現 heavy-tailed 間歇分布，而非高斯波動  
3. 存在可重複測得的「雙模式切換頻率峰值」對應臨界注意區間  

---

# IX. 理論精義總結 (Core Insight)

系統的真正自由度不在於持續演化，而在於「是否被注意所喚醒並進入可切換的存在狀態」。
