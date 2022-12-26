 #!/usr/bin/python3
 #coding: utf-8
 
import pandas as pd
import settings as setting
import requests, datetime, time
import pac as pc

while True:
	try:
		print("-------start-------")
		print(str(datetime.datetime.now())[:19])

		for contra in setting.param_list:
			#  You will get a warning if you don't specify a dtype. There may be a better way.
			txData = pd.read_csv(setting.param[contra]['csv'], encoding='utf8', dtype={'input': str, 'contractAddress': str,\
								 'cumulativeGasUsed': str, 'gasUsed': str, 'confirmations': str, 'methodId': str, 'functionName': str})
			#  set param
			fileName = setting.param[contra]['csv'] 
			etherScanAddress = setting.param[contra]['address'] 
			discordNotifyName = setting.param[contra]['name']
			discordNotifyLink = 'https://etherscan.io/address/' + setting.param[contra]['address']
			pc.check_tx_update(txData, etherScanAddress, discordNotifyName, discordNotifyLink, fileName)
			print("\n")

		print(str(datetime.datetime.now())[:19])

		#  Confirmation of bot running
		if datetime.datetime.now().hour == 11:
			message = "```" + str(datetime.datetime.now())[:19] + " (UTC+0)" + "   bot is running ... " +  "```"
			pc.discord(message)

		print("end")
		time.sleep(setting.SLEEP)

	except requests.exceptions.RequestException as e:
		print("error! : ", e)
