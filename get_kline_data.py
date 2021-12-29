# -*- coding: utf-8 -*-
"""
  @ Author:   Mr.Hat
  @ Email:    shenghong6560@gmail.com
  @ Date:     2021/12/29 12:00
  @ Description: 
  @ History:
"""
import xml.dom.minidom as xmldom
from threading import Thread
import requests
import zipfile
import tempfile
from datetime import datetime, timedelta
from loguru import logger


symbols = ["1000SHIBUSDT", "1000XECUSDT", "1INCHUSDT", "AAVEUSDT", "ADABUSD", "ADAUSDT", "AKROUSDT", "ALGOUSDT",
           "ALICEUSDT", "ALPHAUSDT", "ANKRUSDT", "ANTUSDT", "ARPAUSDT", "ARUSDT", "ATAUSDT", "ATOMUSDT",
           "AUDIOUSDT", "AVAXUSDT", "AXSUSDT", "BAKEUSDT", "BALUSDT", "BANDUSDT", "BATUSDT", "BCHUSDT", "BELUSDT",
           "BLZUSDT", "BNBBUSD", "BNBUSDT", "BTCBUSD", "BTCDOMUSDT", "BTCSTUSDT", "BTCUSDT", "BTSUSDT", "BTTUSDT",
           "BZRXUSDT", "C98USDT", "CELOUSDT", "CELRUSDT", "CHRUSDT", "CHZUSDT", "COMPUSDT", "COTIUSDT", "CRVUSDT",
           "CTKUSDT", "CTSIUSDT", "CVCUSDT", "DASHUSDT", "DEFIUSDT", "DENTUSDT", "DGBUSDT", "DODOUSDT", "DOGEBUSD",
           "DOGEUSDT", "DOTUSDT", "DYDXUSDT", "EGLDUSDT", "ENJUSDT", "ENSUSDT", "EOSUSDT", "ETCUSDT", "ETHBUSD",
           "ETHUSDT", "FILUSDT", "FLMUSDT", "FTMUSDT", "FTTBUSD", "GALAUSDT", "GRTUSDT", "GTCUSDT", "HBARUSDT",
           "HNTUSDT", "HOTUSDT", "ICPUSDT", "ICXUSDT", "IOSTUSDT", "IOTAUSDT", "IOTXUSDT", "KAVAUSDT", "KEEPUSDT",
           "KLAYUSDT", "KNCUSDT", "KSMUSDT", "LINAUSDT", "LINKUSDT", "LITUSDT", "LPTUSDT", "LRCUSDT", "LTCUSDT",
           "LUNAUSDT", "MANAUSDT", "MASKUSDT", "MATICUSDT", "MKRUSDT", "MTLUSDT", "NEARUSDT", "NEOUSDT", "NKNUSDT",
           "NUUSDT", "OCEANUSDT", "OGNUSDT", "OMGUSDT", "ONEUSDT", "ONTUSDT", "PEOPLEUSDT", "QTUMUSDT", "RAYUSDT",
           "REEFUSDT", "RENUSDT", "RLCUSDT", "RSRUSDT", "RUNEUSDT", "RVNUSDT", "SANDUSDT", "SCUSDT", "SFPUSDT",
           "SKLUSDT", "SNXUSDT", "SOLBUSD", "SOLUSDT", "SRMUSDT", "STMXUSDT", "STORJUSDT", "SUSHIUSDT", "SXPUSDT",
           "THETAUSDT", "TLMUSDT", "TOMOUSDT", "TRBUSDT", "TRXUSDT", "UNFIUSDT", "UNIUSDT", "VETUSDT", "WAVESUSDT",
           "XEMUSDT", "XLMUSDT", "XMRUSDT", "XRPBUSD", "XRPUSDT", "XTZUSDT", "YFIIUSDT", "YFIUSDT", "ZECUSDT",
           "ZENUSDT", "ZILUSDT", "ZRXUSDT"]

time_ = ["1m", "3m", "5m", "15m", "30m", "1h", "4h"]


def get_binance_kline_data(symbol, time_, data_time):
    uri = f"https://data.binance.vision/data/futures/um/daily/klines/{symbol}/{time_}/{symbol}-{time_}-{data_time}.zip"
    try:
        data = requests.get(uri).content

        _tmp_file = tempfile.TemporaryFile()  # 创建临时文件

        _tmp_file.write(data)  # byte字节数据写入临时文件

        zf = zipfile.ZipFile(_tmp_file, mode='r')
        for names in zf.namelist():
            f = zf.extract(names, f'./kline_data/{symbol}/{time_}')  # 解压到zip目录文件下
            logger.error(f"{symbol}---{time_}---{data_time}---{f}")

        zf.close()
    except:
        pass


def get_data_df_time(s, dm):
    dt = datetime(2021, 6, 1)
    for i in range(0, 365):
        ta = dt + timedelta(days=i)
        d = ta.day if int(ta.day) > 9 else f"0{ta.day}"
        m = ta.month if int(ta.month) > 9 else f"0{ta.month}"
        ts = f"{ta.year}-{m}-{d}"
        if ts == "2021-12-28":
            break

        get_binance_kline_data(s, dm, ts)


def get_csv_data(s):
    for dm in time_:
        t = Thread(target=get_data_df_time, args=(s, dm, ))
        t.start()


if __name__ == '__main__':
    # get_binance_kline_data("ADAUSDT", "5m", "2021-08-12")
    for s in symbols:
        t = Thread(target=get_csv_data, args=(s,))
        t.start()

