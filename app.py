import streamlit as st

st.set_page_config(layout="wide", page_title="Bio-Neural Network Visualizer")

st.title("🧠 仿生神經網路設計器 (36 Nodes)")
st.write("點擊兩個節點以嘗試建立連線。系統會根據規則進行校驗。")

# 初始化 Session State
if 'selected' not in st.session_state:
    st.session_state.selected = []
if 'connections' not in st.session_state:
    st.session_state.connections = []

# 定義節點數據
layers = [1, 2, 3]
types = ['C', 'A', 'B', 'D']
indices = [1, 2, 3]
colors = {'C': '#FFCC00', 'A': '#FF3300', 'B': '#3399FF', 'D': '#9933FF'}

# 繪製介面
cols = st.columns(3)

for i, layer in enumerate(layers):
    with cols[i]:
        st.subheader(f"Layer {layer}")
        for t in types:
            st.write(f"**Type {t}**")
            btn_cols = st.columns(3)
            for j, idx in enumerate(indices):
                node_id = f"{t}{layer}.{idx}"
                
                # 判斷是否被選中
                is_selected = node_id in st.session_state.selected
                label = f"📍 {node_id}" if is_selected else node_id
                
                if btn_cols[j].button(label, key=node_id):
                    st.session_state.selected.append(node_id)
                    
                    if len(st.session_state.selected) == 2:
                        src = st.session_state.selected[0]
                        tgt = st.session_state.selected[1]
                        
                        # --- 規則校驗邏輯 ---
                        # 範例：C 只能連 A 或 B
                        if src.startswith('C'):
                            if not (tgt.startswith('A') or tgt.startswith('B')):
                                st.error(f"❌ 連結無效！{src} 必須跟同層的 A 或 B 建立連結。")
                            else:
                                st.success(f"✅ 已建立連結: {src} ➜ {tgt}")
                                st.session_state.connections.append((src, tgt))
                        else:
                            st.info(f"已記錄連線嘗試: {src} ➜ {tgt} (規則校驗擴充中...)")
                        
                        # 重置選擇
                        st.session_state.selected = [] 

# 顯示目前的連線清單
st.divider()
st.sidebar.header("已建立的連結")
for c in st.session_state.connections:
    st.sidebar.write(f"🔗 {c[0]} -> {c[1]}")

if st.sidebar.button("重置所有連線"):
    st.session_state.connections = []
    st.session_state.selected = []
    st.rerun()
