import plotly.graph_objs as go
import pandas as pd

def plot_performance(equity_curve: pd.Series):
    """
    누적수익률 곡선 시각화 (plotly)
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=equity_curve.index, y=equity_curve.values, mode="lines", name="누적수익률"))
    fig.update_layout(title="누적수익률 곡선", xaxis_title="날짜", yaxis_title="자산")
    return fig

# TODO: 연별수익률, 드로우다운 등 추가 