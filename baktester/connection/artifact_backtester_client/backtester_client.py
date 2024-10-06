import requests
import logging


class BacktesterClient:
    def __init__(self, base_url, username,password, safe_mode=False):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.safe_mode = safe_mode
        self.token = None
    
    def login(self):
        
        data = {'username': self.username, 'password': self.password}

        response = requests.post(self.base_url + '/token', data=data,verify=self.safe_mode)
        if response.status_code == 200:
            self.token = response.json()['access_token']
            return True
        
        return False

    def get_headers(self):
        return {'Authorization': 'Bearer ' + self.token}

    '''
    -------------------------------------------------
    |               SNAPSHOT REQUEST                |
    -------------------------------------------------
    '''



    def get_strategy_stats(self):
        
        response = requests.get(
            self.base_url + '/backtest/strategy_stats', 
            headers=self.get_headers(),
            verify=self.safe_mode)
        
        if response.status_code == 200:
            return response.json()
        return None



    def get_broker_stats(self, broker_id):
        response = requests.get(
            self.base_url + '/backtest/broker_stats', 
            headers=self.get_headers(),
            json={"broker_id": broker_id},
            verify=self.safe_mode)
        
        if response.status_code == 200:
            return response.json()
        return None

    '''
    -------------------------------------------------
    |               BACKTEST REQUEST                |
    -------------------------------------------------
    '''

    def get_strategies(self):
            response = requests.get(
                self.base_url + '/backtest/get_strategies', 
                headers=self.get_headers(),
                verify=self.safe_mode)
            
            if response.status_code == 200:
                return response.json()
            return None

    '''
    -------------------------------------------------
    |                 START BACKTEST                 |
    -------------------------------------------------
    '''

    def start_backtest(
            self, 
            start_date, 
            end_date, 
            strategy_name,
            ohlcv_data_pool, 
            strategy_params, 
            brokers_config):
        
        json = {
            "start_date": start_date,
            "end_date": end_date,
            "strategy": strategy_name,
            "ohlcv_data_pool": ohlcv_data_pool,
            "strategy_params": strategy_params,
            "brokers_config": brokers_config
        }

        response = requests.post(
            self.base_url + '/backtest/start', 
            headers=self.get_headers(),
            json=json,
            verify=self.safe_mode)
        
        if response.status_code == 200:
            return response.json()
        if not response.status_code == 200:
            logging.error(response.json())
            raise Exception(response.json())

        return False


