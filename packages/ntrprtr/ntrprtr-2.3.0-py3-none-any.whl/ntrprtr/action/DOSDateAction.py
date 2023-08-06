from ntrprtr.action.ActionBase import ActionBase

class DOSDateAction(ActionBase):
    def __init__(self):
        super().__init__()
        self._config["endianess"] = "little"

    def process(self, action, _bytes):
        self._mergeConfig(action)
        r = ""
        c = self._cnvrtr
        hexValues = _bytes.hex(" ")

        endianess = self._config["endianess"]
        if(endianess == "big"):
            r = self._cnvrtr.hexToBin(_bytes.hex()).rjust(16, "0")
        elif(endianess == "little"):
            r = c.hexToBin(c.toLittleEndian(hexValues)).rjust(16, "0")
        
        yearBits = [r[i:i + 7] for i in range(0, 7, 7)][0]
        monthBits = [r[i:i + 4] for i in range(7, 11, 4)][0]
        dayBits = [r[i:i + 5] for i in range(11, 16, 5)][0]

        return str(c.binToDec(dayBits)) + "." + str(c.binToDec(monthBits)) + "." +  str(c.binToDec(yearBits)+1980)