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

# タブ構成
tab1, tab2, tab3 = st.tabs(
    ["🚪 搬入・通過チェッカー", "📐 隙間・設置チェッカー", "🔢 現場のメモ電卓"]
)

with tab1:
  with st.form("transport_form"):
    st.markdown("### 📦 家具・家電のサイズ (cm)")
    c1, c2, c3 = st.columns(3)
    with c1:
      w = st.number_input(
          "幅 (W)", min_value=0.0, value=80.0, step=1.0, key="t_w"
      )
    with c2:
      d = st.number_input(
          "奥行 (D)", min_value=0.0, value=45.0, step=1.0, key="t_d"
      )
    with c3:
      h = st.number_input(
          "高さ (H)", min_value=0.0, value=180.0, step=1.0, key="t_h"
      )

    st.markdown("### 🚪 通り道のサイズ (cm)")
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

with tab2:
  with st.form("gap_form"):
    st.markdown("### 🏠 設置スペースのクリアランス")
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
        label="✨ 両側のトータル余裕 (Clearance)",
        value=f"{round(margin, 1)} cm",
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

with tab3:
  st.markdown("### 🔢 現場のメモ電卓")
  st.markdown(
      "<p style='font-size:11px; color:#64748b;'>採寸時の足し算や、ミリからセンチへの換算などにサッと使えます。</p>",
      unsafe_allow_html=True,
  )

  calc_input = st.text_input(
      "計算式を入力 (例: 80 + 15 - 3)", value="", placeholder="例: 120 + 45"
  )
  if calc_input:
    try:
      # 安全に数式を評価
      # 数字と基本的な演算子のみ許可
      allowed_chars = set("0123456789+-*/(). ")
      if all(c in allowed_chars for c in calc_input):
        calc_result = eval(calc_input)
        st.metric(label="計算結果", value=f"{calc_result} cm")
      else:
        st.error(
            "使用できるのは数字と四則演算子 (+, -, *, /) のみです。"
        )
    except Exception:
      st.warning("正しい数式を入力してください。")

  st.markdown("---")
  st.markdown("**💡 よく使う換算メモ**")
  st.markdown("- 10 mm = 1 cm")
  st.markdown("- 100 cm = 1 m")
