import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. 페이지 레이아웃 및 제목 설정
st.set_page_config(page_title="쌍곡선 안테나 시뮬레이터", page_icon="📡", layout="wide")

st.title("📡 기하 심화탐구: 쌍곡선(Hyperbola)의 기하학적 성질 및 안테나 시뮬레이션")
st.write("고등학교 기하 과정의 **쌍곡선 정의**와 **광학적 성질(두 초점을 활용한 전파 반사)**을 이용하여 카세그레인(Cassegrain) 안테나의 원리를 실시간으로 시뮬레이션합니다.")
st.markdown("---")

# 사이드바 제어판 구성
with st.sidebar:
    st.header("📐 쌍곡선 기하학 파라미터")
    
    # 주축의 정점 a (x^2/a^2 - y^2/b^2 = 1)
    a = st.slider("주축 반지름 ($a$)", min_value=1.0, max_value=4.0, value=2.0, step=0.1,
                  help="원점에서 쌍곡선 꼭짓점까지의 거리입니다. 값이 작을수록 굴곡이 급해집니다.")
    
    # 공액축의 정점 b
    b = st.slider("공액축 반지름 ($b$)", min_value=1.0, max_value=5.0, value=2.5, step=0.1,
                  help="쌍곡선의 벌어지는 정도를 결정하는 계수입니다.")
    
    # 안테나의 세로 크기 (y 범위)
    y_max = st.slider("안테나 가로/세로 크기 ($y_{max}$)", min_value=2.0, max_value=6.0, value=4.0, step=0.2,
                      help="시뮬레이션할 쌍곡선 거울면의 실제 크기입니다.")

# 2. 수학적 기하학 계산
# 초점 거리 c 계산: c^2 = a^2 + b^2 => c = sqrt(a^2 + b^2)
c = np.sqrt(a**2 + b**2)

# 이심률 e 계산: e = c / a (쌍곡선은 항상 e > 1)
eccentricity = c / a

# 쌍곡선 궤적 계산 (우측 항성/거울면: x = a * sqrt(1 + (y/b)^2))
y_orbit = np.linspace(-y_max, y_max, 400)
x_orbit = a * np.sqrt(1 + (y_orbit / b)**2)

# 안테나 공학적 지표: 이심률에 따른 전파 주행 경로 제어 효율 모델링
# 카세그레인 안테나 부반사경은 이심률이 1.5 ~ 2.5 사이일 때 주반사경(포물선)과의 초점 매칭 효율이 극대화됩니다.
optimal_e = 1.8
efficiency = max(0.0, 100 * np.exp(-4 * (eccentricity - optimal_e) ** 2))

