import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. 페이지 설정 (넓은 레이아웃)
st.set_page_config(page_title="쌍곡선 안테나 시뮬레이터", page_icon="📡", layout="wide")

st.title("📡 고2 기하 심화탐구: 쌍곡선의 성질과 안테나 수신 효율 시뮬레이션")
st.write("교과서 개념인 **쌍곡선 공식 $\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1$**과 **점근선**을 활용하여 안테나 효율을 실시간 분석합니다.")
st.markdown("---")

# 사이드바 제어판 (철저히 고2 교과서 문자로만 구성)
with st.sidebar:
    st.header("📐 쌍곡선 거울면(안테나) 제어")
    a = st.slider("주축 상수 ($a$)", min_value=1.0, max_value=4.0, value=2.0, step=0.1,
                  help="원점에서 안테나 꼭짓점까지의 거리입니다.")
    b = st.slider("공액축 상수 ($b$)", min_value=1.0, max_value=5.0, value=2.5, step=0.1,
                  help="점근선의 기울기(b/a)를 결정하는 상수입니다.")
    y_max = st.slider("안테나 거울의 크기 ($y_{max}$)", min_value=2.0, max_value=6.0, value=4.0, step=0.2)

# 2. 기하학 공식 및 효율 계산
# 초점 거리 c 계산: c^2 = a^2 + b^2
c = np.sqrt(a**2 + b**2)

# 고2 맞춤형 수신 효율 모델링 (점근선 기울기 b/a 가 1.25일 때 최적이 되도록 설정)
# 이심률이라는 단어를 쓰지 않고, 교과서 단어인 '점근선의 기울기'로 효율을 결정함!
asymptote_slope = b / a
optimal_slope = 1.25
efficiency = max(0.0, 100 * np.exp(-3 * (asymptote_slope - optimal_slope) ** 2))

