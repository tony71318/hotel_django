# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response

import json

from web3 import Web3, KeepAliveRPCProvider, IPCProvider
web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))

def get(request,title):

	if title == 'peers':	
		ouptput = json.dumps(web3.admin.peers, sort_keys=True, indent=4)
		return HttpResponse(ouptput, content_type="application/json")

	if title == 'nodeinfo':	
		output = json.dumps(web3.admin.nodeInfo, sort_keys=True, indent=4)
		return HttpResponse(output, content_type="application/json")	

	if title == 'node':	
		output = json.dumps(web3.version.node, sort_keys=True, indent=4)
		return HttpResponse(output, content_type="application/json")		

	if title == 'network':	
		output = json.dumps(web3.version.network, sort_keys=True, indent=4)
		return HttpResponse(output, content_type="application/json")		

	if title == 'accounts':	
		output = json.dumps(web3.personal.listAccounts, sort_keys=True, indent=4)
		return HttpResponse(output, content_type="application/json")		

	if title == 'block':	
		number = int(request.GET['number'])

		output = json.dumps(web3.eth.getBlock(int(number)), sort_keys=True, indent=4)
		return HttpResponse(output, content_type="application/json")					

def multiply_contract(request,function):			
	abi = [ { "constant": 'false', "inputs": [ { "name": "x", "type": "int256" }, { "name": "y", "type": "int256" } ], "name": "multiply", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "_plus", "type": "address" }, { "name": "x", "type": "int256" }, { "name": "y", "type": "int256" } ], "name": "delegateToPlus", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'true', "inputs": [], "name": "z", "outputs": [ { "name": "", "type": "int256", "value": "6" } ], "payable": 'false', "type": "function" } ]
	address = '0x5022be5267afD7156096aF8EE18aA18d7ee9C7b5'
	myContract = web3.eth.contract(abi=abi,address=address)

	if function == 'value':
		output = json.dumps(myContract.call().z(), sort_keys=True, indent=4)
		return HttpResponse(output, content_type="application/json")

	if function == 'multiply':
		x = int(request.GET['x'])
		y = int(request.GET['y'])

		web3.personal.unlockAccount(web3.eth.coinbase, 'internintern')

		output = json.dumps(myContract.transact({'from': web3.eth.coinbase}).multiply(x,y), sort_keys=True, indent=4)
		return HttpResponse(output, content_type="application/json")		

