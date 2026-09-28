import math
import streamlit as st

st.set_page_config(
    page_title="家具の数学電卓 | 諦めてた家具、通るかも",
    page_icon="📐",
    layout="centered",
)

# カスタムCSS（電卓をスマホでも強制4列にするデザイン）
st.markdown(
    """
    <style>
    .main { background-color: #f8fafc; }
    
    /* 電卓ボタン用のカスタムグリッド */
    .calc-container {
        display: flex;
        flex-direction: column;
        gap: 8px;
        max-width: 100%;
        margin: 0 auto;
    }
    .calc-row {
        display: flex;
        gap: 8px;
    }
    /* スマホでも強制的に4列均等に並べる */
    .calc-btn-form {
        flex: 1;
        margin: 0 !important;
    }
    .calc-btn-form button {
        width: 100% !important;
        background-color: #4f46e5 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        padding: 0.7rem 0 !important;
        font-size: 16px !important;
        box-shadow: 0 2px 6px rgba(79, 70, 229, 0.3);
        border: none !important;
    }
    .calc-btn-form button:hover {
        background-color: #4338ca !important;
    }
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

# 電卓用のセッション状態の初期化
if "calc_expr" not in st.session_state:
  st.session_state.calc_expr = ""

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

# 3. 本物のボタン式電卓
st.markdown("### 🔢 3. 現場のボタン電卓")
st.markdown(
    "<p style='font-size:11px; color:#64748b;'>ボタンをタップしてその場でサッと計算できます。</p>",
    unsafe_allow_html=True,
)

# ディスプレイ表示
display_text = (
    st.session_state.calc_expr if st.session_state.calc_expr else "0"
)
st.text_input("ディスプレイ", value=display_text, disabled=True, key="disp")

# ボタンレイアウト定義
buttons = [
    ["C", "(", ")", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "⌫", "="],
]

# カスタムCSSコンテナ内でボタンをレンダリング
for r_idx, row in enumerate(buttons):
  cols = st.columns(4)
  for c_idx, btn_label in enumerate(row):
    with cols[c_idx]:
      # 各ボタンに固有のクラスを割り当てるためのラッパー
      st.markdown('<div class="calc-btn-form">', unsafe_allow_html=True)
      if st.button(btn_label, key=f"btn_{r_idx}_{c_idx}"):
        if btn_label == "C":
          st.session_state.calc_expr = ""
        elif btn_label == "⌫":
          st.session_state.calc_expr = st.session_state.calc_expr[:-1]
        elif btn_label == "=":
          try:
            expr = (
                st.session_state.calc_expr.replace("×", "*")
                .replace("÷", "/")
                .replace("✕", "*")
            )
            res = eval(expr)
            st.session_state.calc_expr = str(res)
          except Exception:
            st.session_state.calc_expr = "エラー"
        else:
          st.session_state.calc_expr += btn_label
        st.rerun()
      st.markdown("</div>", unsafe_allow_html=True)
