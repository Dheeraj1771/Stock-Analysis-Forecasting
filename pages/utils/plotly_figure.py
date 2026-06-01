import plotly.graph_objects as go
import dateutil
import pandas_ta as pta
import datetime

def plotly_table(dataframe):
    # headerColor = 'grey'
    rowEvenColor = '#f8fafd'
    rowOddColor = '#e1efff'
    fig = go.Figure(data=[go.Table(
    header=dict(
        values=["<b><b>"]+["<b>"+str(i)[:10]+"<b>" for i in dataframe.columns],
        line_color='#0078ff', fill_color='#0078ff',
        align='center', font=dict(color='white', size=15),height=35,
    ),
    cells=dict(
        values=[["<b>"+str(i)+"<b>" for i in dataframe.index]]+[dataframe[i] for i in dataframe.columns], fill_color = [[rowOddColor,rowEvenColor]],
        align='left', line_color=['white'],font=dict(color=["black"], size=15)
    )
    )])
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
    return fig

def filter_data(dataframe, num_period):
    if(num_period=='5d'):
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-1)
    elif(num_period=='1mo'):
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
    elif(num_period=='6m0'):
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
    elif(num_period=='1y'):
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
    elif(num_period=='5y'):
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
    elif(num_period=='ytd'):
        date = datetime.datetime(dataframe.index[-1].year, 1, 1)
    else:
        date = dataframe.index[0]
    return dataframe.reset_index()[dataframe.reset_index()['Date']>date]

def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                             mode='lines', name='Open', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             mode='lines', name='Close', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                             mode='lines', name='High', line=dict(width=2, color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                             mode='lines', name='Low', line=dict(width=2, color='red')))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500, 
        margin=dict(l=0, r=20, t=20, b=0), 
        plot_bgcolor='white', 
        paper_bgcolor='#e1efff', 
        legend=dict(
            yanchor="top",
            y=1.0,        
            xanchor="right",
            x=1.0         
        )
    )
    return fig

def candlestick(dataframe, num_period):
    dataframe=filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=dataframe['Date'],
                                 open=dataframe['Open'], close=dataframe['Close'],
                                 high=dataframe['High'], low=dataframe['Low']))
    fig.update_layout(showlegend=False, height=500, margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor='white', paper_bgcolor='#e1efff' )
    return fig

def RSI(dataframe, num_period):
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['RSI'], marker_color='orange',
                            name='RSI', line=dict(width=2, color='orange')
    ))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[70]*len(dataframe), fill='tonexty',
                            name='Overbought', marker_color='red', line=dict(width=2, color='red', dash='dash')
    ))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[30]*len(dataframe), fill='tonexty',
                            name='Oversold', marker_color='#79da84', line=dict(width=2, color='#79da84', dash='dash')
    ))
    fig.update_layout(yaxis_range=[0, 100], height=200, margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor='white', paper_bgcolor='#e1efff', 
                      legend=dict(orientation='h',yanchor='top', y=1.02, xanchor='right', x=1
    ))
    return fig

def moving_average(dataframe, num_period):
    dataframe['SMA_50'] = pta.sma(dataframe['Close'], 50)
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                             mode='lines', name='Open', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             mode='lines', name='Close', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                             mode='lines', name='High', line=dict(width=2, color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                             mode='lines', name='Low', line=dict(width=2, color='red')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'],
                             mode='lines', name='SMA 50', line=dict(width=2, color='purple')))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500, 
        margin=dict(l=0, r=20, t=20, b=0), 
        plot_bgcolor='white', 
        paper_bgcolor='#e1efff', 
        legend=dict(
            yanchor="top",
            y=1.0,        
            xanchor="right",
            x=1.0         
        )
    )
    return fig
    
def MACD(dataframe, num_period):
    macd_df = pta.macd(dataframe['Close'])
    
    dataframe['MACD'] = macd_df.iloc[:, 0]
    dataframe['MACD Hist'] = macd_df.iloc[:, 1]
    dataframe['MACD Signal'] = macd_df.iloc[:, 2]

    dataframe = filter_data(dataframe, num_period)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], 
                             y=dataframe['MACD'],
                             name='MACD', 
                             marker_color='orange',
                             line=dict(width=2, color='orange')
    ))
    
    fig.add_trace(go.Scatter(x=dataframe['Date'], 
                             y=dataframe['MACD Signal'],
                             name='Signal', 
                             marker_color='red',
                             line=dict(width=2, color='red', dash='dash')
    ))
    c = ['red' if val < 0 else "green" for val in dataframe['MACD Hist']] 
    fig.add_trace(go.Bar(x=dataframe['Date'], y=dataframe['MACD Hist'],
                         name='Histogram', marker_color=c
    ))
    
    fig.update_layout(
        height=500, 
        margin=dict(l=0, r=0, t=0, b=0), 
        plot_bgcolor='white', 
        paper_bgcolor='#e1efff', 
        legend=dict(
            yanchor="top",
            y=1.0,        
            xanchor="right",
            x=1.0         
        )
    )
    return fig

def moving_average_forecast(forecast):
    fig = go.Figure()
    # Leave Last 30 Days
    fig.add_trace(go.Scatter(x=forecast.index[:-30],
                             y=forecast['Close'].iloc[:-30],
                             mode='lines',
                             name='Close Price',
                             line = dict(width=2, color='Black')
    ))
    # Last 30 Days
    fig.add_trace(go.Scatter(x=forecast.index[-31:],
                             y=forecast['Close'].iloc[-31:],
                             mode='lines',
                             name='Future Close Price',
                             line = dict(width=2, color='red')
    ))
    
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500, 
        margin=dict(l=0, r=20, t=20, b=0), 
        plot_bgcolor='white', 
        paper_bgcolor='#e1efff', 
        legend=dict(
            yanchor="top",           
            xanchor="left",
        )
    )
    return fig