import network
import socket
from time import sleep
from machine import Pin, Timer
from mywifi import networksetting

ssid, password = networksetting()

led_one = Pin(14, Pin.OUT)
led_two = Pin(15, Pin.OUT)

timer=Timer(-1)
timer2=Timer(-1)

def Website():
    value_one = led_one.value()
    value_two = led_two.value()
    website = """<!DOCTYPE html>
    <html>
        <head> <title>Lutz Embedded Tec! Raspberry Pico W</title>
        <meta http-equiv="refresh" content="5">
        </head>
        <body>
            <h1>Lutz Embedded Tec! Raspberry Pico W</h1>
            
            <table style="width:400px" class="center">
                  <tr>
                    <th><center>LED Number </center></th>
                    <th><center>Button </center> </th>
                    <th><center>Delay </center> </th>
                    <th><center>Pin State</center> </th>
                  </tr>
                  <tr>
                    <td><center>one </td>
                    <td><center><input type='button' value='toggle' onclick='toggleLed("one")'/> </center></td>
                    <td><center><input type='text' value="0" id="delay_one"> </center></td>
                    <td> <center>  <span id="value_one">""" + str(value_one) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>two</center> </td>
                    <td><center><input type='button' value='toggle' onclick='toggleLed("two")'/></center></td>
                    <td><center><input type='text' value="0" id="delay_two"> </center></td>
                    <td><center>  <span id="value_two">""" + str(value_two) + """</span></center></td>
                   </tr>
            </table>
            

                        
            <script>
                function toggleLed(led){
                    var delay = document.getElementById('delay_'+led).value;
                    var xhttp = new XMLHttpRequest();
                    xhttp.open('GET', '/led/'+led+'/'+delay, true);
                    xhttp.send();
                }

                    
            </script>
        </body>
    </html>
    """
    return website

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 10
print('Waiting for connection')
while max_wait > 10:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1    
    sleep(1)
status = None
if wlan.status() != 3:
    raise RuntimeError('Connections failed')
else:
    status = wlan.ifconfig()
    print('connection to', ssid,'succesfull established!', sep=' ')
    print('IP-adress: ' + status[0])
ipAddress = status[0]
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
while True:
    try:
        cl, addr = s.accept()
        print('Connection from ', addr, "accepted!")
        request = cl.recv(1024)
        request = str(request)
        
        if request.find('/led/') == 6:
            split_request=request.split()
            split2_request=split_request[1].split('/')
            print(split2_request[3])


            if request.find('/led/one') == 6:
                timer.init(period=int(split2_request[3]),mode=Timer.ONE_SHOT, callback=lambda t:led_one.toggle())
                

            if request.find('/led/two') == 6:
                timer2.init(period=int(split2_request[3]),mode=Timer.ONE_SHOT, callback=lambda t:led_two.toggle())
                

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(Website())
        cl.close()
    except OSError as e:
        cl.close()
        print('connection closed')

