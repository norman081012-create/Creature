import streamlit as st
import random

st.set_page_config(layout="wide", page_title="Bio-Neural Simulator")

st.title("🧠 仿生神經網路模擬器 (空間加成權重版)")
st.write("已實裝生物學「空間加成 (Spatial Summation)」：興奮(+1)與抑制(-1)將進行算術加總。")

# ==========================================
# 初始化 Session State
# ==========================================
if 'selected' not in st.session_state:
    st.session_state.selected = []
if 'node_states' not in st.session_state:
    st.session_state.node_states = {} 
if 'connections' not in st.session_state:
    # 預設迴圈
    st.session_state.connections = [
        ("外輸入來源", "外輸入1"),
        ("外輸入1", "C1.1"),
        ("C1.1", "A1.1"),      
        ("A1.1", "B1"),        
        ("B1", "C2.1"),
        ("C2.1", "A2.1"),
        ("A2.1", "動器1"),
        ("動器1", "外輸入來源"), 
        ("動器1", "內輸入1"),   
        ("內輸入1", "C3.1"),
        ("C3.1", "D3.1"),
        ("D3.1", "B1")         
    ]

# ==========================================
# 模式切換
# ==========================================
mode = st.radio("切換系統模式：", ["🛠️ 編輯模式 (建立/刪除連線)", "⚡ 運行模式 (發送刺激訊號)"], horizontal=True)
st.divider()

# ==========================================
# 嚴格連線規則校驗器
# ==========================================
def validate_connection(src, tgt):
    if src == "外輸入來源" and tgt.startswith("外輸入"): return True
    if src.startswith("外輸入") and tgt.startswith("C1"): return True
    if src.startswith("內輸入") and tgt.startswith("C3"): return True
    if src.startswith("動器"): return True 
    if src.startswith("C1") and tgt.startswith("A1"): return True
    if src.startswith("A1") and tgt.startswith("B"): return True
    if src.startswith("C3") and tgt.startswith("D3"): return True
    if src.startswith("D3") and tgt.startswith("B"): return True
    if src.startswith("B") and tgt.startswith("C2"): return True
    if src.startswith("C2") and tgt.startswith("A2"): return True
    if src.startswith("A2") and tgt.startswith("動器"): return True
    return False

# ==========================================
# 動態邏輯運算引擎 (空間加成權重更新)
# ==========================================
def recalculate_network():
    rev_graph = {}
    for src, tgt in st.session_state.connections:
        if tgt not in rev_graph: rev_graph[tgt] = []
        rev_graph[tgt].append(src)
        
    for _ in range(6): 
        new_states = dict(st.session_state.node_states)
        for node in rev_graph.keys():
            if node in ["外輸入來源", "內輸入1"]: 
                continue 
            
            # 👉 神經權重計算 (Net Signal)
            net_signal = 0
            
            # 加總所有傳進來的訊號
            for src in rev_graph[node]:
                if st.session_state.node_states.get(src, 0) == 1:
                    if src.startswith('D'):
                        net_signal -= 1  # 抑制訊號扣 1 分
                    else:
                        net_signal += 1  # 興奮訊號加 1 分
                        
            # 👉 閾值判斷 (Threshold)
            if net_signal > 0:
                new_states[node] = 1  # 興奮大於抑制，發火 (例如: 2A - 1D = +1)
            else:
                new_states[node] = 0  # 互相抵消或抑制大於興奮，保持安靜 (例如: 1A - 1D = 0)
                
        st.session_state.node_states = new_states

# ==========================================
# 介面渲染
# ==========================================
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
                src, tgt = st.session_state.selected[0], st.session_state.selected[1]
                if validate_connection(src, tgt):
                    if (src, tgt) not in st.session_state.connections:
                        st.session_state.connections.append((src, tgt))
                        st.success(f"✅ 已建立連結: {src} ➜ {tgt}")
                else:
                    st.error(f"❌ 違反嚴格規則！無法建立 {src} ➜ {tgt} 的連線。")
                st.session_state.selected = []
                st.rerun()

    else:
        # ⚡ 運行模式
        btn_type = "primary" if state == 1 else "secondary"
        display_label = f"{label_prefix}{node_id} ({state})"
        
        if st.button(display_label, key=f"run_{node_id}", type=btn_type, use_container_width=True):
            if node_id in ["外輸入來源", "內輸入1", "動器1", "動器2"]:
                st.session_state.node_states[node_id] = 1 - state
                recalculate_network() 
                st.rerun()
            else:
                st.info("請點擊『輸入來源』或『動器』來發起全網連鎖反應！")

# ==========================================
# 網格佈局
# ==========================================
left_col, center_col, right_col = st.columns([1.5, 6, 1.5])

with left_col:
    st.subheader("🌍 外在環境")
    render_node("外輸入來源", "🔄 ")
    st.divider()
    render_node("外輸入1", "📥 ")
    render_node("外輸入2", "📥 ")

with center_col:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Layer 1 (感覺/衝動)")
        for i in range(1, 4): render_node(f"C1.{i}", "🟡 ")
        st.divider()
        for i in range(1, 4): render_node(f"A1.{i}", "🔴 ")
        
    with col2:
        st.subheader("B (整合樞紐)")
        for i in range(1, 4): render_node(f"B{i}", "🌐 ")
        st.divider()
        st.subheader("Layer 2 (運動/執行)")
        for i in range(1, 4): render_node(f"C2.{i}", "🟡 ")
        st.divider()
        for i in range(1, 4): render_node(f"A2.{i}", "🔴 ")

    with col3:
        st.subheader("Layer 3 (認知/抑制)")
        for i in range(1, 4): render_node(f"C3.{i}", "🟡 ")
        st.divider()
        for i in range(1, 4): render_node(f"D3.{i}", "🟣 ")

with right_col:
    st.subheader("💭 內在訊號")
    render_node("內輸入1", "🧠 ")
    render_node("內輸入2", "🧠 ")

st.divider()
space_l, act1_col, act2_col, space_r = st.columns([2, 2, 2, 2])
with act1_col: render_node("動器1", "🦾 ")
with act2_col: render_node("動器2", "🦾 ")

# ==========================================
# 動態拓撲圖與側邊欄管理
# ==========================================
st.divider()
st.subheader("📊 嚴格架構拓撲圖")

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
if st.sidebar.button("清空畫布與狀態", type="primary"):
    st.session_state.connections = []
    st.session_state.selected = []
    st.session_state.node_states = {}
    st.rerun()
