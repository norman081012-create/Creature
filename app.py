import streamlit as st

st.set_page_config(layout="wide", page_title="Bio-Neural Network Visualizer")

st.title("🧠 仿生神經網路設計器 (雙引擎架構)")
st.write("已套用最新邏輯：物理反射迴圈 (1-2-外在) 與 認知控制迴圈 (內在-3-B) 雙軌並行。")

if 'selected' not in st.session_state:
    st.session_state.selected = []
if 'connections' not in st.session_state:
    # 完美實踐你的最新控制流
    st.session_state.connections = [
        # 物理循環引擎 (Physical Engine)
        ("外輸入來源", "外輸入1"),    # 外在 -> 1 (環境提供刺激)
        ("外輸入1", "C1.1"),        # 進入 L1
        ("C1.1", "C2.1"),           # 1 控制 2
        ("C2.1", "動器1"),          # 2 控制 動器
        ("動器1", "外輸入來源"),      # 動器 控制 外在
        
        # 認知覆寫引擎 (Cognitive Engine)
        ("內輸入1", "C3.1"),        # 內在 控制 3
        ("C3.1", "B1")              # 3 控制 B (B 準備調控中樞)
    ]

def render_node(node_id, label_prefix=""):
    is_selected = node_id in st.session_state.selected
    display_label = f"🎯 [選定] {label_prefix}{node_id}" if is_selected else f"{label_prefix}{node_id}"
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

left_col, center_col, right_col = st.columns([1.5, 6, 1.5])

with left_col:
    st.subheader("🌍 外在實體")
    render_node("外輸入來源", "🔄 ")
    st.divider()
    render_node("外輸入1", "📥 ")

with center_col:
    layers = [1, 2, 3]
    types_grid = ['C', 'A', 'D'] 
    indices = [1, 2, 3]
    
    layer_cols = st.columns(3)
    for i, layer in enumerate(layers):
        with layer_cols[i]:
            st.subheader(f"Layer {layer}")
            st.markdown(f"**全局總線 (Hub)**")
            render_node(f"B{layer}", "🌐 ")
            st.divider()
            for t in types_grid:
                btn_cols = st.columns(3)
                for j, idx in enumerate(indices):
                    with btn_cols[j]:
                        render_node(f"{t}{layer}.{idx}")

with right_col:
    st.subheader("💭 內在動機")
    render_node("內輸入1", "🧠 ")

st.divider()
space_l, act1_col, act2_col, space_r = st.columns([2, 2, 2, 2])
with act1_col:
    render_node("動器1", "🦾 ")

st.divider()
st.subheader("📊 雙軌邏輯拓撲圖")

if st.session_state.connections:
    mermaid_code = "graph TD\n"
    def clean_id(node_name): return node_name.replace(".", "_")
    
    for src, tgt in st.session_state.connections:
        mermaid_code += f'    {clean_id(src)}["{src}"] --> {clean_id(tgt)}["{tgt}"]\n'
    st.markdown(f"```mermaid\n{mermaid_code}\n```")

st.sidebar.header("控制台")
if st.sidebar.button("清空所有連線 (Reset)", type="primary"):
    st.session_state.connections = []
    st.session_state.selected = []
    st.rerun()
