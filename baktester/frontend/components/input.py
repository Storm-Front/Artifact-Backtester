from dash import dcc, html
import dash_bootstrap_components as dbc

def create_button(button_id, button_text, button_class):
    return html.Div(
        [
            dbc.Button(
                button_text, id=button_id, className=button_class, 
            ),
            
        ]
    )


def generate_input_fields(strategy):
    form_elements = []
    for param, param_type in strategy.items():
        if param == 'name':
            continue
        if param_type == 'text':
            form_elements.append(dcc.Input(id=param, type='text', placeholder=f'input_{param}'))
        if param_type == 'dict':
            form_elements.append(dcc.Input(id=param, type='text', placeholder=f'input_{param}'))
        elif param_type == 'int':
            form_elements.append(dcc.Input(id=param, type='number', placeholder=f'input_{param}'))
        elif param_type == 'list':
            form_elements.append(dcc.Textarea(id=param, placeholder=f'input_{param}'))
    return form_elements



def create_select(id, options, default=None, multi=False):
    return dcc.Dropdown(
        id=id,
        options=options,
        value=default,
        multi=multi,
        style={'color': '#000000'}

    )
