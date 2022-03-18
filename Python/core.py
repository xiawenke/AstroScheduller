'''
Author: your name
Date: 2022-03-17 21:20:04
LastEditTime: 2022-03-17 23:36:34
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /AstroSchedullerGo/Python/core.py
'''

import os
import json
import requests
import hashlib
import ctypes
from utilities import utilities

class core():
    def __init__(self):
        self.u = utilities()
        self.coreInfo = {
            "version": "0.9.2",
            "config": False,
            "configUrl": "https://raw.githubusercontent.com/xiawenke/AstroSchedullerGo/Dev/releases_latest/_scheduller.config",
            "corePath": self.u.get_dir(__file__) + "/lib/_scheduller.so",
            "configPath": self.u.get_dir(__file__) + "/lib/_scheduller.config"
        }
        
        # Check if the AstroSchedullerGo Module exists\
        if(not os.path.isdir(self.u.get_dir(self.coreInfo["corePath"]))):
            os.mkdir(self.u.get_dir(self.coreInfo["corePath"]))
        
        self.get_core_info()
        
        if(not os.path.isfile(self.coreInfo["corePath"])):
            self.download_core()
        
        self.check_integrity()
    
    def get_core_info(self):
        try:
            self.coreInfo["config"] = json.loads(requests.get(self.coreInfo["configUrl"]).text)
            try:
                self.coreInfo["config"] = self.coreInfo["config"][self.coreInfo["version"]]
            except Exception as e:
                print("get_core_info: AstroSchedullerGo no longer support for version", self.coreInfo["version"])
                exit()
                
        except Exception as e:
            print(str(e), " -> working without internet connection. ")
            
            if(os.path.isfile(self.coreInfo["configPath"])):
                self.coreInfo["config"] = json.loads(open(self.coreInfo["configPath"]).read())
            else:
                print("get_core_info: Need internet to initialize. (If you are working offline, see https://github.com/xiawenke/AstroSchedullerGo for more information.)")
                exit()
        
        open(self.coreInfo["configPath"], "w+").write(json.dumps(self.coreInfo["config"]))
        
        return True
    
    def download_core(self):
        print("Downloading AstroSchedullerGo Module...")
            
        try:
            #open(self.coreInfo["corePath"], "wb").write(requests.get(self.coreInfo["config"]["url"], stream=True).content)
            
            req = requests.get(self.coreInfo["config"]["url"], stream=True)
            with open(self.coreInfo["corePath"], 'wb') as f:
                f.write(req.content)
        except Exception as e:
            print(str(e), " -> AstroSchedullerGo Module does not exists. Try again after check the internet connection. (If you are working offline, see https://github.com/xiawenke/AstroSchedullerGo for more information.)")
            exit()
        
        print("Downloading AstroSchedullerGo Module... Done.")
        return True
    
    def check_integrity(self):
        try:
            if(hashlib.md5(open(self.coreInfo["corePath"], "rb").read()).hexdigest() == self.coreInfo["config"]["md5"]):
                print("check_integrity: pass")
                return True
            else:
                print("check_integrity: not pass")
                self.download_core()
                return self.check_integrity()
        except Exception as e:
            print("check_integrity: not check", str(e))
            return False
    
    def reset():
        # Delete the file.
        return True
    
    def go_schedule(self, importPath, exportPath):
        goHandle = ctypes.cdll.LoadLibrary(self.coreInfo["corePath"])
        goHandle.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        goHandle.py_schedule(importPath.encode(), exportPath.encode())
        
        if(not os.path.isfile(importPath) or not os.path.isfile(exportPath)):
            return False
        
        return True
        