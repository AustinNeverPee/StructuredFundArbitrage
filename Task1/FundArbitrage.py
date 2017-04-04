# -*- coding: utf-8 -*-
# 分级基金的折价套利

import struct
import numpy as np
import csv

# 定义基金的结构
StockData = np.dtype({
    'names': ['date', 'open', 'high', 'low', 'close', 'amount', 'vol'],
    'formats': ['i', 'f', 'f', 'f', 'f', 'f', 'i']}, align=True)

# 储存基金数据的列表
FoFsList = [];
AFList = [];
BFList = [];

# 打开数据文件
ff = open("Data/sh502020.day","rb");
fa = open("Data/sh502021.day","rb");
fb = open("Data/sh502022.day","rb");

# 累计天数
count = 0;

# 循环读入多天的日线数据
try:
	while True:
		data_f = ff.read(32);
		data_a = fa.read(32);
		data_b = fb.read(32);
		if not (data_f and data_a and data_b):
			break
		
		_data_f = struct.unpack("iiiiifii", data_f);
		_data_a = struct.unpack("iiiiifii", data_a);
		_data_b = struct.unpack("iiiiifii", data_b);

		# 添加历史日线数据
		day_data_f = struct.pack("ifffffi", 
			_data_f[0],
			_data_f[1] / 100.0,
			_data_f[2] / 100.0,
			_data_f[3] / 100.0,
			_data_f[4] / 100.0,
			_data_f[5],
			_data_f[6]);
		day_data_a = struct.pack("ifffffi", 
			_data_a[0],
			_data_a[1] / 100.0,
			_data_a[2] / 100.0,
			_data_a[3] / 100.0,
			_data_a[4] / 100.0,
			_data_a[5],
			_data_a[6]);
		day_data_b = struct.pack("ifffffi", 
			_data_b[0],
			_data_b[1] / 100.0,
			_data_b[2] / 100.0,
			_data_b[3] / 100.0,
			_data_b[4] / 100.0,
			_data_b[5],
			_data_b[6]);
		fofs = np.array([day_data_f], dtype=StockData);
		af = np.array([day_data_a], dtype=StockData);
		bf = np.array([day_data_b], dtype=StockData);
		FoFsList.append(fofs)
		AFList.append(af)
		BFList.append(bf)

		count += 1;
finally:
	# 关闭数据文件
	ff.close()
	fa.close()
	fb.close()

print("共记录了该分级基金%d天的日线数据，日期从%d到%d。"
	%(count, FoFsList[0]['date'], FoFsList[count-1]['date']))

# 分析历史数据，判断哪一天可以做折价套利
GoodFund = [];
for i in range(0, count):
	# 假设a、b基金的份额占比为1:1
	# a、b合并后，母基金交易价格
	ConvergePrice = (AFList[i]['close'] + BFList[i]['close']) / 2;

	# 整体折价率
	DiscountRate = (FoFsList[i]['close'] - ConvergePrice) / FoFsList[i]['close'];

	# 赎回费
	RedemptionFee = 0.005;

	# 买进费用
	PurchaseCost = 0.0005;

	# 利润阈值
	ProfitThreshold = 0.01;

	# 判断利润是否到达设定的阈值
	if DiscountRate - RedemptionFee - PurchaseCost >= ProfitThreshold:
		GoodFund.append([FoFsList[i]['date'], DiscountRate])

		print("该分级基金在%d可以进行折价套利，其整体折价率为%f"
			%(FoFsList[i]['date'], DiscountRate))

# 导出数据到excel
csvfile = open('FundData.csv', 'a+', newline='');
spamwriter = csv.writer(csvfile)
# 基金信息
spamwriter.writerow(['date', 
	'open(母)', 'high(母)', 'low(母)', 'close(母)', 'amount(母)', 'vol(母)', 
	'open(A)', 'high(A)', 'low(A)', 'close(A)', 'amount(A)', 'vol(A)',
	'open(B)', 'high(B)', 'low(B)', 'close(B)', 'amount(B)', 'vol(B)',])
for i in range(0, count):
	spamwriter.writerow([FoFsList[i]['date'], 
		FoFsList[i]['open'], FoFsList[i]['high'], FoFsList[i]['low'], FoFsList[i]['close'], FoFsList[i]['amount'], FoFsList[i]['vol'],
		AFList[i]['open'], AFList[i]['high'], AFList[i]['low'], AFList[i]['close'], AFList[i]['amount'], AFList[i]['vol'],
		BFList[i]['open'], BFList[i]['high'], BFList[i]['low'], BFList[i]['close'], BFList[i]['amount'], BFList[i]['vol']])

spamwriter.writerow('')

# 适合折价套利的日期
spamwriter.writerow(['good enough for discount arbitrage'])
spamwriter.writerow(['date', 'discount rate'])
for GoodFundItem in GoodFund:
	spamwriter.writerow([GoodFundItem[0], GoodFundItem[1]])
csvfile.close()