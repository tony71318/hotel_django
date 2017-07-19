# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response

import json
import time

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
	abi = [ { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" } ], "name": "new_order", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'true', "inputs": [], "name": "owner_2", "outputs": [ { "name": "", "type": "address" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [], "name": "order_id_table_size", "outputs": [ { "name": "", "type": "uint256" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" } ], "name": "delete_order", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'true', "inputs": [], "name": "owner", "outputs": [ { "name": "", "type": "address" } ], "payable": 'false', "type": "function" }, { "constant": 'true', "inputs": [ { "name": "", "type": "uint256" } ], "name": "order_id_table", "outputs": [ { "name": "", "type": "bytes" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "order_id", "type": "bytes" } ], "name": "check", "outputs": [ { "name": "", "type": "bool" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "newOwner", "type": "address" } ], "name": "transferOwnership", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "newOwner", "type": "address" } ], "name": "addOwnership", "outputs": [], "payable": 'false', "type": "function" }, { "anonymous": 'false', "inputs": [ { "indexed": 'false', "name": "order_id", "type": "bytes" } ], "name": "new_order_event", "type": "event" }, { "anonymous": 'false', "inputs": [ { "indexed": 'false', "name": "order_id", "type": "bytes" } ], "name": "update_order_event", "type": "event" }, { "anonymous": 'false', "inputs": [ { "indexed": 'false', "name": "order_id", "type": "bytes" } ], "name": "delete_order_event", "type": "event" } ]
	address = '0x20054728a550aC384C5C72Aa4CEF5B6942f8A4E7'

	myContract = web3.eth.contract(abi=abi,address=address)			

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

		total_room = {
			'1': 3,
			'2': 4
		}

		# post 的資料
		user_id = request.POST['user_id']
		room_id = request.POST['room_id']
		checkin_date = request.POST['checkin_date']

		room_type = room_id[0]
		ordered_room_count = 0

		order_id = checkin_date + '_' + room_type + '_' + time.strftime("%I:%M:%S") + user_id;	

		# 檢查有無相同order_id
		if myContract.call().check(order_id) == False:
			output = json.dumps({'result': 'order is not available'}, sort_keys=True, indent=4)
			return HttpResponse(output, content_type="application/json")
		else:	
			# 查詢所有的order_id
			size = myContract.call().order_id_table_size()		
			for i in range(0,size):
				if 'id_table' in locals():
					id_table.append(myContract.call().order_id_table(i))
				else:
					id_table = [myContract.call().order_id_table(i)]
			if 'id_table' in locals():		
				print(id_table)		

				# 計算該房型已被預訂幾間房
				for i in id_table:
					if myContract.call().check(i) == False:
						order_checkin_date,order_room_type,order_order_id = i.split('_')
						if order_room_type == room_type and order_checkin_date == checkin_date:
							ordered_room_count += 1
				print(ordered_room_count)	

			if ordered_room_count >= total_room[room_type]:
				output = json.dumps({'result': 'order is not available'}, sort_keys=True, indent=4)
				return HttpResponse(output, content_type="application/json")
			else:
				web3.personal.unlockAccount(web3.eth.coinbase, 'internintern')

				transaction = myContract.transact({'from': web3.eth.coinbase}).new_order(order_id)
				output = json.dumps({'result': transaction}, sort_keys=True, indent=4)
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


