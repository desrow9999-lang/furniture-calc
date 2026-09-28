import math
import streamlit as st

st.set_page_config(
    page_title="家具の数学電卓", page_icon="📐", layout="centered"
)

# スタイリッシュなデザインのためのカスタムCSS
st.markdown(
    """
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        background-color: #4f46e5;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.75rem;
    }
    .stButton>button:hover {
        background-color: #4338ca;
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ヘッダー
st.markdown(
    "<p style='text-align: center; color: #4f46e5; font-size: 14px; font-weight: 600; margin-bottom: 0;'>家具の数学電卓</p>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h1 style='text-align: center; font-size: 24px; margin-top: 0;'>搬入シミュレーター</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #64748b; font-size: 12px;'>諦めてた家具、三平方の定理で通るかもしれません。</p>",
    unsafe_allow_html=True,
)

st.divider()

# 入力フォーム
with st.form("calc_form"):
  st.markdown("### 📦 家具のサイズ (cm)")
  col1, col2, col3 = st.columns(3)
  with col1:
    width = st.number_input("幅 (W)", min_value=0.0, value=80.0, step=1.0)
  with col2:
    depth = st.number_input("奥行 (D)", min_value=0.0, value=45.0, step=1.0)
  with col3:
    height = st.number_input("高さ (H)", min_value=0.0, value=180.0, step=1.0)

  st.markdown("### 🚪 通り道のサイズ (cm) ※任意")
  col_d1, col_d2 = st.columns(2)
  with col_d1:
    door_width = st.number_input("ドアの幅", min_value=0.0, value=75.0, step=1.0)
  with col_d2:
    door_height = st.number_input(
        "ドアの高さ", min_value=0.0, value=190.0, step=1.0
    )

  submitted = st.form_submit_button("数学で判定する")

if submitted:
  # 三平方の定理で立体対角線を計算 (√(w^2 + d^2 + h^2))
  diagonal = math.sqrt(width**2 + depth**2 + height**2)

  st.success("計算が完了しました！")

  # 結果表示
  st.metric(label="📐 立体対角線", value=f"{round(diagonal, 1)} cm")

  min_side = min(width, depth, height)
  min_door = min(door_width, door_height) if (door_width > 0 and door_height > 0) else 0

  if door_width > 0 and door_height > 0:
    door_diagonal = math.sqrt(door_width**2 + door_height**2)
    if min_side <= min_door and diagonal <= door_diagonal:
      st.markdown(
          "🟢 **判定: 搬入できる可能性が高いです！**<br>諦めないで！斜め（対角線）に傾ければ通ります。",
          unsafe_allow_html=True,
      )
    else:
      st.markdown(
          "🔴 **判定: 注意が必要です**<br>そのままではドアや通路の寸法をオーバーしている可能性があります。分解を検討してください。",
          unsafe_allow_html=True,
      )
