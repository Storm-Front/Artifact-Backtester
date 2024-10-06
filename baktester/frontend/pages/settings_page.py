from dash import html, callback, Input, Output, dcc, no_update
from components.input import (
    create_select
)
import dash_bootstrap_components as dbc

def settings_page(cache):

    
    @callback(
            Output('select-strategy', 'value'),
            Output('select-strategy', 'options'),
            Output('store', 'data'),
            Input('select-strategy', 'value'))
    def update_selected_strategy(data):
        backtests=cache.get('executed_backtests')
        options=[]
        if not backtests:
            return no_update, no_update, {}
        for key in backtests.keys():
            options.append({'label':backtests[key]['strategy_name'] + key , 'value': key})
        if data==None:
            return cache.get('selected_strategy'), options, cache.get('selected_strategy')
        cache.set('selected_strategy', data)
        return cache.get('selected_strategy'), options, cache.get('selected_strategy')



    return html.Div(children=[
        create_select('select-strategy', {}),

    ])