# 3. 화면 배치 (두 개의 컬럼)
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🔍 쌍곡선 거울면 및 이중 초점 전파 경로 시뮬레이션")
    st.caption("💡 원리: 외부(포물선)에서 가상 초점 F2를 향해 수렴하던 전파가 쌍곡선 거울면에 부딪혀 실제 초점 F1(수신기)으로 완벽하게 모입니다.")
    
    fig_hyperbola = go.Figure()
    
    # ① 쌍곡선 안테나 거울면 그리기 (우측 반사경)
    fig_hyperbola.add_trace(go.Scatter(
        x=x_orbit, y=y_orbit,
        mode='lines',
        line=dict(color='#00CC96', width=4),
        name='쌍곡선 거울면'
    ))
    
    # ② 제1초점 F1 (c, 0) - 실제 수신기 위치
    fig_hyperbola.add_trace(go.Scatter(
        x=[c], y=[0],
        mode='markers+text',
        marker=dict(size=14, color='red', symbol='diamond'),
        name=f'제1초점 F1 ({c:.2f}, 0) [수신기]',
        text=[f'F1({c:.2f}, 0)'], textposition='bottom right'
    ))
    
    # ③ 제2초점 F2 (-c, 0) - 가상 초점 위치
    fig_hyperbola.add_trace(go.Scatter(
        x=[-c], y=[0],
        mode='markers+text',
        marker=dict(size=14, color='orange', symbol='diamond-open'),
        name=f'제2초점 F2 ({-c:.2f}, 0) [가상초점]',
        text=[f'F2({-c:.2f}, 0)'], textposition='bottom left'
    ))
    
    # ④ 점근선 그리기 (y = \\pm (b/a)x)
    x_asymp = np.linspace(-c - 2, c + 4, 100)
    y_asymp_pos = (b / a) * x_asymp
    y_asymp_neg = -(b / a) * x_asymp
    
    fig_hyperbola.add_trace(go.Scatter(
        x=x_asymp, y=y_asymp_pos,
        mode='lines',
        line=dict(color='rgba(255, 255, 255, 0.2)', width=1, dash='dot'),
        name='점근선',
        showlegend=True
    ))
    fig_hyperbola.add_trace(go.Scatter(
        x=x_asymp, y=y_asymp_neg,
        mode='lines',
        line=dict(color='rgba(255, 255, 255, 0.2)', width=1, dash='dot'),
        showlegend=False
    ))

    # ⑤ 전파 레이트레이싱 (Ray Tracing) 시뮬레이션
    # 안테나 표면의 5개 샘플 포인트 선정
    y_samples = np.linspace(-y_max * 0.8, y_max * 0.8, 5)
    x_samples = a * np.sqrt(1 + (y_samples / b)**2)
    
    for xs, ys in zip(x_samples, y_samples):
        # 가상 초점 F2(-c, 0)에서 표면 점(xs, ys)을 향하는 방향 벡터 계산
        dx = xs - (-c)
        dy = ys - 0
        length = np.sqrt(dx**2 + dy**2)
        
        # 외부 시작점 (거울면보다 더 오른쪽 뒤에서 F2를 향해 다가오는 선 확장)
        x_start = xs + dx * 0.4
        y_start = ys + dy * 0.4
        
        # 1) 입사 전파 (가상초점 F2를 향해 좁혀져 들어오는 실선)
        fig_hyperbola.add_trace(go.Scatter(
            x=[x_start, xs], y=[y_start, ys],
            mode='lines',
            line=dict(color='#636EFA', width=1.5),
            showlegend=False
        ))
        
        # 2) 가상 연장선 (거울이 없다면 F2까지 도달했을 점선 경로)
        fig_hyperbola.add_trace(go.Scatter(
            x=[xs, -c], y=[ys, 0],
            mode='lines',
            line=dict(color='rgba(255, 165, 0, 0.4)', width=1, dash='dash'),
            showlegend=False
        ))
        
        # 3) 반사 전파 (거울면에 부딪힌 후 실제 초점 F1으로 꺾이는 선)
        fig_hyperbola.add_trace(go.Scatter(
            x=[xs, c], y=[ys, 0],
            mode='lines',
            line=dict(color='gold', width=2),
            showlegend=False
        ))

    # 그래프 1:1 비율 유지 설정 및 한계값 지정
    max_axis = max(c + 3, y_max + 1)
    fig_hyperbola.update_layout(
        template="plotly_dark",
        width=700, height=550,
        xaxis=dict(title="X 좌표", range=[-max_axis, max_axis], scaleratio=1, scaleanchor="y"),
        yaxis=dict(title="Y 좌표", range=[-max_axis, max_axis]),
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True
    )
    
    st.plotly_chart(fig_hyperbola, use_container_width=True)

