import math
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="家具の数学電卓 | 諦めてた家具、通るかも",
    page_icon="📐",
    layout="centered",
)

# カスタムCSS ＆ スリープ防止
st.markdown(
    """
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button {
        width: 100%;
        background-color: #4f46e5;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 0.8rem;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    .stButton>button:hover { background-color: #4338ca; color: white; }
    </style>

    <script>
    async function requestWakeLock() {
        try {
            if ('wakeLock' in navigator) {
                const wakeLock = await navigator.wakeLock.request('screen');
            }
        } catch (err) {}
    }
    requestWakeLock();
    </script>
    """,
    unsafe_allow_html=True,
)

# ヘッダー
st.markdown(
    "<p style='text-align: center; color: #4f46e5; font-size: 13px; font-weight: 700; margin-bottom: 0; letter-spacing: 0.05em;'>家具の数学電卓</p>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h1 style='text-align: center; font-size: 22px; margin-top: 2px;'>搬入・隙間シミュレーター</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #64748b; font-size: 11px;'>諦めてたその家具、三平方の定理なら通るかもしれません。</p>",
    unsafe_allow_html=True,
)

st.divider()

# 1. 搬入・通過チェッカー
st.markdown("### 🚪 1. 搬入・通過チェッカー")
with st.form("transport_form"):
  st.markdown("##### 📦 家具・家電のサイズ (cm)")
  c1, c2, c3 = st.columns(3)
  with c1:
    w = st.number_input("幅 (W)", min_value=0.0, value=80.0, step=1.0, key="t_w")
  with c2:
    d = st.number_input("奥行 (D)", min_value=0.0, value=45.0, step=1.0, key="t_d")
  with c3:
    h = st.number_input("高さ (H)", min_value=0.0, value=180.0, step=1.0, key="t_h")

  st.markdown("##### 🚪 通り道のサイズ (cm)")
  dc1, dc2 = st.columns(2)
  with dc1:
    dw = st.number_input(
        "ドア・廊下の幅", min_value=0.0, value=75.0, step=1.0, key="t_dw"
    )
  with dc2:
    dh = st.number_input(
        "ドア・廊下の高さ", min_value=0.0, value=190.0, step=1.0, key="t_dh"
    )

  submitted_t = st.form_submit_button("数学で搬入判定する")

if submitted_t:
  diagonal = math.sqrt(w**2 + d**2 + h**2)
  st.success("計算完了！")
  st.metric(label="📐 家具の立体対角線", value=f"{round(diagonal, 1)} cm")

  min_side = min(w, d, h)
  door_diag = math.sqrt(dw**2 + dh**2)
  min_door = min(dw, dh)

  if min_side <= min_door and diagonal <= door_diag:
    st.markdown(
        "🟢 **【合格】搬入できる可能性が極めて高いです！**<br>家具を斜め（対角線）に傾けることで、クリアできる数学的根拠があります。自信を持って挑みましょう！",
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        "🔴 **【要注意】そのままでは厳しいかも…**<br>対角線または最小辺が寸法を超えています。脚を外す、あるいは分解できるか再確認を！",
        unsafe_allow_html=True,
    )

st.divider()

# 2. 隙間・設置チェッカー
st.markdown("### 📐 2. 隙間・設置チェッカー")
with st.form("gap_form"):
  space_w = st.number_input(
      "利用可能な壁幅・隙間 (cm)", min_value=0.0, value=90.0, step=1.0
  )
  item_w = st.number_input(
      "置きたい家具の幅 (cm)", min_value=0.0, value=80.0, step=1.0
  )
  baseboard = st.number_input(
      "巾木（壁下の出っ張りの厚み）(cm)", min_value=0.0, value=1.5, step=0.5
  )

  submitted_g = st.form_submit_button("隙間を計算する")

