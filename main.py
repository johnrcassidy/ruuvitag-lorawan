import machine
import ustruct

import settings

from node import LoRaWANNode
from ruuvitag.scanner import RuuviTagScanner


def pack_temp(temp):
    """Temperature in 0.005 degrees as signed short"""
    temp_conv = round(round(temp, 2) / 0.005)
    temp_int16 = ustruct.pack('!h', temp_conv)
    return temp_int16


def pack_hum(hum):
    """Humidity in 0.0025 percent as unsigned short"""
    hum_conv = round(round(hum, 2) / 0.0025)
    hum_int16 = ustruct.pack('!H', hum_conv)
    return hum_int16


payload = b''

rts = RuuviTagScanner(settings.RUUVITAGS)

# get all data and prepare payload
print('harvest ruuvitags')
for ruuvitag in rts.find_ruuvitags(timeout=settings.TIMEOUT):
    id_payload = settings.RUUVITAGS.index(ruuvitag.mac.encode())
    temp_payload = pack_temp(ruuvitag.temperature)
    hum_payload = pack_hum(ruuvitag.humidity)
    payload = payload + bytes([id_payload]) + temp_payload + hum_payload

print('setup lorawan')
node = LoRaWANNode(settings.NODE_APP_EUI, settings.NODE_APP_KEY)

print('send payload')
node.send(payload)

print('enter deepsleep for {} ms'.format(settings.NODE_DEEPSLEEP))
machine.deepsleep(settings.NODE_DEEPSLEEP)
