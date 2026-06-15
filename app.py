import streamlit as st

st.set_page_config(layout="wide", page_title="Bio-Neural Network Visualizer")

st.title("🧠 仿生神經網路設計器 (動態拓撲版)")
st.write("點擊節點建立連線。B 節點已升級為各層的全局樞紐，下方將即時生成帶箭頭的連線圖。")

# 初始化 Session State
if 'selected' not in st.session_state:
    st.session_state.selected = []
if 'connections' not in st.session_state:
    # 預載最基礎的感覺-運動反射迴圈
    st.session_state.connections = [
        ("動器1", "外輸入來源"),
        ("動器2", "外輸入來源"),
        ("外輸入來源", "外輸入1"),
        ("外輸入來源", "外輸入2"),
        ("外輸入來源", "外輸入3"),
        ("外輸入1", "C1.1"),
        ("C1.1", "A1.1"),
        ("A1.1", "C2.1"),
        ("C2.1", "A2.1"),
        ("A2.1", "動器1")
    ]

# --- 輔助函式：渲染可點擊的節點 ---
def render_node(node_id, label_prefix=""):
    is_selected = node_id in st.session_state.selected
    display_label = f"🎯 [選定] {label_prefix}{node_id}" if is_selected else f"{label_prefix}{node_id}"
    
    # 根據節點類型給定按鈕樣式 (Streamlit 原生支援 primary, secondary)
    btn_type = "primary" if is_selected else "secondary"
    
    if st.button(display_label, key=node_id, type=btn_type, use_container_width=True):
        st.session_state.selected.append(node_id)
        
        if len(st.session_state.selected) == 2:
            src = st.session_state.selected[0]
            tgt = st.session_state.selected[1]
            
            st.session_state.connections.append((src, tgt))
            st.success(f"✅ 已建立連結: {src} ➜ {tgt}")
            
            st.session_state.selected = []
            st.rerun()

# ==========================================
# 介面佈局：左(外) 1.5 : 中(核) 6 : 右(內) 1.5
# ==========================================
left_col, center_col, right_col = st.columns([1.5, 6, 1.5])

# --- 左側：外輸入與環境 ---
with left_col:
    st.subheader("🌍 外部環境")
    render_node("外輸入來源", "🔄 ")
    st.divider()
    render_node("外輸入1", "📥 ")
    render_node("外輸入2", "📥 ")
    render_node("外輸入3", "📥 ")

# --- 中間：核心神經網路 (B已改為層級全局節點) ---
with center_col:
    layers = [1, 2, 3]
    types_grid = ['C', 'A', 'D'] # C, A, D 保留 3 個子節點
    indices = [1, 2, 3]
    
    layer_cols = st.columns(3)
    for i, layer in enumerate(layers):
        with layer_cols[i]:
            st.subheader(f"Layer {layer}")
            
            # 將 B 獨立繪製為該層的單一樞紐
            st.markdown(f"**全局總線 (Hub)**")
            render_node(f"B{layer}", "🌐 ")
            st.divider()
            
            # 繪製 C, A, D 矩陣
            for t in types_grid:
                st.caption(f"**Type {t}**")
                btn_cols = st.columns(3)
                for j, idx in enumerate(indices):
                    node_id = f"{t}{layer}.{idx}"
                    with btn_cols[j]:
                        render_node(node_id)

# --- 右側：內輸入 ---
with right_col:
    st.subheader("💭 內部訊號")
    render_node("內輸入1", "🧠 ")
    render_node("內輸入2", "🧠 ")

# --- 下方：動器 ---
st.divider()
space_l, act1_col, act2_col, space_r = st.columns([2, 2, 2, 2])
with act1_col:
    render_node("動器1", "🦾 ")
with act2_col:
    render_node("動器2", "🦾 ")

# ==========================================
# 動態拓撲圖生成 (Mermaid.js)
# ==========================================
st.divider()
st.subheader("📊 即時神經網路連線圖")

if st.session_state.connections:
    # 建立 Mermaid 語法字串
    mermaid_code = "graph TD\n"
    
    # 處理 ID 字元（避免 Mermaid 因特殊符號如小數點報錯）
    def clean_id(node_name):
        return node_name.replace(".", "_")
    
    for src, tgt in st.session_state.connections:
        clean_src = clean_id(src)
        clean_tgt = clean_id(tgt)
        # 繪製帶箭頭的線
        mermaid_code += f'    {clean_src}["{src}"] --> {clean_tgt}["{tgt}"]\n'
    
    # 使用 Streamlit 原生 Markdown 渲染 Mermaid
    st.markdown(f"```mermaid\n{mermaid_code}\n```")
else:
    st.info("目前沒有連線，點擊上方節點開始建立！")

# ==========================================
# 側邊欄控制
# ==========================================
st.sidebar.header("控制台")
if st.sidebar.button("清空所有連線 (Reset)", type="primary"):
    st.session_state.connections = []
    st.session_state.selected = []
    st.rerun()
