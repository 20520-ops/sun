import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. 페이지 레이아웃 및 제목 설정
st.set_page_config(page_title="포물선 안테나 시뮬레이터", page_icon="📡", layout="wide")

st.title("📡 기하 심화탐구: 포물선 안테나의 기하학적 성질 시뮬레이션")
st.write("포물선의 방정식 $y = ax^2$을 이용하여 전파가 초점으로 모이는 성질과 안테나의 설계 효율을 실시간으로 분석합니다.")
st.markdown("---")

# 사변형 레이아웃 구성 (왼쪽: 제어판, 오른쪽: 시각화 및 그래프)
with st.sidebar:
    st.header("⚙️ 안테나 기하학 파라미터")
    
    # 포물선 계수 a (y = ax^2)
    a = st.slider("포물선 계수 ($a$)", min_value=0.05, max_value=1.50, value=0.25, step=0.05,
                  help="계수가 커질수록 포물선이 좁고 깊어집니다.")
    
    # 안테나 지름 D
    D = st.slider("안테나 지름 ($D$)", min_value=2.0, max_value=10.0, value=6.0, step=0.5,
                  help="안테나의 전체 가로 폭을 결정합니다.")

# 2. 수학적 및 공학적 기하 계산
# 초점 거리 p 계산: y = ax^2 은 x^2 = (1/a)y 이므로 4p = 1/a => p = 1 / (4a)
p = 1 / (4 * a)

# 안테나의 깊이 (H) 계산: x가 D/2 일 때의 y값
H = a * (D / 2) ** 2

# 안테나 공학 핵심 지표: f/D 비 (Focal length to Diameter ratio)
# 실제 위성 안테나는 f/D가 0.35 ~ 0.45 일 때 수신 효율(전파 밀집도 및 노이즈 차단)이 극대화됩니다.
f_over_D = p / D
# 효율 모델링 (최적점 0.38 기준의 가우시안 곡선 공식 적용)
efficiency = max(0.0, 100 * np.exp(-25 * (f_over_D - 0.38) ** 2))

# 3. 화면 배치 (두 개의 컬럼)
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🔍 포물선 기하 구조 및 전파 반사 경로")
    
    # 포물선 궤적 계산
    x_orbit = np.linspace(-D/2, D/2, 500)
    y_orbit = a * (x_orbit ** 2)
    
    fig_antenna = go.Figure()
    
    # ① 포물선 안테나 본체 그리기
    fig_antenna.add_trace(go.Scatter(
        x=x_orbit, y=y_orbit,
        mode='lines',
        line=dict(color='#00CC96', width=4),
        name='안테나 단면 ($y = ax^2$)'
    ))
    
    # ② 초점 F(0, p) 표시
    fig_antenna.add_trace(go.Scatter(
        x=[0], y=[p],
        mode='markers+text',
        marker=dict(size=14, color='red', symbol='diamond'),
        name=f'초점 F (0, {p:.2f})',
        text=[f'초점 F(0, {p:.2f})'], textposition='top center'
    ))
    
    # ③ 입사되는 전파 및 반사 경로 시뮬레이션 (수학적 시각화)
    # 지름 범위 내에서 7개의 전파 레이를 생성
    ray_x = np.linspace(-D/2 * 0.9, D/2 * 0.9, 7)
    y_top = H + p * 0.5 # 전파가 내려오기 시작하는 상단 높이
    
    for rx in ray_x:
        if rx == 0: continue # 중심선은 중복되므로 제외
        ry = a * (rx ** 2) # 포물선 표면에 부딪히는 y 좌표
        
        # 전파선 추가 (상단 -> 포물선 표면 -> 초점)
        fig_antenna.add_trace(go.Scatter(
            x=[rx, rx, 0],
            y=[y_top, ry, p],
            mode='lines',
            line=dict(color='rgba(255, 215, 0, 0.6)', width=1.5, dash='dash' if ry==y_top else 'solid'),
            showlegend=False
        ))
        
    # 기하학적 왜곡 방지를 위한 1:1 비율 설정 (Aspect Ratio)
    max_val = max(D/2, y_top) + 0.5
    fig_antenna.update_layout(
        template="plotly_dark",
        width=650, height=550,
        xaxis=dict(title="X 좌표", range=[-max_val, max_val], scaleratio=1, scaleanchor="y"),
        yaxis=dict(title="Y 좌표", range=[-0.5, max_val]),
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True
    )
    
    st.plotly_chart(fig_antenna, use_container_width=True)