def booking_contract(request,function):		

	# 建立contract's instance 
	# abi = [ { "constant": 'false', "inputs": [], "name": "order_id_table_size", "outputs": [ { "name": "", "type": "uint256" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" } ], "name": "update_paid", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" } ], "name": "get_all_2", "outputs": [ { "name": "", "type": "bytes" }, { "name": "", "type": "bytes" }, { "name": "", "type": "bool" }, { "name": "", "type": "bool" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" }, { "name": "name", "type": "bytes" }, { "name": "room_id", "type": "uint256" }, { "name": "number_of_people", "type": "uint256" }, { "name": "price", "type": "uint256" }, { "name": "date", "type": "bytes" }, { "name": "time", "type": "bytes" } ], "name": "update_order", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" } ], "name": "update_checkin", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" } ], "name": "delete_order", "outputs": [], "payable": 'false', "type": "function" }, { "constant": "true", "inputs": [], "name": "owner", "outputs": [ { "name": "", "type": "address" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" }, { "name": "name", "type": "bytes" }, { "name": "room_id", "type": "uint256" }, { "name": "number_of_people", "type": "uint256" }, { "name": "price", "type": "uint256" }, { "name": "date", "type": "bytes" }, { "name": "time", "type": "bytes" } ], "name": "new_order", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" } ], "name": "get_all_1", "outputs": [ { "name": "", "type": "bytes" }, { "name": "", "type": "bytes" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" } ], "payable": 'false', "type": "function" }, { "constant": "true", "inputs": [ { "name": "", "type": "uint256" } ], "name": "order_id_table", "outputs": [ { "name": "", "type": "bytes" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" } ], "name": "check", "outputs": [ { "name": "", "type": "bool" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "newOwner", "type": "address" } ], "name": "transferOwnership", "outputs": [], "payable": 'false', "type": "function" }, { "anonymous": 'false', "inputs": [ { "indexed": 'false', "name": "order_id", "type": "bytes" }, { "indexed": 'false', "name": "name", "type": "bytes" }, { "indexed": 'false', "name": "room_id", "type": "uint256" }, { "indexed": 'false', "name": "number_of_people", "type": "uint256" }, { "indexed": 'false', "name": "price", "type": "uint256" }, { "indexed": 'false', "name": "date", "type": "bytes" }, { "indexed": 'false', "name": "time", "type": "bytes" } ], "name": "new_order_event", "type": "event" }, { "anonymous": 'false', "inputs": [ { "indexed": 'false', "name": "order_id", "type": "bytes" }, { "indexed": 'false', "name": "name", "type": "bytes" }, { "indexed": 'false', "name": "room_id", "type": "uint256" }, { "indexed": 'false', "name": "number_of_people", "type": "uint256" }, { "indexed": 'false', "name": "price", "type": "uint256" }, { "indexed": 'false', "name": "date", "type": "bytes" }, { "indexed": 'false', "name": "time", "type": "bytes" } ], "name": "update_order_event", "type": "event" }, { "anonymous": 'false', "inputs": [ { "indexed": 'false', "name": "order_id", "type": "bytes" }, { "indexed": 'false', "name": "paid", "type": "bool" } ], "name": "update_paid_event", "type": "event" }, { "anonymous": 'false', "inputs": [ { "indexed": 'false', "name": "order_id", "type": "bytes" }, { "indexed": 'false', "name": "checkin", "type": "bool" } ], "name": "update_checkin_event", "type": "event" }, { "anonymous": 'false', "inputs": [ { "indexed": 'false', "name": "order_id", "type": "bytes" } ], "name": "delete_order_event", "type": "event" } ]
	# address = '0x2c3db28d761D5375f4d8E3C6025ac8d990Aad18b'
	abi = [ { "constant": 'true', "inputs": [], "name": "owner_2", "outputs": [ { "name": "", "type": "address", "value": "0xae75dffd61993cb18321862aaa6c800ce930c2d7" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [], "name": "order_id_table_size", "outputs": [ { "name": "", "type": "uint256" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" } ], "name": "update_paid", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" } ], "name": "get_all_2", "outputs": [ { "name": "", "type": "bytes" }, { "name": "", "type": "bytes" }, { "name": "", "type": "bool" }, { "name": "", "type": "bool" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" }, { "name": "name", "type": "bytes" }, { "name": "room_id", "type": "uint256" }, { "name": "number_of_people", "type": "uint256" }, { "name": "price", "type": "uint256" }, { "name": "date", "type": "bytes" }, { "name": "time", "type": "bytes" } ], "name": "update_order", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" } ], "name": "update_checkin", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" } ], "name": "delete_order", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'true', "inputs": [], "name": "owner", "outputs": [ { "name": "", "type": "address", "value": "0x291837238f171047afb414152c2c58d6cf887481" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" }, { "name": "name", "type": "bytes" }, { "name": "room_id", "type": "uint256" }, { "name": "number_of_people", "type": "uint256" }, { "name": "price", "type": "uint256" }, { "name": "date", "type": "bytes" }, { "name": "time", "type": "bytes" } ], "name": "new_order", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" } ], "name": "get_all_1", "outputs": [ { "name": "", "type": "bytes" }, { "name": "", "type": "bytes" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" } ], "payable": 'false', "type": "function" }, { "constant": 'true', "inputs": [ { "name": "", "type": "uint256" } ], "name": "order_id_table", "outputs": [ { "name": "", "type": "bytes" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" } ], "name": "check", "outputs": [ { "name": "", "type": "bool" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "newOwner", "type": "address" } ], "name": "transferOwnership", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "newOwner", "type": "address" } ], "name": "addOwnership", "outputs": [], "payable": 'false', "type": "function" }, { "anonymous": 'false', "inputs": [ { "indexed": 'false', "name": "order_id", "type": "bytes" }, { "indexed": 'false', "name": "name", "type": "bytes" }, { "indexed": 'false', "name": "room_id", "type": "uint256" }, { "indexed": 'false', "name": "number_of_people", "type": "uint256" }, { "indexed": 'false', "name": "price", "type": "uint256" }, { "indexed": 'false', "name": "date", "type": "bytes" }, { "indexed": 'false', "name": "time", "type": "bytes" } ], "name": "new_order_event", "type": "event" }, { "anonymous": 'false', "inputs": [ { "indexed": 'false', "name": "order_id", "type": "bytes" }, { "indexed": 'false', "name": "name", "type": "bytes" }, { "indexed": 'false', "name": "room_id", "type": "uint256" }, { "indexed": 'false', "name": "number_of_people", "type": "uint256" }, { "indexed": 'false', "name": "price", "type": "uint256" }, { "indexed": 'false', "name": "date", "type": "bytes" }, { "indexed": 'false', "name": "time", "type": "bytes" } ], "name": "update_order_event", "type": "event" }, { "anonymous": 'false', "inputs": [ { "indexed": 'false', "name": "order_id", "type": "bytes" }, { "indexed": 'false', "name": "paid", "type": "bool" } ], "name": "update_paid_event", "type": "event" }, { "anonymous": 'false', "inputs": [ { "indexed": 'false', "name": "order_id", "type": "bytes" }, { "indexed": 'false', "name": "checkin", "type": "bool" } ], "name": "update_checkin_event", "type": "event" }, { "anonymous": 'false', "inputs": [ { "indexed": 'false', "name": "order_id", "type": "bytes" } ], "name": "delete_order_event", "type": "event" } ]
	address = '0x7064691E8548db91BDF74A858Aeb38Fd24e10976'

	myContract = web3.eth.contract(abi=abi,address=address)

	# Ｇet Method 獲得指定訂單id的資訊
	if function == 'get':
		order_id = request.GET['order_id']

		output = myContract.call().get_all_1(order_id)
		output.extend(myContract.call().get_all_2(order_id))

		keys = ['order_id','name','room_id','number_of_people','price','date','time','paid','checkin']
		output = dict((k,output[keys.index(k)]) for k in keys)

		output = json.dumps(output, indent=4)

		return HttpResponse(output, content_type="application/json")

	# Ｇet Method 獲得全部訂單的資訊
	if function == 'get_all':

		size = myContract.call().order_id_table_size()

		for i in range(0,size):
			key = myContract.call().order_id_table(i)

			output = myContract.call().get_all_1(key)
			output.extend(myContract.call().get_all_2(key))

			keys = ['order_id','name','room_id','number_of_people','price','date','time','paid','checkin']
			output = dict((k,output[keys.index(k)]) for k in keys)

			if 'orders' in locals():
				orders.append(output)
			else:
				orders = []
				orders.append(output)	

		output = json.dumps(orders, indent=4)

		return HttpResponse(output, content_type="application/json")			

	# Ｇet Method 獲得全部的order_id
	if function == 'order_id':

		size = myContract.call().order_id_table_size()

		for i in range(0,size):
			if 'output' in locals():
				output.append(myContract.call().order_id_table(i))
			else:
				output = [myContract.call().order_id_table(i)]

		output = json.dumps(output, sort_keys=True, indent=4)

		return HttpResponse(output, content_type="application/json")	

	# Ｇet Method 檢查特定房間時段能否入住
	if function == 'check':
		order_id = request.GET['order_id']

		output = myContract.call().check(order_id)

		output_data = {'check': output}
		output_json = json.dumps(output_data)

		return HttpResponse(output_json, content_type="application/json")	

	# Post Method 新增一筆訂單
	if function == 'post':
		# order_id = request.POST['order_id']
		name = request.POST['name']
		room_id = int(request.POST['room_id'])
		# number_of_people = int(request.POST['number_of_people'])
		# price = int(request.POST['price'])
		checkin_date = request.POST['checkin_date']
		# time = request.POST['time']

		order_id = str(room_id) + '_' + checkin_date;
		print(order_id)

		return HttpResponse(json.dumps(room_id, sort_keys=True, indent=4), content_type="application/json")

		# if myContract.call().check(order_id) == True:
		# 	web3.personal.unlockAccount(web3.eth.coinbase, 'internintern')

		# 	transaction = myContract.transact({'from': web3.eth.coinbase}).new_order(order_id,name,room_id,number_of_people,price,date,time)
		# 	output = json.dumps({'result': transaction}, sort_keys=True, indent=4)
		# 	return HttpResponse(output, content_type="application/json")
		# else:
		# 	output = json.dumps({'result': 'order is not available'}, sort_keys=True, indent=4)
		# 	return HttpResponse(output, content_type="application/json")

	# Post Method 更新一筆訂單
	if function == 'update':
		order_id = request.POST['order_id']
		name = request.POST['name']
		room_id = int(request.POST['room_id'])
		number_of_people = int(request.POST['number_of_people'])
		price = int(request.POST['price'])
		date = request.POST['date']
		time = request.POST['time']

		if myContract.call().check(order_id) == False:
			web3.personal.unlockAccount(web3.eth.coinbase, 'internintern')

			transaction = myContract.transact({'from': web3.eth.coinbase}).update_order(order_id,name,room_id,number_of_people,price,date,time)
			output = json.dumps({'result': transaction}, sort_keys=True, indent=4)
			return HttpResponse(output, content_type="application/json")
		else:
			output = json.dumps({'result': 'order is not exist'}, sort_keys=True, indent=4)
			return HttpResponse(output, content_type="application/json")		

	# Post Method 刪除一筆訂單
	if function == 'delete':
		order_id = request.POST['order_id']

		if myContract.call().check(order_id) == False:
			web3.personal.unlockAccount(web3.eth.coinbase, 'internintern')

			transaction = myContract.transact({'from': web3.eth.coinbase}).delete_order(order_id)
			output = json.dumps({'result': transaction}, sort_keys=True, indent=4)
			return HttpResponse(output, content_type="application/json")
		else:
			output = json.dumps({'result': 'order is not exist'}, sort_keys=True, indent=4)
			return HttpResponse(output, content_type="application/json")

	# Post Method 更新一筆訂單的支付狀態
	if function == 'update_paid':
		order_id = request.POST['order_id']

		if myContract.call().check(order_id) == False:
			web3.personal.unlockAccount(web3.eth.coinbase, 'internintern')

			transaction = myContract.transact({'from': web3.eth.coinbase}).update_paid(order_id)
			output = json.dumps({'result': transaction}, sort_keys=True, indent=4)
			return HttpResponse(output, content_type="application/json")
		else:
			output = json.dumps({'result': 'order is not exist'}, sort_keys=True, indent=4)
			return HttpResponse(output, content_type="application/json")		

	# Post Method 更新一筆訂單的入住狀態
	if function == 'update_checkin':
		order_id = request.POST['order_id']

		if myContract.call().check(order_id) == False:
			web3.personal.unlockAccount(web3.eth.coinbase, 'internintern')

			transaction = myContract.transact({'from': web3.eth.coinbase}).update_checkin(order_id)
			output = json.dumps({'result': transaction}, sort_keys=True, indent=4)
			return HttpResponse(output, content_type="application/json")
		else:
			output = json.dumps({'result': 'order is not exist'}, sort_keys=True, indent=4)
			return HttpResponse(output, content_type="application/json")				



