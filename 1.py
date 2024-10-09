import VARIATION
import VARIATION.MODBUS
data = b'\x00\x01\x02\x03\x04\x05\x06\x07'
# print(VARIATION.MODBUS.GENERAL_FUZZ_CHANGE(data))

# Map = []
# print(Map.count(b'\x123'))
# print(data[:2])

print(VARIATION.MODBUS.GENERAL_FUZZ_CHANGE(b'\x01\x02\x03\x04\x05\x06\x07\x08'))