import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="고2 기하 쌍곡선 시뮬레이터", page_icon="📐", layout="wide")

st.title("📐 고2 기하 심화탐구: 쌍곡선의 정의와 빛의 반사 성질")
st.write("교과서에서 배우는 **쌍곡선의 방정식 $\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1$**의 기하학적 성질을 실시간으로 확인합니다.")
st.markdown("---")

# 사이드바 제어판 (교과서에 나오는 문자만 사용!)
with st.sidebar:
    st.header("🔍 쌍곡선 상수 조절")
    a = st.slider("주축 상수 ($a$)", min_value=1.0, max_value=4.0, value=2.0, step=0.1,
                  help="원점에서 꼭짓점까지의 거리입니다. 주축의 길이는 2a가 됩니다.")
    b = st.slider("공액축 관련 상수 ($b$)", min_value=1.0, max_value=5.0, value=2.0, step=0.1,
                  help="점근선의 기울기(b/a)를 결정하는 상수입니다.")
    
    st.markdown("---")
    st.header("📍 쌍곡선 위의 점 P 제어")
    # 쌍곡선 위의 점 P를 움직여보는 슬라이더
    y_p = st.slider("점 P의 Y좌표 선택", min_value=-4.0, max_value=4.0, value=1.5, step=0.1)

# 2. 고2 교육과정 수학 계산
# 초점 c 계산 공식: c^2 = a^2 + b^2
c = np.sqrt(a**2 + b**2)

# 선택한 y_p에 따른 점 P의 X좌표 계산 (우측 쌍곡선: x = a * sqrt(1 + y^2/b^2))
x_p = a * np.sqrt(1 + (y_p / b)**2)

# 두 초점 좌표
F1_x, F1_y = c, 0   # 오른쪽 초점
F2_x, F2_y = -c, 0  # 왼쪽 초점

# 점 P에서 두 초점까지의 실제 거리 계산 (피타고라스 정리)
PF1 = np.sqrt((x_p - F1_x)**2 + (y_p - F1_y)**2)
PF2 = np.sqrt((x_p - F2_x)**2 + (y_p - F2_y)**2)
distance_diff = abs(PF2 - PF1) # 두 거리의 차

