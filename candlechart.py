import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

def plot_candlestick(df,title,macd=False,rsi=False):
    data=df.copy()

    fig = make_subplots(rows=4, cols=1, shared_xaxes=True)



    fig.add_trace(go.Candlestick(
        x = data['basDt'],
        open=data['mkp'],
        high=data['hipr'],
        low=data['lopr'],
        close=data['clpr'],
        increasing=dict(line=dict(color='#ed2926'), fillcolor='#ed2926'),
                             decreasing=dict(line=dict(color='#2679ed'), fillcolor='#2679ed'),
        showlegend=False,
        name=""
    ),row=1,col=1)


    fig.update_layout(xaxis_rangeslider_visible=True, xaxis2_rangeslider_visible=False, xaxis3_rangeslider_visible=False,xaxis4_rangeslider_visible=False)
    fig.update_xaxes(rangeslider_thickness = 0.05)
    

    # 이동평균선
    data['MA5'] = data['clpr'].rolling(window=5).mean()
    data['MA20'] = data['clpr'].rolling(window=20).mean()
    data['MA60'] = data['clpr'].rolling(window=60).mean()
    fig.add_trace(go.Scatter(x=data['basDt'], y=data['MA5'], mode='lines', name='MA-5', line=dict(color='#9d11d0', width=0.7)),row=1,col=1)
    fig.add_trace(go.Scatter(x=data['basDt'], y=data['MA20'], mode='lines', name='MA-20', line=dict(color='#dcad04', width=0.7)),row=1,col=1)
    fig.add_trace(go.Scatter(x=data['basDt'], y=data['MA60'], mode='lines', name='MA-60', line=dict(color='#11d067', width=0.7)),row=1,col=1)

    # Volumne
    volume_colors = ['#ed2926' if data['clpr'].iloc[i]>= data['mkp'].iloc[i] else '#2679ed' for i in range(len(data['clpr']))]
    fig.add_trace(go.Bar(x=data['basDt'], y=data['trqu'], name='Volume', marker=dict(color=volume_colors,line=dict(width=0.1),opacity=0.7)), row=2, col=1)

    yaxis_title = None
    # MACD
    if (macd == True) & (rsi==False):
        fig.add_trace(go.Scatter(x=data['basDt'], y=data['MACD'], mode='lines', name='MACD',line=dict(color='#680a08',width=0.7)),
        row=3,col=1)
        fig.add_trace(go.Scatter(x=data['basDt'], y=data['MACD_signal'], mode='lines', name='Signal Line',line=dict(color='#a8693d',width=0.7)), 
        row=3, col=1)
        fig.add_trace(go.Bar(x=data['basDt'], y=data['MACD_oscillator'], name='MACD Oscillator', marker=dict(color='#e38c4f',line=dict(width=0.1))), 
        row=3, col=1)
        yaxis_title = {"axis_name": "yaxis3", "title": "MACD"}
    
    # RSI
    elif (macd == False) & (rsi==True):
        fig.add_trace(go.Scatter(x=data['basDt'], y=data['RSI'], mode='lines', name='RSI',line=dict(color='#d00f6e')),
        row=3,col=1)
        yaxis_title = {"axis_name": "yaxis3", "title": "RSI"}
    
    elif (macd == True) & (rsi==True):
        fig.add_trace(go.Scatter(x=data['basDt'], y=data['MACD'], mode='lines', name='MACD',line=dict(color='#680a08',width=0.7)),
        row=3,col=1)
        fig.add_trace(go.Scatter(x=data['basDt'], y=data['MACD_signal'], mode='lines', name='Signal Line',line=dict(color='#a8693d',width=0.7)), 
        row=3, col=1)
        fig.add_trace(go.Bar(x=data['basDt'], y=data['MACD_oscillator'], name='MACD Oscillator', marker=dict(color='#e38c4f',line=dict(width=0.1))), 
        row=3, col=1)

        fig.add_trace(go.Scatter(x=data['basDt'], y=data['RSI'], mode='lines', name='RSI',line=dict(color='#d00f6e')),
        row=4,col=1)
        yaxis_title = [{"axis_name": "yaxis3", "title": "MACD"},
            {"axis_name": "yaxis4", "title": "RSI"}]

    
    if yaxis_title:
        if isinstance(yaxis_title, list):
            for axis_info in yaxis_title:
                fig.update_layout(**{axis_info["axis_name"]: {"title": axis_info["title"]}})
        else:
            fig.update_layout(**{yaxis_title["axis_name"]: {"title": yaxis_title["title"]}})
    
    fig.update_layout(
        #title = '일별 주가',
        #title_font_family="맑은고딕",
        #title_font_size = 18,
        #title_pad=dict(b=5,t=5),
        hoverlabel=dict(
            bgcolor='black',
            font_size=15,
        ),
        hovermode="x unified", 
        template='plotly_dark',
        xaxis_tickangle=0,
        xaxis_showticklabels=True,
        xaxis_tickformat='%Y-%m-%d',
        yaxis_tickformat = ',',
        legend = dict(orientation = 'h', xanchor = "center", x = 0.75, y= 1), 
        barmode='group',
        yaxis=dict(domain=[0.5, 1.0], title = '주가'),          # 첫 번째 행의 y축
        yaxis2=dict(domain=[0.25, 0.40],title='거래량'),         # 두 번째 행의 y축
        yaxis3=dict(domain=[0.12, 0.22]),
        yaxis4=dict(domain=[0.0,0.1])
    )
        
    fig.update_layout(margin=go.layout.Margin(
            l=10, #left margin
            r=10, #right margin
            b=10, #bottom margin
            t=1  #top margin
        ),
        width=1000,height=700)
    num_points_to_display = 365  # 표시하려는 데이터 포인트 수
    if len(data)>=365:
        fig.update_xaxes(range=[data['basDt'].iloc[-num_points_to_display],data['basDt'].iloc[-1]])
    else :
        pass
    fig.update_yaxes(autorange=True)

    # fig.update_layout(yaxis_range=[min(data['lopr'].iloc[-num_points_to_display:]),max(data['hipr'].iloc[-num_points_to_display:])])

    fig.update_layout(yaxis_fixedrange=False)
    fig.update_layout()


    fig.update_layout(
    xaxis=dict(showticklabels=True),
    xaxis2=dict(showticklabels=False),
    xaxis3=dict(showticklabels=False),
    xaxis4=dict(showticklabels=False)
    )

    fig.update_xaxes(rangebreaks=[dict(bounds=["sat","mon"])]) ### 주말제거
    return fig