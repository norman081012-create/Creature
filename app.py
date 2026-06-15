import streamlit as st

st.set_page_config(layout="wide", page_title="Bio-Neural Network Visualizer")

st.title("🧠 仿生神經網路設計器 (含環境互動迴圈)")
st.write("點擊任何兩個節點建立連線。目前已預載動器與外部環境的互動迴圈。")

# 初始化 Session State
if 'selected' not in st.session_state:
    st.session_state.selected = []
if 'connections' not in st.session_state:
    # 預先載入你設定的環境回饋機制連線
    st.session_state.connections = [
        ("動器1", "外輸入來源"),
        ("動器2", "外輸入來源"),
        ("外輸入來源", "外輸入1"),
        ("外輸入來源", "外輸入2"),
        ("外輸入來源", "外輸入3")
    ]

# --- 輔助函式：渲染可點擊的節點 ---
def render_node(node_id, label_prefix=""):
    is_selected = node_id in st.session_state.selected
    # 如果被選中，加上圖示提示
    display_label = f"🎯 [已選] {label_prefix}{node_id}" if is_selected else f"{label_prefix}{node_id}"
    
    if st.button(display_label, key=node_id, use_container_width=True):
        st.session_state.selected.append(node_id)
        
        if len(st.session_state.selected) == 2:
            src = st.session_state.selected[0]
            tgt = st.session_state.selected[1]
            
            # 建立連線並記錄
            st.session_state.connections.append((src, tgt))
            st.success(f"✅ 已建立連結: {src} ➜ {tgt}")
            
            # 重置選擇並重新整理畫面
            st.session_state.selected = []
            st.rerun()

# ==========================================
# 介面佈局開始
# 比例分配：左(外輸入) 1.5 : 中(核心神經) 6 : 右(內輸入) 1.5
# ==========================================
left_col, center_col, right_col = st.columns([1.5, 6, 1.5])

# --- 最左邊：外輸入與環境 ---
with left_col:
    st.subheader("🌍 環境與外輸入")
    render_node("外輸入來源", "🔄 ")
    st.divider()
    render_node("外輸入1", "📥 ")
    render_node("外輸入2", "📥 ")
    render_node("外輸入3", "📥 ")

# --- 中間：核心神經網路 (36節點) ---
with center_col:
    layers = [1, 2, 3]
    types = ['C', 'A', 'B', 'D']
    indices = [1, 2, 3]
    
    layer_cols = st.columns(3)
    for i, layer in enumerate(layers):
        with layer_cols[i]:
            st.subheader(f"Layer {layer}")
            for t in types:
                st.caption(f"**Type {t}**")
                btn_cols = st.columns(3)
                for j, idx in enumerate(indices):
                    node_id = f"{t}{layer}.{idx}"
                    with btn_cols[j]:
                        render_node(node_id)

# --- 最右邊：內輸入 ---
with right_col:
    st.subheader("💭 內部訊號")
    render_node("內輸入1", "🧠 ")
    render_node("內輸入2", "🧠 ")

# --- 最下方：動器 ---
st.divider()
st.subheader("🦾 輸出執行 (Actuators)")
# 用空欄位把動器擠在中間，視覺上比較平衡
space_l, act1_col, act2_col, space_r = st.columns([2, 2, 2, 2])
with act1_col:
    render_node("動器1")
with act2_col:
    render_node("動器2")


# ==========================================
# 側邊欄：顯示目前所有連線狀態
# ==========================================
st.sidebar.header("🔗 當前連線清單")
for c in st.session_state.connections:
    st.sidebar.text(f"{c[0]}  ➜  {c[1]}")

if st.sidebar.button("清空所有連線 (Reset)", type="primary"):
    st.session_state.connections = []
    st.session_state.selected = []
    st.rerun()
