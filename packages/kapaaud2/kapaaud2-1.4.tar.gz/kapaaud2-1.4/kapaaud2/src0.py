-- Version: Lua 5.3.5
-- 此线程为主线程，可调用任何指令

local ip="192.168.1.12"
local port=4001
local err=0
local socket=0
local code=0
local Option={SpeedL=50, AccL=20, Start=170, ZLimit=170, End=170,SYNC=1}
Jump(P1, Option)

while true do
	::create_server::
	err, socket = TCPCreate(false, ip, port)
	if err ~= 0 then
		print("Failed to create socket, re-connecting")
		Sleep(1000)
		goto create_server
	end
	err = TCPStart(socket, 0)
	if err ~= 0 then
		print("Failed to start server, re-connecting")
		TCPDestroy(socket)
		Sleep(1000)
		goto create_server
	end
	while true do
		err, buf = TCPRead(socket, 0,"string")
		data =buf.buf
		if err ~= 0 then
			print("Failed to read data, re-connecting")
			TCPDestroy(socket)
			Sleep(1000)
			break
		end
		print(data)
		if  data== "A1" then
			Jump(P8, Option)
			DO(1,1)
			Jump(P9, Option)			
			DO(1,0)
			Jump(P1, Option)
			TCPWrite(socket,"fw")	
		elseif  data== "B1" then
			Jump(P8, Option)
			DO(1,1)
			Jump(P10, Option)			
			DO(1,0)
			Jump(P1, Option)
			TCPWrite(socket,"fw")	
		elseif  data== "C1" then
			Jump(P8, Option)
			DO(1,1)
			Jump(P11, Option)			
			DO(1,0)
			Jump(P1, Option)
			TCPWrite(socket,"fw")	
		elseif  data== "D1" then
			Jump(P8, Option)
			DO(1,1)
			Jump(P12, Option)			
			DO(1,0)
			Jump(P1, Option)
			TCPWrite(socket,"fw")	
		end	
			
			
	end
end