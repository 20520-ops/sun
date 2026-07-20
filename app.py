import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="쌍곡선 안테나 시뮬레이터", page_icon="📡", layout="wide")

st.title("📡 고2 기하 심화탐구: 쌍곡선의 성질을 이용한 카세그레인 안테나 시뮬레이션")
st.write("교과서 개념인 **쌍곡선의 방정식 $\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1$**과 **빛의 반사 성질**을 결합한 웹앱입니다.")
st.markdown("---")

# 사이드바 제어판 (고2 수준의 문자만 사용)
with st.sidebar:
    st.header("📐 쌍곡선 거울면(안테나) 제어")
    a = st.slider("주축 상수 ($a$)", min_value=1.0, max_value=4.0, value=2.0, step=0.1,
                  help="원점에서 안테나 꼭짓점까지의 거리입니다. 값이 작을수록 안테나가 뾰족해집니다.")
    b = st.slider("공액축 상수 ($b$)", min_value=1.0, max_value=5.0, value=2.5, step=0.1,
                  help="점근선의 기울기(b/a)를 결정하여 안테나가 벌어지는 정도를 조절합니다.")
    y_max = st.slider("안테나 거울의 크기 ($y_{max}$)", min_value=2.0, max_value=6.0, value=4.0, step=0.2,
                      help="시뮬레이션할 쌍곡선 안테나판의 실제 위아래 크기입니다.")

# 2. 기하학 공식 계산 (c^2 = a^2 + b^2)
c = np.sqrt(a**2 + b**2)

# 두 초점 설정
F1_x, F1_y = c, 0   # 우측 초점 (실제 수신기 위치)
F2_x, F2_y = -c, 0  # 좌측 초점 (가상 초점 / 포물선 거울의 초점과 겹치는 곳)

