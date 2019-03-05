import os
import re

DEBUG_LOG_FUNCTION_RE = re.compile(r'nrf_802154_log_entry\(\s*(\w+)\s*,\s*\d+\s*\);', re.MULTILINE)

DRV_SRC_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../src'))

print(DRV_SRC_PATH)

MODULE_HEX_ID_MAP = {
    'nrf_802154_rsch.c': '4900'
}

for dir_path, dirs, files in os.walk(DRV_SRC_PATH):
    for file in files:
        with open(os.path.join(dir_path, file)) as file_handler:
            module_id = MODULE_HEX_ID_MAP.get(file, 'FFFF')
            print('{} ({})'.format(file, module_id))

            decoder = []
            defines = []

            for index, function in enumerate(DEBUG_LOG_FUNCTION_RE.findall(file_handler.read())):
                hex_id = hex(int(module_id, 16) + index)
                decoder.append('            {{id: "FUNCTION_{}", val: {}, from: "RSCH", to: "RSCH", text: "{}()"}},'.format(function, hex_id, function))
                defines.append('#define FUNCTION_{:<40} {}UL'.format(function, hex_id))

            if decoder:
                print('\n'.join(decoder))
            if defines:
                print('\n'.join(defines))
