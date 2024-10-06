from dash import html, callback, Input, Output, dcc, no_update, dash_table
from components.input import (
    create_select
)
import dash_bootstrap_components as dbc
import pandas as pd

def portfolio_page(cache):

    @callback(
            Output('select-broker', 'options'),
            Input('store', 'data'))
    def update_selected_strategy(strat_id):
        if strat_id==None:
            return no_update
        brokers_list=cache.get(f'base_stats_{strat_id}')['brokers_list'][-1]
        brokers_list=[{'label': broker, 'value': broker} for broker in brokers_list]
        return brokers_list



    @callback(
            Output('portfolio-history', 'children'),
            Output('broker-total', 'children'),
            Input('select-broker', 'value'),
            Input('store', 'data'))
    def update_portfolio_table(broker, strat_id):
        if broker is None:
            return no_update
        if not cache.get(f'cached_broker_table_{strat_id}'):    
            create_table_per_broker(cache, strat_id)

        df_portfolio_history = cache.get(f'cached_broker_table_{strat_id}')[broker]
        total_profit_loss = df_portfolio_history['Profit/Loss'].sum().round(3)
        return dbc.Table.from_dataframe(df_portfolio_history, striped=True, bordered=True, hover=True), f'the total is: {total_profit_loss}'


    '''  page layout'''
    return html.Div(children=[
        create_select('select-broker', {},True),
        html.Br(),
        html.Div(id='portfolio-history'),
        dbc.Card(id='broker-total',children=[]),
    ])






def create_table_per_broker(cache, strat_id):
    brokers_list = cache.get(f'base_stats_{strat_id}')['brokers_list'][-1]
    cached_table ={}
    for broker in brokers_list:
        df_portfolio_history = pd.DataFrame()

        stats = cache.get(f'{broker}_{strat_id}')
        boker_history = pd.DataFrame(
            stats['portfolio_history'],
            columns=['Quantity', 'Cost', 'Position', 'Asset', 'Currency', 'Broker', 'Entry Price', 'Entry Time', 'Fees', 'Cash After', 'Exit Price', 'Exit Time']
        )
        boker_history['Profit/Loss'] = ((boker_history['Exit Price'] - boker_history['Entry Price']) * boker_history['Quantity']).round(3)

        df_portfolio_history = pd.concat([df_portfolio_history, boker_history])
        cached_table[broker] = df_portfolio_history


    cache.set(f'cached_broker_table_{strat_id}', cached_table)