# 3. 화면 배치 (좌측: 그래프, 우측: 교과서 정의 증명 및 설명)
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📊 쌍곡선 기하학적 시각화")
    
    # 쌍곡선 그래프 그리기 위한 데이터 계산
    y_vals = np.linspace(-5, 5, 400)
    x_vals_right = a * np.sqrt(1 + (y_vals / b)**2)
    x_vals_left = -x_vals_right
    
    fig = go.Figure()
    
    # ① 우측 쌍곡선 (안테나 거울면 역할)
    fig.add_trace(go.Scatter(x=x_vals_right, y=y_vals, mode='lines', line=dict(color='#00CC96', width=3), name='쌍곡선 (우)'))
    # ② 좌측 쌍곡선 (반대편 쌍곡선)
    fig.add_trace(go.Scatter(x=x_vals_left, y=y_vals, mode='lines', line=dict(color='rgba(0,204,150,0.2)', width=1.5), name='쌍곡선 (좌)'))
    
    # ③ 점근선 그리기 (y = \pm (b/a)x)
    x_asymp = np.linspace(-7, 7, 100)
    fig.add_trace(go.Scatter(x=x_asymp, y=(b/a)*x_asymp, mode='lines', line=dict(color='gray', width=1, dash='dot'), name='점근선 ($y=\\frac{b}{a}x$)'))
    fig.add_trace(go.Scatter(x=x_asymp, y=-(b/a)*x_asymp, mode='lines', line=dict(color='gray', width=1, dash='dot'), showlegend=False))
    
    # ④ 두 초점 F1, F2 표시
    fig.add_trace(go.Scatter(x=[c], y=[0], mode='markers+text', marker=dict(size=12, color='red'), name=f'초점 F1({c:.2f}, 0)', text=['F1'], textposition='bottom right'))
    fig.add_trace(go.Scatter(x=[-c], y=[0], mode='markers+text', marker=dict(size=12, color='orange'), name=f'초점 F2({-c:.2f}, 0)', text=['F2'], textposition='bottom left'))
    
    # ⑤ 사용자가 선택한 점 P 표시
    fig.add_trace(go.Scatter(x=[x_p], y=[y_p], mode='markers+text', marker=dict(size=14, color='yellow', symbol='circle'), name=f'선택한 점 P({x_p:.2f}, {y_p:.2f})', text=['P'], textposition='top center'))
    
    # ⑥ 점 P에서 두 초점까지 선 잇기
    fig.add_trace(go.Scatter(x=[x_p, F1_x], y=[y_p, F1_y], mode='lines', line=dict(color='red', width=2), name='선분 PF1'))
    fig.add_trace(go.Scatter(x=[x_p, F2_x], y=[y_p, F2_y], mode='lines', line=dict(color='orange', width=2), name='선분 PF2'))

    # 기하학적 왜곡 방지 (1:1 비율)
    fig.update_layout(
        template="plotly_dark",
        width=700, height=600,
        xaxis=dict(title="X축", range=[-7, 7], scaleratio=1, scaleanchor="y"),
        yaxis=dict(title="Y축", range=[-6, 6]),
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📝 쌍곡선의 정의 실시간 증명 판")
    st.write("교과서 정의: **쌍곡선 위의 임의의 점에서 두 초점에 이르는 거리의 차는 주축의 길이($2a$)로 일정하다.**")
    
    # 실시간 수치 보여주기
    st.info(f"""
    **현재 위치에서의 계산 결과:**
    * 선분 $\\overline{{PF_2}}$ (긴 거리) = `{PF2:.4f}`
    * 선분 $\\overline{{PF_1}}$ (짧은 거리) = `{PF1:.4f}`
    * **두 거리의 차 ($|\\overline{{PF_2}} - \\overline{{PF_1}}|$)** = **`{distance_diff:.4f}`**
    """)
    
    # 주축의 길이 계산 출력
    st.success(f"현재 설정된 **주축의 길이 ($2a$)** = {2*a:.1f}")
    st.caption("💡 왼쪽 사이드바에서 점 P의 위치나 상수를 바꿔보세요! 거리의 차가 항상 주축의 길이와 똑같이 유지되는 마법을 볼 수 있습니다.")
    
    st.markdown("---")
    st.subheader("📡 안테나에 쓰이는 기하학적 원리")
    st.write("""
    **"한 초점을 향해 달리는 빛은 쌍곡선에 부딪히면 다른 초점으로 모인다"**
    
    교과서에는 안 나오지만, 쌍곡선은 독특한 **빛의 반사 성질**이 있습니다.
    
    1. 왼쪽 그림에서 주황색 선($\\overline{{PF_2}}$) 방향을 따라서 외부에서 전파가 들어온다고 상상해 보세요. 이 전파는 원래 **왼쪽 초점 $F_2$**를 향해 가고 있었습니다.
    2. 하지만 $F_2$에 도달하기 전, 초록색 **쌍곡선 거울(안테나)**에 부딪힙니다.
    3. 반사된 전파는 신기하게도 방향이 꺾여서 **오른쪽 진짜 초점 $F_1$**으로 전부 모이게 됩니다.
    
    이 성질을 이용해 우주 기지국이나 천체 망원경에서는 큰 포물선 거울과 작은 쌍곡선 거울을 겹쳐서 전파를 한곳으로 모으는 **카세그레인 안테나**를 만듭니다.
    """)
    
    st.markdown("---")
    st.markdown("### 📐 단원 관련 핵심 공식 요약")
    st.latex(r"c = \sqrt{a^2 + b^2}")
    st.latex(r"\text{점근선의 방정식: } y = \pm \frac{b}{a}x")