# 3. 레이아웃 분할 (왼쪽: 안테나 시뮬레이션 그래프, 오른쪽: 수학적 증명 및 세특 해설)
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🔍 실시간 쌍곡선 전파 경로 시뮬레이션")
    st.caption("⚡ 주황색 전파선들은 원래 왼쪽 초점(F2)을 향해 달리다가, 초록색 쌍곡선 거울에 부딪혀 빨간색 진짜 초점(F1)으로 100% 모이게 됩니다.")
    
    fig = go.Figure()
    
    # ① 쌍곡선 안테나 거울면 그리기 (실제 안테나로 쓰는 우측 분기만 선명하게 표시)
    y_orbit = np.linspace(-y_max, y_max, 400)
    x_orbit = a * np.sqrt(1 + (y_orbit / b)**2)
    fig.add_trace(go.Scatter(x=x_orbit, y=y_orbit, mode='lines', line=dict(color='#00CC96', width=4), name='쌍곡선 안테나 거울면'))
    
    # 반대편 쌍곡선은 교과서 흐름상 연하게 점선으로 표시해둠
    x_orbit_left = -x_orbit
    fig.add_trace(go.Scatter(x=x_orbit_left, y=y_orbit, mode='lines', line=dict(color='rgba(255,255,255,0.15)', width=1.5, dash='dash'), name='반대편 쌍곡선(가상)'))
    
    # ② 점근선 그리기 (y = \pm (b/a)x)
    x_asymp = np.linspace(-c - 2, c + 3, 100)
    fig.add_trace(go.Scatter(x=x_asymp, y=(b/a)*x_asymp, mode='lines', line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dot'), name='점근선'))
    fig.add_trace(go.Scatter(x=x_asymp, y=-(b/a)*x_asymp, mode='lines', line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dot'), showlegend=False))
    
    # ③ 두 초점 F1, F2 표시
    fig.add_trace(go.Scatter(x=[c], y=[0], mode='markers+text', marker=dict(size=12, color='red', symbol='diamond'), name='진짜 초점 F1 (수신기)', text=['F1 (수신기)'], textposition='bottom center'))
    fig.add_trace(go.Scatter(x=[-c], y=[0], mode='markers+text', marker=dict(size=12, color='orange', symbol='diamond-open'), name='가상 초점 F2', text=['F2 (가상초점)'], textposition='bottom center'))
    
    # 🌟 킥포인트: 안테나 전파 레이트레이싱 (Ray Tracing) 생성 🌟
    # 안테나 표면에 부딪힐 5개의 전파 유입 지점 선정
    y_rays = np.linspace(-y_max * 0.8, y_max * 0.8, 5)
    x_rays = a * np.sqrt(1 + (y_rays / b)**2)
    
    for xr, yr in zip(x_rays, y_rays):
        # 가상 초점 F2(-c, 0)에서 안테나 표면(xr, yr)을 잇는 직선의 방향 벡터 계산
        dx = xr - (-c)
        dy = yr - 0
        
        # 외부 입사 전파 시작점 (거울면의 더 오른쪽 바깥에서 수렴하며 들어오는 경로 선명화)
        x_start = xr + dx * 0.3
        y_start = yr + dy * 0.3
        
        # 1) 들어오는 전파 (주반사경에서 반사되어 F2를 향해 좁혀져 들어오는 선)
        fig.add_trace(go.Scatter(x=[x_start, xr], y=[y_start, yr], mode='lines', line=dict(color='#636EFA', width=2), showlegend=False))
        
        # 2) 가상 연장선 (안테나 거울이 없었다면 가상초점 F2까지 그대로 갔을 점선 경로)
        fig.add_trace(go.Scatter(x=[xr, -c], y=[yr, 0], mode='lines', line=dict(color='rgba(255, 165, 0, 0.35)', width=1.5, dash='dash'), showlegend=False))
        
        # 3) 반사된 전파 (안테나 거울면에 부딪힌 후 실제 초점 F1으로 꺾여 모이는 꿀색 선)
        fig.add_trace(go.Scatter(x=[xr, c], y=[yr, 0], mode='lines', line=dict(color='gold', width=2), showlegend=False))

    # 좌표계 비율 1:1 고정
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
    st.subheader("📐 실시간 기하학적 분석 데이터")
    
    # 실시간 메트릭 창 생성
    st.metric(label="🎯 계산된 초점의 좌표 ($c$)", value=f"±{c:.3f}")
    st.metric(label="📏 주축의 길이 ($2a$)", value=f"{2*a:.2f}")
    st.metric(label="📈 점근선의 방정식", value=f"y = ±({b:.1f}/{a:.1f})x")
    
    st.markdown("---")
    st.subheader("📝 쌍곡선의 기하학적 정의 검증")
    st.write("안테나 맨 위쪽 끝 점 $P$를 기준으로 교과서 정의를 수치로 증명합니다.")
    
    # 안테나 최상단 점 P 좌표
    px, py = x_orbit[-1], y_orbit[-1]
    # 피타고라스 정리로 두 초점까지의 거리 계산
    dist_F1 = np.sqrt((px - c)**2 + py**2)
    dist_F2 = np.sqrt((px - (-c))**2 + py**2)
    diff = abs(dist_F2 - dist_F1)
    
    st.info(f"""
    **점 $P({px:.2f}, {py:.2f})$에서의 계산:**
    * $\\overline{{PF_2}}$ (가상초점까지 거리) = `{dist_F2:.4f}`
    * $\\overline{{PF_1}}$ (실제초점까지 거리) = `{dist_F1:.4f}`
    * **두 거리의 차 ($|\\overline{{PF_2}} - \\overline{{PF_1}}|$)** = **`{diff:.4f}`**
    
    👉 이 값은 설정한 **주축의 길이($2a = {2*a:.2f}$)**와 완벽하게 일치합니다!
    """)
    
    st.markdown("---")
    st.subheader("💡 카세그레인 안테나의 비밀")
    st.write("""
    교과서에서 배우는 **'쌍곡선 위의 한 점에서의 접선은 두 초점과 그 점이 이루는 각을 이등분한다'**는 성질 때문에 이런 안테나 공학이 가능해집니다.
    
    주축 $a$와 공액축 관련 상수 $b$ 슬라이더를 움직여보세요. 
    거울의 곡률이 아무리 찌그러지거나 펴져도, 들어오는 파란색 전파선들이 거울에 맞고 꺾일 때 **반드시 골드색 선을 따라 정확히 수신기($F_1$)로 모이는 것**을 시각적으로 확인할 수 있습니다.
    """)
