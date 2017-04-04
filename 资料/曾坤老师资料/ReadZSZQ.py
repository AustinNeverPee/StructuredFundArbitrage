# -*- coding: utf-8 -*-

import struct
import numpy as np


# StockData = np.dtype({
#     'names': ['date', 'open', 'high', 'low', 'close', 'amount', 'vol', 'reservation'],
#     'formats': ['i', 'i', 'i', 'i', 'i', 'f', 'i', 'i']}, align=True)


StockData = np.dtype({
    'names': ['date', 'open', 'high', 'low', 'close', 'amount', 'vol'],
    'formats': ['i', 'f', 'f', 'f', 'f', 'f', 'i']}, align=True)


fn = "sh600004.day";
fid = open(fn,"rb");
data0 = fid.read(32);

_data = struct.unpack("iiiiifii", data0);

c = _data;
date_ = c[0];
open_ = c[1]/100.0;
high_ = c[2]/100.0;
low_  = c[3]/100.0;
close_= c[4]/100.0;
amount_= c[5];
vol_   = c[6];

DayData = struct.pack("ifffffi", _data[0], open_, high_, low_, close_, amount_, vol_);

a = np.array([DayData], dtype=StockData);
StockDataList = [];

StockDataList.append(a)
print StockDataList[0]['date']
print StockDataList[0]['open']
print StockDataList[0]['high']
print StockDataList[0]['low']
print StockDataList[0]['amount']
print StockDataList[0]['vol']


# DayData = struct.pack("iffffii", _data[0], open_, high_, low_, close_, _data[5], _data[6]);
#
# a = np.array([DayData], dtype=StockData);
# StockDataList = [];
#
# StockDataList.append(a)
# print StockDataList[0]['date']
# print StockDataList[0]['open']

