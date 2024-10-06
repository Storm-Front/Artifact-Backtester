from dash_app_template.app import DashApp
from artifact_backtester_client.backtester_client import BacktesterClient
from pages.start_backtest import start_backtest_page
from pages.overview_page import overview_page
from dash_app_template.cache.flask_cache import FlaskCache
import custom_template
import plotly.io as pio
from pages.settings_page import settings_page
from pages.portfolio_page import portfolio_page
from pages.summary_page import summary_page
from pages.strategy_page import strategy_page

pio.templates.default = "darkly"

client=BacktesterClient(
    'https://0.0.0.0:7000',
    'Simone', 
    'password',
    False
)

app= DashApp('TestApp')
app.register_caching_strategy(FlaskCache(app.server))
cache = app.cache

client.login()
cache.set('strategies',client.get_strategies()['strategies'])
cache.set('executed_backtests', {})


configuration=start_backtest_page(cache, client)

app.register_page(configuration, '/','configuration')

overview=overview_page(cache)
app.register_page(overview, '/overview','overview')

settings=settings_page(cache)
app.register_page(settings, '/settings','settings')

operations=portfolio_page(cache)
app.register_page(operations, '/portfolio','portfolio')

summary=summary_page(cache)
app.register_page(summary, '/summary','summary')

strategy=strategy_page(cache)
app.register_page(strategy, '/strategy','strategy')

app.run(jupyter_mode='external', port=8078)