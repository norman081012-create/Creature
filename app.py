import streamlit as st

st.set_page_config(layout="wide", page_title="Bio-Neural Simulator")

st.title("🧠 仿生神經網路模擬器 (D 節點抑制反轉版)")

# ==========================================
# 初始化 Session State
# ==========================================
if 'selected' not in st.session_state:
    st.session_state.selected = []
if 'connections' not in st.session_state:
    st.session_state.connections = []
if 'node_states' not in st.session_state:
    st.session_state.node_states = {} # 記錄所有節點的狀態 (0 或 1)

mode = st.radio("切換系統模式：", ["🛠️ 編輯模式 (建立/刪除連線)", "⚡ 運行模式 (發送刺激訊號)"], horizontal=True)
st.divider()

# --- 輔助函式：建立神經網路圖 (Adjacency List) ---
def build_graph():
    graph = {}
    for src, tgt in st.session_state.connections:
        if src not in graph:
            graph[src] = []
        graph[src].append(tgt)
    return graph

# --- 輔助函式：觸發訊號傳遞與 D 節點反轉 ---
def trigger_signal(start_node):
    graph = build_graph()
    
    # 點擊來源節點時，強制翻轉其狀態
    st.session_state.node_states[start_node] = 1 - st.session_state.node_states.get(start_node, 0)
    
    visited = set([start_node])
    queue = [start_node]
    
    while queue:
        curr = queue.pop(0)
        curr_state = st.session_state.node_states.get(curr, 0)
        
        # 核心生理邏輯：只有當前節點處於「激發 (1)」狀態時，才會向下游發送訊號
        if curr_state == 1:
            for neighbor in graph.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    
                    # 判斷訊號來源的屬性
                    if curr.startswith('D'):
                        # 🔴 D 節點專屬邏輯：反轉/抑制。強制將下游目標歸零
                        st.session_state.node_states[neighbor] = 0
                    else:
                        # 🟢 標準節點邏輯：興奮/翻轉。讓下游目標從 0 變 1
                        tgt_state = st.session_state.node_states.get(neighbor, 0)
                        st.session_state.node_states[neighbor] = 1 - tgt_state
                        
                    # 將被影響的下游節點加入佇列，繼續傳導
                    queue.append(neighbor)

# --- 輔助函式：渲染可點擊的節點 ---
def render_node(node_id, label_prefix=""):
    if node_id not in st.session_state.node_states:
        st.session_state.node_states[node_id] = 0
        
    state = st.session_state.node_states[node_id]
    
    if mode == "🛠️ 編輯模式 (建立/刪除連線)":
        is_selected = node_id in st.session_state.selected
        display_label = f"🎯 [選定] {label_prefix}{node_id}" if is_selected else f"{label_prefix}{node_id}"
        btn_type = "primary" if is_selected else "secondary"
        
        if st.button(display_label, key=f"edit_{node_id}", type=btn_type, use_container_width=True):
            st.session_state.selected.append(node_id)
            if len(st.session_state.selected) == 2:
                src = st.session_state.selected[0]
                tgt = st.session_state.selected[1]
                if (src, tgt) not in st.session_state.connections:
                    st.session_state.connections.append((src, tgt))
                    st.success(f"✅ 已建立連結: {src} ➜ {tgt}")
                else:
                    st.warning(f"⚠️ 連結已經存在囉！")
                st.session_state.selected = []
                st.rerun()

    else:
        # ⚡ 運行模式
        btn_type = "primary" if state == 1 else "secondary"
        display_label = f"{label_prefix}{node_id} ({state})"
        
        if st.button(display_label, key=f"run_{node_id}", type=btn_type, use_container_width=True):
            if node_id == "外輸入來源" or node_id == "內輸入1":
                trigger_signal(node_id)
                st.rerun()
            else:
                st.info("請點擊『外輸入來源』或『內輸入1』來發起連鎖反應！")

# ==========================================
# 介面佈局
# ==========================================
left_col, center_col, right_col = st.columns([1.5, 6, 1.5])

with left_col:
    st.subheader("🌍 外在環境")
    render_node("外輸入來源", "🔄 ")
    st.divider()
    render_node("外輸入1", "📥 ")

with center_col:
    layers = [1, 2, 3]
    layer_cols = st.columns(3)
    for i, layer in enumerate(layers):
        with layer_cols[i]:
            st.subheader(f"Layer {layer}")
            st.markdown("**B (Binding / 樞紐)**")
            b_cols = st.columns(2)
            with b_cols[0]: render_node(f"B{layer}.1")
            with b_cols[1]: render_node(f"B{layer}.2")
            
            st.divider()
            st.markdown("**C / A / D (處理核心)**")
            render_node(f"C{layer}.1", "🟡 ")
            render_node(f"A{layer}.1", "🔴 ")
            render_node(f"D{layer}.1", "🟣 ")

with right_col:
    st.subheader("💭 內在訊號")
    render_node("內輸入1", "🧠 ")

st.divider()
space_l, act_col, space_r = st.columns([3, 2, 3])
with act_col:
    render_node("動器1", "🦾 ")

# ==========================================
# 動態拓撲圖與側邊欄管理
# ==========================================
st.divider()
st.subheader("📊 動態拓撲圖")

if st.session_state.connections:
    mermaid_code = "graph TD\n"
    def clean_id(n): return n.replace(".", "_")
    for src, tgt in st.session_state.connections:
        mermaid_code += f'    {clean_id(src)}["{src}"] --> {clean_id(tgt)}["{tgt}"]\n'
    st.markdown(f"```mermaid\n{mermaid_code}\n```")

st.sidebar.header("🔗 當前連線管理")
if mode == "🛠️ 編輯模式 (建立/刪除連線)":
    for conn in list(st.session_state.connections):
        col1, col2 = st.sidebar.columns([4, 1])
        col1.text(f"{conn[0]} ➜ {conn[1]}")
        if col2.button("❌", key=f"del_{conn[0]}_{conn[1]}"):
            st.session_state.connections.remove(conn)
            st.rerun()

st.sidebar.divider()
if st.sidebar.button("清空所有連線與狀態", type="primary"):
    st.session_state.connections = []
    st.session_state.selected = []
    st.session_state.node_states = {}
    st.rerun()
