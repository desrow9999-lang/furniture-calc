import math
import streamlit as st

st.set_page_config(
    page_title="家具の数学電卓 | 諦めてた家具、通るかも",
    page_icon="📐",
    layout="centered",
)

# カスタムCSS ＆ スリープ防止（WakeLock API）
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
                console.log('Screen Wake Lock is active!');
            }
        } catch (err) {
            console.error(`${err.name}, ${err.message}`);
        }
    }
    requestWakeLock();
    </script>
    """,
    unsafe_allow_html=True,
)

# 電卓用のセッション状態の初期化
if "calc_expr" not in st.session_state:
  st.session_state.calc_expr = ""
if "calc_result" not in st.session_state:
  st.session_state.calc_result = ""

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

# 計算式のディスプレイ表示
display_val = (
    st.session_state.calc_expr
    if st.session_state.calc_expr
    else ("=" + str(st.session_state.calc_result) if st.session_state.calc_result !== "" else "0")
)
st.text_input(
    "ディスプレイ",
    value=st.session_state.calc_expr if st.session_state.calc_expr else "0",
    disabled=True,
    key="disp",
)

# ボタンのレイアウト (4列)
b1, b2, b3, b4 = st.columns(4)

with b1:
  if st.button("C", key="btn_c"):
    st.session_state.calc_expr = ""
    st.session_state.calc_result = ""
    st.rerun()
with b2:
  if st.button("(", key="btn_lpar"):
    st.session_state.calc_expr += "("
    st.rerun()
with b3:
  if st.button(")", key="btn_rpar"):
    st.session_state.calc_expr += ")"
    st.rerun()
with b4:
  if st.button("÷", key="btn_div"):
    st.session_state.calc_expr += "/"
    st.rerun()

b5, b6, b7, b8 = st.columns(4)
with b5:
  if st.button("7", key="btn_7"):
    st.session_state.calc_expr += "7"
    st.rerun()
with b6:
  if st.button("8", key="btn_8"):
    st.session_state.calc_expr += "8"
    st.rerun()
with b7:
  if st.button("9", key="btn_9"):
    st.session_state.calc_expr += "9"
    st.rerun()
with b8:
  if st.button("×", key="btn_mul"):
    st.session_state.calc_expr += "*"
    st.rerun()

b9, b10, b11, b12 = st.columns(4)
with b9:
  if st.button("4", key="btn_4"):
    st.session_state.calc_expr += "4"
    st.rerun()
with b10:
  if st.button("5", key="btn_5"):
    st.session_state.calc_expr += "5"
    st.rerun()
with b11:
  if st.button("6", key="btn_6"):
    st.session_state.calc_expr += "6"
    st.rerun()
with b12:
  if st.button("-", key="btn_sub"):
    st.session_state.calc_expr += "-"
    st.rerun()

b13, b14, b15, b16 = st.columns(4)
with b13:
  if st.button("1", key="btn_1"):
    st.session_state.calc_expr += "1"
    st.rerun()
with b14:
  if st.button("2", key="btn_2"):
    st.session_state.calc_expr += "2"
    st.rerun()
with b15:
  if st.button("3", key="btn_3"):
    st.session_state.calc_expr += "3"
    st.rerun()
with b16:
  if st.button("+", key="btn_add"):
    st.session_state.calc_expr += "+"
    st.rerun()

b17, b18, b19, b20 = st.columns(4)
with b17:
  if st.button("0", key="btn_0"):
    st.session_state.calc_expr += "0"
    st.rerun()
with b18:
  if st.button(".", key="btn_dot"):
    st.session_state.calc_expr += "."
    st.rerun()
with b19:
  if st.button("⌫", key="btn_back"):
    st.session_state.calc_expr = st.session_state.calc_expr[:-1]
    st.rerun()
with b20:
  if st.button("=", key="btn_eq"):
    try:
      # 計算実行
      res = eval(st.session_state.calc_expr)
      st.session_state.calc_expr = str(res)
    except Exception:
      st.session_state.calc_expr = "エラー"
    st.rerun()
