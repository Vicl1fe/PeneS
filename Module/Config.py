import sys
import os
import json

class Config:
    def __init__(self):
        self.exePath = os.path.dirname(sys.argv[0])
        dirs = "config"
        self.filename = dirs + "/config.json"
        self.config = {}
        # 加载旧的配置文件
        if os.path.exists(self.exePath+"/"+self.filename):
            with open(self.exePath+"/"+self.filename,"r",encoding="utf-8") as f:
                self.config = json.loads(f.readline().strip())
        else:
            # 初始化模块的配置
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            self.config["google"] = {}
            self.config["fofa"] = {}
            # 1表示选中，0表示没选中
            # host title ip domain port country province city country_name header server protocol banner cert
            # URL IP 端口 标题 域名
            # self.config["fofa"]["save"] = [1,1,1]
            self.config["fofa"]["save"] = {
                "host":[1,1], # 就是Url,[1,0]第一个元素表示被选中，第二个元素是表格中位置
                "ip":[1,2],
                "port":[1,3],
                "title": [1, 4],
                "domain": [0, 0],
                "protocol": [0, 0],
                "banner": [0, 0],
                "cert": [0, 0],
                "country": [0, 0],
                "province": [0, 0],
                "country_name": [0, 0],
                "header": [0, 0],
                "server": [0, 0],
                "city": [0, 0],
            }

    def save(self):
        config_json = json.dumps(self.config)
        with open(self.exePath+"/"+self.filename,"w",encoding="utf-8") as f:
            f.write(config_json)

    # 返回复选框已经选中的数量
    def Fofa_save_num(self):
        num = 0
        if "save" in self.config["fofa"]:
            for i in self.config["fofa"]["save"]:
                if self.config["fofa"]["save"][i][0] == 1:
                    num += 1

        return num

    def reload(self):
        # 加载旧的配置文件
        if os.path.exists(self.exePath + "/" + self.filename):
            with open(self.exePath + "/" + self.filename, "r", encoding="utf-8") as f:
                self.config = json.loads(f.readline().strip())
                return True
        else:
            return False