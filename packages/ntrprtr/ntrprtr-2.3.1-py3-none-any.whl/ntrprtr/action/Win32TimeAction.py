from datetime import datetime, timezone

from datetime import datetime

from ntrprtr.action.ActionBase import ActionBase

class Win32TimeAction(ActionBase):
    def __init__(self):
        super().__init__()
        self._config["endianess"] = "little"

    def process(self, action, _bytes):
        self._mergeConfig(action)
        result = ""
        c = self._cnvrtr
        hexValues = _bytes.hex(" ")
        
        endianess = self._config["endianess"]
        if(endianess == "big"):
            result = self._cnvrtr.hexToDec(_bytes.hex())
        elif(endianess == "little"):
            result = self.__hexToLittleEndianToDec(_bytes)  

        dtObj =  self.__convert(result)

        return str(dtObj.strftime("%d.%m.%y %H:%M:%S UTC"))

    def __hexToLittleEndianToDec(self, byteArr):
        le = self._cnvrtr.toLittleEndian(byteArr.hex(" "))
        return self._cnvrtr.hexToDec(le)

    def __convert(self, windows_timestamp):
        unix_epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        windows_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
        epoch_delta = unix_epoch - windows_epoch
        windows_timestamp_in_seconds = windows_timestamp / 10_000_000
        unix_timestamp = windows_timestamp_in_seconds - epoch_delta.total_seconds()

        return datetime.utcfromtimestamp(unix_timestamp)