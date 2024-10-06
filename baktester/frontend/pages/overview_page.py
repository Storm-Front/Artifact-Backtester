from dash import html, callback, Input, Output, dcc, no_update, ctx
import plotly.express as px
from components.input import (
    create_select
)
import pandas as pd
import plotly.graph_objects as go
from components.graph import (
    line_plot,
    create_card
)
import math 


def overview_page(cache):


    ''' update the main graph with capital and drawdown '''
    @callback(
        Output('backtest-graph', 'figure'),
        Input('store', 'data')
    )
    def update_graphs(data):
        if data==None:
            return no_update
        base_stats=cache.get(f'base_stats_{data}')


        ending_capital=base_stats['ending_capital']
        drawdown=base_stats['drawdown']
        df_c = pd.DataFrame(ending_capital, columns=['timestamp', 'value'])
        df_c['timestamp'] = pd.to_datetime(df_c['timestamp'], unit='ms')

        df_d = pd.DataFrame(drawdown)
        df_d['timestamp'] = df_c['timestamp']
        df_d['value'] = drawdown
        fig_c=line_plot(df_c['timestamp'],df_c['value'], 'lines+markers', 'capital', color_='yellow')
        fig_d=line_plot(df_d['timestamp'],df_d['value'], 'lines+markers', 'drawdown', yaxis_='y2', color_='green')


        fig = go.Figure()
        fig.add_trace(fig_c)
        fig.add_trace(fig_d)

        fig.update_layout(
            title='Portfolio Value and Drawdown',
            xaxis_title='Date',
            yaxis_title='Portfolio Value',
            yaxis=dict(
                title='Portfolio Value',
                titlefont=dict(color='yellow'),
                tickfont=dict(color='yellow')
            ),
            yaxis2=dict(
                title='Drawdown',
                titlefont=dict(color='green'),
                tickfont=dict(color='green'),
                overlaying='y',
                side='right',
            ),
            xaxis_rangeslider_visible=False  
        )


        return fig

    ''' update cards ( most important stats ) '''

    @callback(
        Output('card1', 'children'),
        Output('card2', 'children'),
        Output('card3', 'children'),
        Output('card4', 'children'),
        Output('card5', 'children'),
        Output('card6', 'children'),
        Input('store', 'data')
    )
    def update_cards(data):

        if data==None:
            return no_update, no_update, no_update, no_update, no_update, no_update
        base_stats=cache.get(f'base_stats_{data}')
        total_profit=math.trunc(base_stats['total_profit'][0]*1000)/1000

        sharpe_ratio=math.trunc(base_stats['sharpe_ratio'][0]*1000)/1000
        max_drawdown=math.trunc(base_stats['max_drawdown'][0]* 1000)/1000
        percentage_of_time_in_market=math.trunc(base_stats['percentage_of_time_in_market'][0] * 1000)/1000
        winrate=math.trunc(base_stats['winrate'][0] * 1000)/1000
        total_number_of_trades=math.trunc(base_stats['total_number_of_trades'][0] * 1000)/1000


        return total_profit, sharpe_ratio, max_drawdown, percentage_of_time_in_market, winrate, total_number_of_trades



    ''' update general info (strategy description and parameters) '''
    @callback(
        Output('strategy-general-info', 'children'),
        Input('store', 'data')
    )
    def update_general_info(data):
        if data==None:
            return no_update

        backtests=cache.get('executed_backtests')
        strategy_name=backtests[data]['strategy_name']

        strategy_params=backtests[data]
        strategy_params_str=""
        for key in strategy_params.keys():
            strategy_params_str+=f"{key}: {strategy_params[key]} \n"
        return html.Div([
            html.H3(f'Strategy: {strategy_name}'),
            html.P(f' {strategy_params_str}')
        ])
    


    ''' page layout '''
    
    return html.Div([
        dcc.Store(id='graph-range-filter', storage_type='local'),
        dcc.Store(id='graph-single-filter', storage_type='local'),
        html.Div(id='strategy-general-info'),

        html.Br(),


        html.Div(className="row", children=[
            html.Div(className="col-md-4", children=create_card('card1', 'NetProfit', "")),
            html.Div(className="col-md-4", children=create_card('card2', 'Sharpe Ratio', "")),
            html.Div(className="col-md-4", children=create_card('card3', 'Max Drawdown', ""))
        ]),
        
        html.Br(),

        dcc.Graph(
        id='backtest-graph' ),

        html.Br(),

        html.Div(className="row", children=[
            html.Div(className="col-md-4", children=create_card('card4', '% time in market', "")),
            html.Div(className="col-md-4", children=create_card('card5', 'Winrate', "")),
            html.Div(className="col-md-4", children=create_card('card6', 'Total Trade', ""))
        ]),


    ]
        )



    ''' update the graph filter with the range selected by the user '''

    @callback(
        Output('graph-range-filter', 'data'),
        Input('backtest-graph', 'relayoutData'))
    def update_graph_filter(relayoutData):
        if relayoutData is None:
            return no_update
        return relayoutData
    
    ''' update the graph filter with the single point selected by the user '''
    @callback(
        Output('graph-single-filter', 'data'),
        Input('backtest-graph', 'clickData'))
    def update_graph_filter(clickData):
        if clickData is None:
            return no_update
        return clickData
