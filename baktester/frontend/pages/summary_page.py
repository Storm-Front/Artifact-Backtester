from dash import html, callback, Input, Output, dcc, no_update, dash_table
from components.input import (
    create_select
)
import dash_bootstrap_components as dbc
import pandas as pd

def summary_page(cache):
    @callback(
        Output('stats-summary', 'children'),
        Input('store', 'data'))
    def update_selected_strategy(strat_id):
        if strat_id is None:
            return no_update

        base_stats = cache.get(f'base_stats_{strat_id}')
        

        '''assolutamente indecente. È solo per testare e mostrare i valori di base_stats'''
        table_rows = []
        for stat_name, stat_values in base_stats.items():
            if stat_name in ["initial_capital", "ending_capital"]:
                if isinstance(stat_values, list) and len(stat_values) > 0:
                    first_value = stat_values[0]  
                    if isinstance(first_value, list) and len(first_value) > 0:
                        result_value = first_value[-1]
                    else:
                        result_value = None  
                else:
                    result_value = None  
            else:
                result_value = stat_values[0] if stat_values else None

            table_rows.append(html.Tr([html.Td(stat_name), html.Td(result_value)]))

        table = dbc.Table([
            html.Thead(html.Tr([html.Th("Statistic Name"), html.Th("Value")])),
            html.Tbody(table_rows)
        ], bordered=True, striped=True, hover=True)

        return table




    return html.Div(children=[

        html.Div(id='stats-summary'),

    ])