with col2:
    st.subheader("📊 계수 변화에 따른 수신 효율")
    
    # 계수 a의 변화 범위에 따른 효율 그래프 생성 (지름 D는 고정된 상태)
    a_range = np.linspace(0.05, 1.50, 300)
    p_range = 1 / (4 * a_range)
    f_D_range = p_range / D
    eff_range = 100 * np.exp(-25 * (f_D_range - 0.38) ** 2)
    
    fig_eff = go.Figure()
    
    # 효율 곡선
    fig_eff.add_trace(go.Scatter(
        x=a_range, y=eff_range,
        mode='lines',
        line=dict(color='#636EFA', width=2.5),
        name='수신 효율 곡선'
    ))
    
    # 현재 설정된 계수 a의 위치 표시
    fig_eff.add_trace(go.Scatter(
        x=[a], y=[efficiency],
        mode='markers',
        marker=dict(size=12, color='red', symbol='circle'),
        name='현재 안테나 설정 상태'
    ))
    
    fig_eff.update_layout(
        template="plotly_dark",
        height=300,
        xaxis=dict(title="포물선 계수 (a)"),
        yaxis=dict(title="수신 효율 (%)", range=[0, 105]),
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False
    )
    
    st.plotly_chart(fig_eff, use_container_width=True)
    
    # 실시간 데이터 지표 출력
    st.markdown("### 📐 실시간 기하학적 데이터")
    st.metric(label="🎯 초점의 Y 좌표 ($p$)", value=f"{p:.3f}")
    st.metric(label="📐 안테나 중심 깊이 ($H$)", value=f"{H:.3f}")
    st.metric(label="📡 초점거리/지름 비 ($f/D$)", value=f"{f_over_D:.3f}")
    st.metric(label="🚀 현재 계산된 전파 수신 효율", value=f"{efficiency:.1f} %")

# 4. 심화 탐구를 위한 기하학 해설 가이드
st.markdown("---")
st.subheader("💡 세특 심화탐구를 위한 기하학 및 공학적 원리 해설")
st.markdown("""
* **포물선의 광학적 성질:** 포물선의 축에 평행하게 들어오는 모든 빛(전파)은 포물선 표면에 부딪힌 후 반사되어 반드시 하나의 점, 즉 **초점 $F(0, p)$**로 모이게 됩니다. 반대로 초점에서 빛을 쏘면 완벽하게 직선으로 뻗어나가므로 탐조등이나 손전등의 원리가 되기도 합니다.
* **계수 $a$와 초점의 관계:** 방정식 $y = ax^2$에서 계수 $a$가 커질수록 포물선의 폭은 좁아지고 깊이는 깊어지며, 초점 거리 $p = \\frac{1}{4a}$는 반비례하여 원점과 가까워집니다.
* **공학적 심화 ($f/D$ 비):** 안테나 공학에서는 단순히 전파를 모으는 것을 넘어, 초점이 너무 멀면 주변 노이즈가 유입되고($f/D$ 가 큰 경우), 초점이 너무 가까우면 안테나 자체 구조물에 의해 전파가 가려지는 블로킹 현상($f/D$ 가 작은 경우)이 발생합니다. 따라서 본 시뮬레이터는 기하학적 최적 밸런스인 $f/D \\approx 0.38$ 부근에서 최고의 효율을 내도록 수학적으로 설계되어 있습니다.
""")
