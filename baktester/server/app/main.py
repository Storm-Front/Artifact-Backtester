import os
import asyncio
import uvloop
from psycopg_pool import ConnectionPool

from artifact.common.api.settings.settings import ApiSettings #type: ignore

from artifact.core.clusters.cluster import Cluster #type: ignore
from artifact.components.catalog.catalog_service import CatalogService #type: ignore
from artifact.components.clock.clock_service import ClockService #type: ignore
from artifact.components.index_map.index_map_service import IndexMapService #type: ignore
from artifact.components.asset_db.asset_db_service import AssetDBService #type: ignore
from artifact.components.exchange_db.exchange_db_service import ExchangeDBService #type: ignore
from artifact.components.ohlcv_db.ohlcv_db_service import OhlcvDBService #type: ignore
from artifact.components.data_sources.yfinance.yf_api import Yf_Api #type: ignore

from artifact.interfaces.data_manager.data_manager_interface import DataManagerInterface #type: ignore
from artifact.components.snapshot_service.snapshot_service import SnapshotService #type: ignore
from artifact.components.backtest.backtest import Backtest #type: ignore
from artifact.interfaces.backtester.backtester_interface import BacktesterInterface #type: ignore

from src.security.certificates_generator import generate_certificates
from src.security.password_encrypter import get_password_encrypted  

import signal
import sys
import time


async def main():

        pool = ConnectionPool(os.getenv('DB_URL'), min_size=1, max_size=10,open=True)
        generate_certificates()

        print(os.getenv('JWT_SECRET'))
        api_settings = ApiSettings(
                os.getenv('SERVER_USERNAME'),
                get_password_encrypted(os.getenv('SERVER_PASSWORD')),
                '0.0.0.0',
                int(os.getenv('PORT')),
                './certs',
                os.getenv('JWT_SECRET'),
                'HS256',
                60*24
            )

        artifact = Cluster('Backtester')
        task=asyncio.create_task(artifact.start())


        await asyncio.sleep(0.1)
        
        backtester_interface = BacktesterInterface(api_settings)
        backtester_interface.start()  
              
        catalog_service = CatalogService(pool)
        catalog_service.start()

        exchange_service = ExchangeDBService(pool)
        exchange_service.start()

        index_map_service = IndexMapService(pool)
        index_map_service.start()

        ohlcv_db_service = OhlcvDBService(pool)
        ohlcv_db_service.start()

        asset_service = AssetDBService(pool)
        asset_service.start()

        clock_service = ClockService()
        clock_service.start()

        snapshot_service = SnapshotService()
        snapshot_service.start() 



        backtest= Backtest()
        backtest.start()

        await task


if __name__ == "__main__":
    with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
        runner.run(main())

