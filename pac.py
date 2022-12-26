 #!/usr/bin/python3
 #coding: utf-8
 
import pandas as pd
import settings as setting
import requests, datetime, time, os

def discord(message):
	if setting.DISCORD_URL == '': return
	try:
		requests.post(setting.DISCORD_URL, data={'content': ' ' + message + ' '})
	except:
		print('error! discord notify sending message')

def ex_base_to_ten(array,data,base):
	for i,j in enumerate(array[data]):
		if j == '0x':
			array.at[i,data] = 0.0
		else:
			array.at[i,data] = int(j,base)
	return array

def get_etherscan_info(_address, _startBlock):
	ethscanAdd = setting.ETHERSCAN_ADDRESS0 + _address + setting.ETHERSCAN_ADDRESS1 + str(_startBlock) + setting.ETHERSCAN_ADDRESS2 \
                 + setting.ETHERSCAN_ADDRESS3 + setting.ETHERSCAN_ADDRESS4 + setting.ETHERSCAN_API_KEY
	responseEthscan = requests.get(ethscanAdd)
	responseEthscanj = pd.DataFrame(responseEthscan.json())
	res1 = responseEthscanj['result']
	res2 = res1.to_json()
	res3 = pd.read_json(res2)
	ethscan = res3.T
	print("address =" , _address)
	return ethscan

def trans_type(_array):
	#  Since the data type does not match, after outputting to csv, type conversion by reading csv
	_array.to_csv('temp.csv', index = False)
	time.sleep(1)
	newarray = pd.read_csv('temp.csv', encoding='utf8', dtype={'input': str, 'contractAddress': str, 'cumulativeGasUsed': str, \
                'gasUsed': str, 'confirmations': str, 'methodId': str, 'functionName': str})
	os.remove('temp.csv')
	return newarray

def max_num(_array, _index):
	maxNum = _array[_index].max()
	return maxNum

def find_new_data_loc(_array, _latestBlockNumber):
	#  Find out what row data of LatestBlockNumber is in csvLatestBlockNumber
	for i ,j in enumerate(_array['blockNumber']):
		if j == _latestBlockNumber:
			row = i + 1	
	etherScanNewSl = _array[row:]
	return etherScanNewSl
	
def conv_unix_human_time(_array):
	#  convert unit time to human time　UTC+0
	for i, j in enumerate(_array['timeStamp']):
		_array.iat[i, 1] = datetime.datetime.fromtimestamp(j)
	return _array

def tx_discord(_df, _name, _address):
	#  Notification of newly added Tx in contract by discord webhook
	cc = 0
	for i, j in enumerate(_df['functionName']):
		if 'airdrop' in str(j) or 'safeTransferFrom' in str(j):
			print("airdrop or safeTransferFrom")
		else:
			if cc == 0:
				ment="@here"
			else:
				ment=""
			message =  ment\
						+ "```New Transaction\n" \
						+ "From              : " + _name + "\n"\
						+ "DateTime(UTC+0)   : " + str(_df.at[i, 'timeStamp']) + "\n"\
						+ "BlockNo           : " + str(_df.at[i, 'blockNumber']) + "\n"\
						+ "MethodId          : " + str(_df.at[i, 'methodId']) + "\n"\
						+ "Function          : " + str(j) + "```"
			discord(message)
			cc  += 1
			time.sleep(3)
	#  Finally notify Etherscan link
	if cc != 0: 
		message =  _address
		discord(message)

def check_tx_update(_csvTxData, _etherScanAddress, _discordNotifyName, _discordNotifyLink, _csvLink):
	csvLatestBlockNumber =  max_num(_csvTxData, 'blockNumber')
	ethscan = get_etherscan_info(_etherScanAddress, csvLatestBlockNumber)
	etherscanNew = trans_type(ethscan)
	etherScanLastestBlockNumber = max_num(etherscanNew, 'blockNumber')
	etherScanNewSl = find_new_data_loc(etherscanNew, csvLatestBlockNumber)
	etherScanNewSl = conv_unix_human_time(etherScanNewSl)
	txdataAll = pd.concat([_csvTxData, etherScanNewSl], axis=0)
	txdataAll.to_csv(_csvLink, index = False) 
	time.sleep(2)
	print("csvLatestBlockNumber        = ", csvLatestBlockNumber)
	print("etherScanLastestBlockNumber = ", etherScanLastestBlockNumber)
	#  Re-roll the index. To use the col index name in .at when discord notification
	etherScanNewSlRe = etherScanNewSl.reset_index()
	if etherScanNewSlRe.empty:
		print("There were no new TXs in the address history")
	else:
		print(etherScanNewSlRe)
	tx_discord(etherScanNewSlRe, _discordNotifyName, _discordNotifyLink)