if submitted_g:
  effective_space = space_w - (baseboard * 2)
  margin = effective_space - item_w
  st.success("計算完了！")
  st.metric(
      label="✨ 両側のトータル余裕 (Clearance)", value=f"{round(margin, 1)} cm"
  )

  if margin >= 0:
    st.markdown(
        f"🟢 巾木を考慮しても、**約 {round(margin, 1)} cm のゆとり**を持って綺麗に収まります！",
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        f"🔴 巾木に干渉し、**約 {abs(round(margin, 1))} cm オーバー**します。配置場所の再考が必要です。",
        unsafe_allow_html=True,
    )

st.divider()

# 3. 本物のボタン式電卓（完全一体型コンポーネント）
st.markdown("### 🔢 3. 現場のボタン電卓")
st.markdown(
    "<p style='font-size:11px; color:#64748b;'>ボタンをタップしてその場でサッと計算できます。</p>",
    unsafe_allow_html=True,
)

calc_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  .calc-box {
    background: #1e293b;
    padding: 12px;
    border-radius: 14px;
    max-width: 100%;
    margin: 0 auto;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
  }
  .calc-display {
    width: 100%;
    height: 48px;
    background: #0f172a;
    color: #38bdf8;
    font-size: 22px;
    text-align: right;
    padding: 10px;
    box-sizing: border-box;
    border-radius: 8px;
    margin-bottom: 10px;
    overflow-x: auto;
    font-family: monospace;
  }
  .calc-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
  }
  .calc-btn {
    background: #4f46e5;
    color: white;
    border: none;
    padding: 12px 0;
    font-size: 16px;
    font-weight: bold;
    border-radius: 8px;
    cursor: pointer;
    text-align: center;
  }
  .calc-btn:active {
    background: #3730a3;
  }
  .calc-btn.op { background: #6366f1; }
  .calc-btn.eq { background: #10b981; }
  .calc-btn.clear { background: #ef4444; }
</style>
</head>
<body>
<div class="calc-box">
  <div id="display" class="calc-display">0</div>
  <div class="calc-grid">
    <button class="calc-btn clear" onclick="appendValue('C')">C</button>
    <button class="calc-btn op" onclick="appendValue('(')">（</button>
    <button class="calc-btn op" onclick="appendValue(')')">）</button>
    <button class="calc-btn op" onclick="appendValue('/')">÷</button>
    
    <button class="calc-btn" onclick="appendValue('7')">7</button>
    <button class="calc-btn" onclick="appendValue('8')">8</button>
    <button class="calc-btn" onclick="appendValue('9')">9</button>
    <button class="calc-btn op" onclick="appendValue('*')">×</button>
    
    <button class="calc-btn" onclick="appendValue('4')">4</button>
    <button class="calc-btn" onclick="appendValue('5')">5</button>
    <button class="calc-btn" onclick="appendValue('6')">6</button>
    <button class="calc-btn op" onclick="appendValue('-')">-</button>
    
    <button class="calc-btn" onclick="appendValue('1')">1</button>
    <button class="calc-btn" onclick="appendValue('2')">2</button>
    <button class="calc-btn" onclick="appendValue('3')">3</button>
    <button class="calc-btn op" onclick="appendValue('+')">+</button>
    
    <button class="calc-btn" onclick="appendValue('0')">0</button>
    <button class="calc-btn" onclick="appendValue('.')">.</button>
    <button class="calc-btn clear" onclick="appendValue('BACK')">⌫</button>
    <button class="calc-btn eq" onclick="calculate()">=</button>
  </div>
</div>

<script>
let expression = "";

function appendValue(val) {
  const display = document.getElementById('display');
  if (val === 'C') {
    expression = "";
  } else if (val === 'BACK') {
    expression = expression.slice(0, -1);
  } else {
    expression += val;
  }
  display.innerText = expression === "" ? "0" : expression;
}

function calculate() {
  const display = document.getElementById('display');
  try {
    let result = eval(expression);
    expression = String(result);
    display.innerText = expression;
  } catch (e) {
    display.innerText = "エラー";
    expression = "";
  }
}
</script>
</body>
</html>
"""

components.html(calc_html, height=275)
