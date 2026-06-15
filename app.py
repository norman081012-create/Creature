import streamlit as st

st.set_page_config(layout="wide", page_title="Bio-Neural Network Visualizer")

st.title("🧠 仿生神經網路設計器 (精簡節點 & 單線刪除版)")
st.write("已將節點精簡化：每層 1個C、1個A、1個D、2個B。您可以在左側邊欄單獨刪除已建立的連線。")

# 初始化 Session State
if 'selected' not in st.session_state:
    st.session_state.selected = []
if 'connections' not in st.session_state:
    st.session_state.connections = []  # 給你一張乾淨的畫布

# --- 輔助函式：渲染可點擊的節點 ---
def render_node(node_id, label_prefix=""):
    is_selected = node_id in st.session_state.selected
    display_label = f"🎯 [選定] {label_prefix}{node_id}" if is_selected else f"{label_prefix}{node_id}"
    btn_type = "primary" if is_selected else "secondary"
    
    if st.button(display_label, key=node_id, type=btn_type, use_container_width=True):
        st.session_state.selected.append(node_id)
        
        # 當選滿兩個節點時，建立連線
        if len(st.session_state.selected) == 2:
            src = st.session_state.selected[0]
            tgt = st.session_state.selected[1]
            
            # 防呆：避免重複建立一模一樣的連線
            if (src, tgt) not in st.session_state.connections:
                st.session_state.connections.append((src, tgt))
                st.success(f"✅ 已建立連結: {src} ➜ {tgt}")
            else:
                st.warning(f"⚠️ 連結 {src} ➜ {tgt} 已經存在囉！")
            
            st.session_state.selected = []
            st.rerun()

# ==========================================
# 介面佈局：左(外) 1.5 : 中(核) 6 : 右(內) 1.5
# ==========================================
left_col, center_col, right_col = st.columns([1.5, 6, 1.5])

# --- 左側：外在實體 ---
with left_col:
    st.subheader("🌍 外在環境")
    render_node("外輸入來源", "🔄 ")
    st.divider()
    render_node("外輸入1", "📥 ")

# --- 中間：核心神經網路 (精簡版) ---
with center_col:
    layers = [1, 2, 3]
    layer_cols = st.columns(3)
    
    for i, layer in enumerate(layers):
        with layer_cols[i]:
            st.subheader(f"Layer {layer}")
            
            # B 節點 (2個)
            st.markdown("**B (Binding / 雙軌樞紐)**")
            b_cols = st.columns(2)
            with b_cols[0]: render_node(f"B{layer}.1")
            with b_cols[1]: render_node(f"B{layer}.2")
            
            st.divider()
            
            # C, A, D 節點 (各1個)
            st.markdown("**C / A / D (處理核心)**")
            render_node(f"C{layer}.1", "🟡 ")
            render_node(f"A{layer}.1", "🔴 ")
            render_node(f"D{layer}.1", "🟣 ")

# --- 右側：內在動機 ---
with right_col:
    st.subheader("💭 內在訊號")
    render_node("內輸入1", "🧠 ")

# --- 下方：動器 ---
st.divider()
space_l, act_col, space_r = st.columns([3, 2, 3])
with act_col:
    render_node("動器1", "🦾 ")

# ==========================================
# 動態拓撲圖生成 (Mermaid.js)
# ==========================================
st.divider()
st.subheader("📊 動態拓撲圖")

if st.session_state.connections:
    mermaid_code = "graph TD\n"
    def clean_id(node_name): 
        return node_name.replace(".", "_")
    
    for src, tgt in st.session_state.connections:
        mermaid_code += f'    {clean_id(src)}["{src}"] --> {clean_id(tgt)}["{tgt}"]\n'
    
    st.markdown(f"```mermaid\n{mermaid_code}\n```")
else:
    st.info("目前沒有連線，點擊上方節點開始建立！")

# ==========================================
# 側邊欄：單線刪除與全域控制
# ==========================================
st.sidebar.header("🔗 當前連線管理")
st.sidebar.write("點擊 ❌ 即可單獨刪除連線")

# 使用 list() 複製一份來進行迴圈，確保刪除時不會影響正在迭代的陣列
for conn in list(st.session_state.connections):
    col1, col2 = st.sidebar.columns([4, 1])
    col1.text(f"{conn[0]} ➜ {conn[1]}")
    # 給每個刪除按鈕獨立的 key
    if col2.button("❌", key=f"del_{conn[0]}_{conn[1]}"):
        st.session_state.connections.remove(conn)
        st.rerun()

st.sidebar.divider()
if st.sidebar.button("清空所有連線 (Reset)", type="primary"):
    st.session_state.connections = []
    st.session_state.selected = []
    st.rerun()
