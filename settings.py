#!/usr/bin/python3
#coding: utf-8

ETHERSCAN_API_KEY 	= ''  #  Etherscan api key
DISCORD_URL 		= ''  #  Discord notify  Webhook URL
SLEEP				= 3530  #  interval time that check transaction and notify. unit: sec


#  Monitoring settings
param_list = ('address1',)  #  If you want the second one to be monitored, add it after ","
param = {
	'address1' : {
		'address' : '0x623FC4F577926c0aADAEf11a243754C546C1F98c',
		'name' : '*****:Deployer',  #  Discord notify
		'csv' : 'tx_data.csv'
	},
	'address2' : {
		'address' : '0x12eA19217C65F36385bB030D00525c1034E2F0Af',
		'name' : '*****:Deployer',  #  Discord notify
		'csv' : '*****.csv'
	}
}

#  Etherscan api
ETHERSCAN_ADDRESS0 = 'https://api.etherscan.io/api?module=account&action=txlist&address='
ETHERSCAN_ADDRESS1 = '&startblock='
ETHERSCAN_ADDRESS2 = '&endblock=99999999&page=1&offset='
ETHERSCAN_ADDRESS3 = '1000'
ETHERSCAN_ADDRESS4 = '&sort=asc&apikey='
