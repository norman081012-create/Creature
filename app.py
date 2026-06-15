import streamlit as st
import random

st.set_page_config(layout="wide", page_title="Bio-Neural Simulator (Strict Rules)")

st.title("🧠 仿生神經網路模擬器 (嚴格規則與隨機生成版)")
st.write("已刪除冗餘節點 (D1, D2, A3)，並寫死連線規則。B 節點成為唯一交匯樞紐。")

# ==========================================
# 初始化 Session State 與預設迴圈
# ==========================================
if 'selected' not in st.session_state:
    st.session_state.selected = []
if 'connections' not in st.session_state:
    # 載入你要求的基礎組合迴圈 (已自動補齊 C1->A1->B 的規則)
    st.session_state.connections = [
        ("外輸入來源", "外輸入1"),
        ("外輸入1", "C1.1"),
        ("C1.1", "A1.1"),      # 嚴格規則：C1 只能連 A1
        ("A1.1", "B1"),        # 嚴格規則：A1 只能連 B
        ("B1", "C2.1"),
        ("C2.1", "A2.1"),
        ("A2.1", "動器1"),
        ("動器1", "外輸入來源"), # 改變環境
        ("動器1", "內輸入1"),   # 行動後產生內在回饋
        ("內輸入1", "C3.1"),
        ("C3.1", "D3.1"),
        ("D3.1", "B1")         # 理智去干預 B1
    ]

# ==========================================
# 嚴格連線規則校驗器 (寫死規則)
# ==========================================
def validate_connection(src, tgt):
    # 外部環境與內在動機
    if src == "外輸入來源" and tgt.startswith("外輸入"): return True
    if src.startswith("外輸入") and tgt.startswith("C1"): return True
    if src.startswith("內輸入") and tgt.startswith("C3"): return True
    if src.startswith("動器"): return True # 動器可以連回輸入源
    
    # Layer 1 規則
    if src.startswith("C1") and tgt.startswith("A1"): return True
    if src.startswith("A1") and tgt.startswith("B"): return True
    
    # Layer 3 規則
    if src.startswith("C3") and tgt.startswith("D3"): return True
    if src.startswith("D3") and tgt.startswith("B"): return True
    
    # Layer 2 規則
    if src.startswith("B") and tgt.startswith("C2"): return True
    if src.startswith("C2") and tgt.startswith("A2"): return True
    if src.startswith("A2") and tgt.startswith("動器"): return True
    
    return False

# ==========================================
# 隨機生成合法網路功能
# ==========================================
def generate_random_network():
    st.session_state.connections = []
    nodes_c1 = ["C1.1", "C1.2", "C1.3"]
    nodes_a1 = ["A1.1", "A1.2", "A1.3"]
    nodes_c3 = ["C3.1", "C3.2", "C3.3"]
    nodes_d3 = ["D3.1", "D3.2", "D3.3"]
    nodes_b  = ["B1", "B2", "B3"]
    nodes_c2 = ["C2.1", "C2.2", "C2.3"]
    nodes_a2 = ["A2.1", "A2.2", "A2.3"]
    acts = ["動器1", "動器2"]
    
    # 隨機產生 2~4 條本能路徑 (L1 -> B)
    for _ in range(random.randint(2, 4)):
        c1, a1, b = random.choice(nodes_c1), random.choice(nodes_a1), random.choice(nodes_b)
        st.session_state.connections.extend([("外輸入來源", "外輸入1"), ("外輸入1", c1), (c1, a1), (a1, b)])
        
    # 隨機產生 1~3 條理智路徑 (L3 -> B)
    for _ in range(random.randint(1, 3)):
        c3, d3, b = random.choice(nodes_c3), random.choice(nodes_d3), random.choice(nodes_b)
        st.session_state.connections.extend([("內輸入1", c3), (c3, d3), (d3, b)])
        
    # 將有收到訊號的 B 往下連到動器
    active_bs = set([tgt for src, tgt in st.session_state.connections if tgt.startswith("B")])
    for b in active_bs:
        c2, a2, act = random.choice(nodes_c2), random.choice(nodes_a2), random.choice(acts)
        st.session_state.connections.extend([(b, c2), (c2, a2), (a2, act)])
    
    # 去除重複連線
    st.session_state.connections = list(dict.fromkeys(st.session_state.connections))

# ==========================================
# 介面渲染
# ==========================================
def render_node(node_id, label_prefix=""):
    is_selected = node_id in st.session_state.selected
    display_label = f"🎯 [選定] {label_prefix}{node_id}" if is_selected else f"{label_prefix}{node_id}"
    btn_type = "primary" if is_selected else "secondary"
    
    if st.button(display_label, key=node_id, type=btn_type, use_container_width=True):
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

left_col, center_col, right_col = st.columns([1.5, 6, 1.5])

with left_col:
    st.subheader("🌍 外在環境")
    render_node("外輸入來源", "🔄 ")
    st.divider()
    render_node("外輸入1", "📥 ")

with center_col:
    # 依照新規則，只顯示合法的節點
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
for conn in list(st.session_state.connections):
    col1, col2 = st.sidebar.columns([4, 1])
    col1.text(f"{conn[0]} ➜ {conn[1]}")
    if col2.button("❌", key=f"del_{conn[0]}_{conn[1]}"):
        st.session_state.connections.remove(conn)
        st.rerun()

st.sidebar.divider()
if st.sidebar.button("🎲 隨機生成合法網路", type="primary"):
    generate_random_network()
    st.rerun()

if st.sidebar.button("清空畫布"):
    st.session_state.connections = []
    st.session_state.selected = []
    st.rerun()
