# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response

import json
import time

from django.core import serializers

from web3 import Web3, KeepAliveRPCProvider, IPCProvider
web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))

# database
from owlting_hotel.models import Order,Room

# terminal color
color_front = '\x1b[7;30;42m'
color_end = '\x1b[0m'
def print_color(text):
	print(color_front + text + color_end)





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
	abi = [ { "constant": 'false', "inputs": [ { "name": "key", "type": "bytes" }, { "name": "order_id", "type": "bytes" }, { "name": "user_id", "type": "bytes" }, { "name": "room_type", "type": "uint256" }, { "name": "date", "type": "bytes" } ], "name": "new_order", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'true', "inputs": [ { "name": "", "type": "uint256" } ], "name": "rooms", "outputs": [ { "name": "id", "type": "uint256" }, { "name": "total_room", "type": "uint256" } ], "payable": 'false', "type": "function" }, { "constant": 'true', "inputs": [], "name": "owner_2", "outputs": [ { "name": "", "type": "address" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "old_key", "type": "bytes" }, { "name": "new_key", "type": "bytes" }, { "name": "order_id", "type": "bytes" }, { "name": "user_id", "type": "bytes" }, { "name": "room_type", "type": "uint256" }, { "name": "date", "type": "bytes" } ], "name": "update_order", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "room_type", "type": "uint256" } ], "name": "delete_room", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "room_type", "type": "uint256" }, { "name": "total_room", "type": "uint256" } ], "name": "add_room", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "key", "type": "bytes" } ], "name": "delete_order", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'true', "inputs": [], "name": "owner", "outputs": [ { "name": "", "type": "address" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "room_type", "type": "uint256" }, { "name": "total_room", "type": "uint256" } ], "name": "edit_room", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "room_type", "type": "uint256" }, { "name": "date", "type": "bytes" } ], "name": "check", "outputs": [ { "name": "", "type": "bool" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "key", "type": "bytes" } ], "name": "order_detail", "outputs": [ { "name": "", "type": "bytes" }, { "name": "", "type": "bytes" }, { "name": "", "type": "uint256" }, { "name": "", "type": "bytes" } ], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "newOwner", "type": "address" } ], "name": "transferOwnership", "outputs": [], "payable": 'false', "type": "function" }, { "constant": 'false', "inputs": [ { "name": "newOwner", "type": "address" } ], "name": "addOwnership", "outputs": [], "payable": 'false', "type": "function" }, { "inputs": [], "payable": 'false', "type": "constructor" } ]
	address = '0x3c33958659F3aE489BD2472D3967bdf4e14a7E27'

	myContract = web3.eth.contract(abi=abi,address=address)			

	# Post Method 新增一筆訂單
	if function == 'post':

		# post 的資料
		user_id = request.POST['user_id']
		room_id = request.POST['room_id']
		checkin_date = request.POST['checkin_date']

		room_type = room_id[0]

		order_id = time.strftime("%y-%m-%d_%H:%M:%S") + '_' + user_id
		key = order_id + checkin_date
		print_color('key: ' + key)

		# 檢查能不能預定
		if myContract.call().check(int(room_type),checkin_date) == False:
			output = json.dumps({'result': 'order is not available'}, sort_keys=True, indent=4)
			return HttpResponse(output, content_type="application/json")
		else:	
			web3.personal.unlockAccount(web3.eth.coinbase, 'internintern')

			# 訂單寫入區塊鏈
			transaction = myContract.transact({'from': web3.eth.coinbase}).new_order(key,order_id,user_id,int(room_type),checkin_date)
			print_color('transaction: ' + transaction)

			# 訂單寫入資料庫
			order = Order.objects.create(order_id=order_id, name=user_id, room_type=room_type, room_id=room_id,start_date=checkin_date,duration='1',paid=False)

			output = json.dumps({'result': transaction}, sort_keys=True, indent=4)
			return HttpResponse(output, content_type="application/json")		

	# Post Method 刪除一筆訂單
	if function == 'delete':
		order_id = request.POST['order_id']
		room_id = request.POST['room_id']
		checkin_date = request.POST['checkin_date']

		room_type = room_id[0]

		key = order_id + checkin_date

		if myContract.call().check(order_id) == False:
			web3.personal.unlockAccount(web3.eth.coinbase, 'internintern')

			transaction = myContract.transact({'from': web3.eth.coinbase}).delete_order(order_id)
			output = json.dumps({'result': transaction}, sort_keys=True, indent=4)
			return HttpResponse(output, content_type="application/json")
		else:
			output = json.dumps({'result': 'order is not exist'}, sort_keys=True, indent=4)
			return HttpResponse(output, content_type="application/json")

	if function == 'list_all':

		order_data_json = serializers.serialize('json', Order.objects.all())
		return HttpResponse(order_data_json, content_type="application/json")	


