from dash import html, callback, Input, Output, dcc,State
import dash_bootstrap_components as dbc
from components.input import (
    create_button,
    generate_input_fields,
    create_select
)
import json
import uuid



def start_backtest_page(cache, client):
    strategies_params= {strategy['name']: strategy for strategy in cache.get('strategies')}
    options={strategy: strategy for strategy in strategies_params.keys()}
    strategies_selector= create_select('strategies_selector', options)


    ''' update strategy params inputs '''
    @callback(
    Output('strategy_params', 'children'),
    Input('strategies_selector', 'value')
    )
    def update_params(strategy_name):
        if not strategy_name:
            return []
        strategy = strategies_params[strategy_name]
        fields= generate_input_fields(strategy)

        return fields
    



    ''' start backtest  '''
    @callback(
        Output('response-output', 'children'),
        Input("start_backtest_button", "n_clicks"),
        State("strategy_params", "children"),
        State("input_start_date", "value"),
        State("input_end_date", "value"),
        State("input_ohlcv_data_pool", "value"),
        State("input_brokers_confing", "value"),
        State("strategies_selector", "value")
    )
    def start_backtest(n_clicks, form_elements, start_date, end_date, ohlcv_data_pool, brokers_confing, strategy_name):

        if n_clicks is None:
            return ""
        
        strategy_params = {}


        '''FUNCTION TO CAST VALUES FOR STRATEGY PARAMS DURING TESTING'''
        response = client.start_backtest(
            start_date=1715179200000,
            end_date=1716580500000,
            strategy_name="sma_test",
            ohlcv_data_pool={"Yf_Api": {"300000": ["artifact.amzn"]}},
            strategy_params={
                "start_date": 1715179200000,
                "end_date": 1716580500000,
                "long_window": 200,
                "short_window": 50,
                "ohlcv_5m": {"Yf_Api": ["artifact.amzn"]},
                "brokers_list": ["BrokerSandBox"]
            },
            brokers_config={"BrokerSandBox": {"available_cash": 10000}}
        )


        # for elem in form_elements: 
        #     prop=elem['props']
        #     strategy_params[prop['id']]=prop['value']

        # response = client.start_backtest(
        #     start_date=start_date, 
        #     end_date= end_date, 
        #     strategy_name= strategy_name,
        #     ohlcv_data_pool=json.loads(ohlcv_data_pool), 
        #     strategy_params= strategy_params,
        #     brokers_config= json.loads(brokers_confing) 
        #     )

        if response['status'] == 200:
            strategy_stats = client.get_strategy_stats()
            id_ = str(uuid.uuid4())
            cache_backtest_results(cache, strategy_stats, id_)
            cache_brokers_results(cache, id_, client)
            backtests=cache.get('executed_backtests')

            backtests[id_]={
                'start_date': start_date,
                'end_date': end_date,
                'strategy_name': strategy_name,
                'ohlcv_data_pool': ohlcv_data_pool,
                'strategy_params': strategy_params,
                'brokers_config': brokers_confing
            }
            cache.set('executed_backtests', backtests)
            cache.set('selected_strategy', id_)
            response_content = html.Div([html.P(f"Response: {response}")])
        else:
            response_content = html.Div([html.P(f"Error: {response}")])
        
        return response_content
                        
                                                  


    return html.Div(
        [
            html.H1('Backtester'),
            strategies_selector,
            html.Br(),
            html.Div('Backtest settings:'),
            dbc.Stack(
                [
                dcc.Input(id=f'input_start_date', type='number', placeholder='start_date'),
                dcc.Input(id=f'input_end_date', type='number', placeholder='end_date'),
                dcc.Input(id=f'input_ohlcv_data_pool', type='text', placeholder='ohlcv_data_pool'),
                dcc.Input(id=f'input_brokers_confing', type='text', placeholder='brokers_confing'),
                ] , gap=2),
        
            html.Hr(),
            dbc.Stack(id="strategy_params", gap=2),
                create_button('start_backtest_button', 'Start backtest', 'primary'),
                html.Div(id='response-output')
            ]
    )


               
''' function to cast input values to the correct type for the request'''
def cast_values(type_dict, value_dict):
    casted_dict = {}
    for key, value_type in type_dict.items():
        if key in value_dict:
            if value_type == 'int':
                casted_dict[key] = int(value_dict[key])
            elif value_type == 'float':
                casted_dict[key] = float(value_dict[key])
            elif value_type == 'str':
                casted_dict[key] = str(value_dict[key])
            elif value_type == 'dict':
                casted_dict[key] = json.loads(value_dict[key])
            elif value_type == 'list':
                casted_dict[key] = json.loads(value_dict[key])
            else:
                casted_dict[key] = value_dict[key]
    return casted_dict


def cache_brokers_results(cache, id, client):
    broker_list=cache.get('base_stats_{}'.format(id))['brokers_list'][-1]

    for broker in broker_list:
        broker_stats=client.get_broker_stats(broker)['stats'][0]['snapshot']
        cache.set(f'{broker}_{id}', broker_stats)





'''Function that formats the snaphots into a better format for use and caches them'''

#TO BE REVIEWED
def cache_backtest_results(cache, snapshots, id_):
    formatted_snapshots = {}

    for snapshot in snapshots['stats']:
        snap = snapshot['snapshot']
        for key, value in snap.items():
            formatted_key = f"{key}_{id_}"

            if formatted_key not in formatted_snapshots:
                formatted_snapshots[formatted_key] = {} if isinstance(value, dict) else []

            if isinstance(value, dict):
                def merge_dicts(target_dict, source_dict):
                    for k, v in source_dict.items():
                        if isinstance(v, dict):
                            if k not in target_dict:
                                target_dict[k] = {}
                            merge_dicts(target_dict[k], v)
                        else:
                            if k not in target_dict:
                                target_dict[k] = []
                            target_dict[k].append(v)

                merge_dicts(formatted_snapshots[formatted_key], value)
            else:
                formatted_snapshots[formatted_key].append(value)

    for key, value in formatted_snapshots.items():
        cache.set(key, value)