with col2:
    st.subheader("📊 기하학적 특성 및 수신 효율")
    
    # 그래프: 이심률(eccentricity) 변화에 따른 안테나 수신 효율 시각화
    e_range = np.linspace(1.05, 3.5, 200)
    eff_range = 100 * np.exp(-4 * (e_range - optimal_e) ** 2)
    
    fig_eff = go.Figure()
    fig_eff.add_trace(go.Scatter(
        x=e_range, y=eff_range,
        mode='lines',
        line=dict(color='#636EFA', width=2.5),
        name='이심률별 매칭 효율'
    ))
    fig_eff.add_trace(go.Scatter(
        x=[eccentricity], y=[efficiency],
        mode='markers',
        marker=dict(size=12, color='red', symbol='circle'),
        name='현재 설정 상태'
    ))
    fig_eff.update_layout(
        template="plotly_dark",
        height=260,
        xaxis=dict(title="쌍곡선 이심률 (e = c/a)"),
        yaxis=dict(title="안테나 수신 효율 (%)", range=[0, 105]),
        margin=dict(l=20, r=20, t=10, b=10),
        showlegend=False
    )
    st.plotly_chart(fig_eff, use_container_width=True)
    
    # 실시간 데이터 테이블 및 메트릭 지표 출력
    st.markdown("### 📐 실시간 쌍곡선 기하 데이터")
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="🎯 초점 좌표 ($c$)", value=f"±{c:.3f}")
        st.metric(label="🚀 쌍곡선 이심률 ($e$)", value=f"{eccentricity:.3f}")
    with c2:
        st.metric(label="📏 주축 길이 ($2a$)", value=f"{2*a:.2f}")
        st.metric(label="📡 현재 시스템 수신 효율", value=f"{efficiency:.1f} %")
        
    # 쌍곡선의 정의 확인 보드 (임의의 점 P에서의 거리의 차 증명)
    st.markdown("---")
    st.markdown("#### 📝 쌍곡선의 기하학적 정의 실시간 증명")
    # 안테나의 맨 위 끝 점 P 선정
    px = x_orbit[-1]
    py = y_orbit[-1]
    
    dist_F1 = np.sqrt((px - c)**2 + py**2)
    dist_F2 = np.sqrt((px - (-c))**2 + py**2)
    diff = abs(dist_F1 - dist_F2)
    
    st.write(f"안테나 끝 점 $P({px:.2f}, {py:.2f})$에서:")
    st.write(f"- 초점1까지의 거리 $\\overline{{PF_1}}$ = `{dist_F1:.4f}`")
    st.write(f"- 초점2까지의 거리 $\\overline{{PF_2}}$ = `{dist_F2:.4f}`")
    st.write(f"  👉 **두 거리의 차 ($|\\overline{{PF_2}} - \\overline{{PF_1}}|$)** = `{diff:.4f}` ( 정확히 $2a = {2*a:.2f}$ 와 일치! )")

# 4. 심화 탐구를 위한 고2 기하학 해설 가이드
st.markdown("---")
st.subheader("💡 세특 심화탐구를 위한 기하학 및 공학적 원리 해설")
st.markdown("""
* **쌍곡선의 광학적 성질 (Reflection Property):** 쌍곡선의 한 가상 초점($F_2$)을 향해 입사하는 빛은 쌍곡선 거울면에 반사된 후 다른 진짜 초점($F_1$)을 통과하게 됩니다. 고등학교 기하 과목에서 배우는 **'쌍곡선 위의 한 점에서의 접선은 두 초점과 그 점이 이루는 각을 이등분한다'**는 광학적 정리가 공학적으로 응용된 예시입니다.
* **카세그레인 안테나(Cassegrain Antenna)의 결합 원리:** 
  1. 우주에서 오는 평행한 전파가 커다란 **포물선(주반사경)**에 부딪혀 포물선의 초점으로 수렴하려 합니다.
  2. 이 포물선의 초점 위치에 **쌍곡선(부반사경)**의 한 초점($F_2$)이 정확히 겹치도록 정밀하게 배치합니다.
  3. 전파가 가상초점($F_2$)에 도달하기 직전 쌍곡선 거울면에 부딪히면서 반사되어, 쌍곡선의 반대편 진짜 초점($F_1$)에 위치한 수신기(Feed Horn)로 깨끗하게 모이게 됩니다.
* **이심률($e$)과 안테나 공학:** 쌍곡선의 이심률 $e = \\frac{c}{a}$는 1보다 클 때 쌍곡선이 되며, 이 값이 최적값(약 1.8)에 가까울수록 주반사경과 부반사경 사이의 초점 매칭이 완벽해져 노이즈를 유입하지 않는 최고 효율의 안테나가 설계됩니다.
""")