# 3. 화면 배분 (좌측: 안테나 레이트레이싱, 우측: 수신효율 그래프 + 수학 증명)
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🔍 실시간 쌍곡선 전파 경로 시뮬레이션")
    st.caption("⚡ 파란 전파들이 가상 초점 F2를 향해 오다가, 초록색 쌍곡선 거울에 반사되어 골드색 진짜 초점 F1으로 모입니다.")
    
    fig = go.Figure()
    
    # ① 쌍곡선 안테나 거울면 그리기 (우측)
    y_orbit = np.linspace(-y_max, y_max, 400)
    x_orbit = a * np.sqrt(1 + (y_orbit / b)**2)
    fig.add_trace(go.Scatter(x=x_orbit, y=y_orbit, mode='lines', line=dict(color='#00CC96', width=4), name='쌍곡선 거울면'))
    
    # 반대편 쌍곡선 (연하게 흐릿하게 처리)
    fig.add_trace(go.Scatter(x=-x_orbit, y=y_orbit, mode='lines', line=dict(color='rgba(255,255,255,0.1)', width=1.5, dash='dash'), name='반대편 쌍곡선(가상)'))
    
    # ② 점근선 그리기 (y = \pm (b/a)x)
    x_asymp = np.linspace(-c - 2, c + 3, 100)
    fig.add_trace(go.Scatter(x=x_asymp, y=(b/a)*x_asymp, mode='lines', line=dict(color='rgba(255, 255, 255, 0.2)', width=1, dash='dot'), name='점근선'))
    fig.add_trace(go.Scatter(x=x_asymp, y=-(b/a)*x_asymp, mode='lines', line=dict(color='rgba(255, 255, 255, 0.2)', width=1, dash='dot'), showlegend=False))
    
    # ③ 두 초점 F1, F2 표시
    fig.add_trace(go.Scatter(x=[c], y=[0], mode='markers+text', marker=dict(size=12, color='red', symbol='diamond'), name='진짜 초점 F1 (수신기)', text=['F1 (수신기)'], textposition='bottom center'))
    fig.add_trace(go.Scatter(x=[-c], y=[0], mode='markers+text', marker=dict(size=12, color='orange', symbol='diamond-open'), name='가상 초점 F2', text=['F2 (가상초점)'], textposition='bottom center'))
    
    # ④ 전파 레이트레이싱선 그리기
    y_rays = np.linspace(-y_max * 0.8, y_max * 0.8, 5)
    x_rays = a * np.sqrt(1 + (y_rays / b)**2)
    
    for xr, yr in zip(x_rays, y_rays):
        dx = xr - (-c)
        dy = yr - 0
        x_start = xr + dx * 0.3
        y_start = yr + dy * 0.3
        
        # 입사선 (파란색)
        fig.add_trace(go.Scatter(x=[x_start, xr], y=[y_start, yr], mode='lines', line=dict(color='#636EFA', width=2), showlegend=False))
        # 가상선 (주황 점선)
        fig.add_trace(go.Scatter(x=[xr, -c], y=[yr, 0], mode='lines', line=dict(color='rgba(255, 165, 0, 0.3)', width=1.5, dash='dash'), showlegend=False))
        # 반사선 (골드색)
        fig.add_trace(go.Scatter(x=[xr, c], y=[yr, 0], mode='lines', line=dict(color='gold', width=2), showlegend=False))

    # 1:1 기하학적 비율 고정
    max_boundary = max(c + 3, y_max + 1)
    fig.update_layout(
        template="plotly_dark",
        width=700, height=550,
        xaxis=dict(title="X 좌표", range=[-max_boundary, max_boundary], scaleratio=1, scaleanchor="y"),
        yaxis=dict(title="Y 좌표", range=[-max_boundary, max_boundary]),
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 점근선 기울기에 따른 수신 효율 그래프")
    st.caption("💡 공액축 상수 $b$가 변하면서 점근선의 기울기가 최적일 때(1.25) 안테나 효율이 100%에 도달합니다.")
    
    # 효율 그래프 그리기 (현재 선택한 a값 고정, b값 변화에 따른 그래프)
    b_range = np.linspace(1.0, 5.0, 200)
    slope_range = b_range / a
    eff_range = 100 * np.exp(-3 * (slope_range - optimal_slope) ** 2)
    
    fig_eff = go.Figure()
    fig_eff.add_trace(go.Scatter(x=b_range, y=eff_range, mode='lines', line=dict(color='#636EFA', width=2.5), name='효율 곡선'))
    fig_eff.add_trace(go.Scatter(x=[b], y=[efficiency], mode='markers', marker=dict(size=12, color='red', symbol='circle'), name='현재 설정 위치'))
    
    fig_eff.update_layout(
        template="plotly_dark",
        height=240,
        xaxis=dict(title="공액축 상수 (b)"),
        yaxis=dict(title="수신 효율 (%)", range=[0, 105]),
        margin=dict(l=20, r=20, t=10, b=10),
        showlegend=False
    )
    st.plotly_chart(fig_eff, use_container_width=True)
    
    # 실시간 기하 데이터 메트릭
    st.markdown("### 📐 실시간 쌍곡선 기하 데이터")
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="🎯 계산된 초점 ($c$)", value=f"±{c:.3f}")
        st.metric(label="📈 점근선 기울기 ($b/a$)", value=f"{asymptote_slope:.2f}")
    with c2:
        st.metric(label="📏 주축 길이 ($2a$)", value=f"{2*a:.2f}")
        st.metric(label="🚀 현재 안테나 수신 효율", value=f"{efficiency:.1f} %")
        
    # 쌍곡선의 정의 확인 보드
    st.markdown("---")
    st.markdown("#### 📝 쌍곡선의 기하학적 정의 실시간 증명")
    px, py = x_orbit[-1], y_orbit[-1]
    dist_F1 = np.sqrt((px - c)**2 + py**2)
    dist_F2 = np.sqrt((px - (-c))**2 + py**2)
    diff = abs(dist_F2 - dist_F1)
    
    st.info(f"""
    **안테나 끝 점 $P({px:.2f}, {py:.2f})$에서 측정:**
    * $\\overline{{PF_2}}$ (가상초점까지 거리) = `{dist_F2:.4f}`
    * $\\overline{{PF_1}}$ (실제초점까지 거리) = `{dist_F1:.4f}`
    * **두 거리의 차 ($|\\overline{{PF_2}} - \\overline{{PF_1}}|$)** = **`{diff:.4f}`**
    
    👉 어떤 상수를 선택해도 거리의 차는 항상 주축의 길이 **$2a = {2*a:.2f}$** 와 완벽히 같습니다!
    """)
