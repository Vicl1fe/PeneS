from PyQt5 import QtWidgets
from ui_setting import Ui_Dialog_Setting

class Setting(QtWidgets.QDialog):
    def __init__(self,config):
        super().__init__()
        # 初始化界面
        self.window2 = Ui_Dialog_Setting()
        self.window2.setupUi(self)

        self.config = config
        # Google初始化
        self.Google_Init()
        # fofa初始化
        self.FOFA_Init()

        # 给cancel绑定退出函数
        self.window2.buttonBox_FOFASetting_button.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.close)

    def Load_GoogleSetting_To_GUI(self):
        # 如果已经保存过，将配置文件中的proxy加载到gui中
        if "proxy" in self.config.config["google"]:
            if self.config.config["google"]["proxy"]:
                if self.config.config["google"]["proxy"].startswith("http://"):
                    self.window2.comboBox_GoogleSetting_protocol.setCurrentIndex(0)
                    temp = self.config.config["google"]["proxy"].replace("http://", "")
                elif self.config.config["google"]["proxy"].startswith("socks5://"):
                    self.window2.comboBox_GoogleSetting_protocol.setCurrentIndex(1)
                    temp = self.config.config["google"]["proxy"].replace("socks5://", "")
                ip = temp.split(":")[0]
                port = temp.split(":")[1]
                self.window2.lineEdit_GoogleSetting_ip.setText(ip)
                self.window2.lineEdit_GoogleSetting_port.setText(port)

    def Load_FofaSetting_To_GUI(self):
        if "email" in self.config.config["fofa"]:
            self.window2.lineEdit_FOFASetting_Email.setText(self.config.config["fofa"]["email"])
        if "key" in self.config.config["fofa"]:
            self.window2.lineEdit_FOFASetting_Key.setText(self.config.config["fofa"]["key"])

        # host title ip domain port country province city country_name header server protocol banner cert
        if "save" in self.config.config["fofa"]:
            if self.config.config["fofa"]["save"]["host"][0] == 1:self.window2.checkBox_FOFASetting_export_host.setChecked(True)
            if self.config.config["fofa"]["save"]["ip"][0] == 1:self.window2.checkBox_FOFASetting_export_ip.setChecked(True)
            if self.config.config["fofa"]["save"]["port"][0] == 1:self.window2.checkBox_FOFASetting_export_port.setChecked(True)
            if self.config.config["fofa"]["save"]["title"][0] == 1:self.window2.checkBox_FOFASetting_export_title.setChecked(True)
            if self.config.config["fofa"]["save"]["domain"][0] == 1:self.window2.checkBox_FOFASetting_export_domain.setChecked(True)
            if self.config.config["fofa"]["save"]["country"][0] == 1:self.window2.checkBox_FOFASetting_export_country.setChecked(True)
            if self.config.config["fofa"]["save"]["province"][0] == 1:self.window2.checkBox_FOFASetting_export_province.setChecked(True)
            if self.config.config["fofa"]["save"]["city"][0] == 1:self.window2.checkBox_FOFASetting_export_city.setChecked(True)
            if self.config.config["fofa"]["save"]["header"][0] == 1:self.window2.checkBox_FOFASetting_export_header.setChecked(True)
            if self.config.config["fofa"]["save"]["server"][0] == 1:self.window2.checkBox_FOFASetting_export_server.setChecked(True)
            if self.config.config["fofa"]["save"]["protocol"][0] == 1:self.window2.checkBox_FOFASetting_export_protocol.setChecked(True)
            if self.config.config["fofa"]["save"]["banner"][0] == 1:self.window2.checkBox_FOFASetting_export_banner.setChecked(True)
            if self.config.config["fofa"]["save"]["cert"][0] == 1:self.window2.checkBox_FOFASetting_export_cert.setChecked(True)
            if self.config.config["fofa"]["save"]["country_name"][0] == 1:self.window2.checkBox_FOFASetting_export_country_name.setChecked(True)


    def FOFA_Init(self):
        # 记录单选框点击的顺序
        self.checkbox_num = self.config.Fofa_save_num()

        # 加载配置文件到GUi
        self.Load_FofaSetting_To_GUI()
        # Fofa设置中的buttonBox点击保存。
        self.window2.buttonBox_FOFASetting_button.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.FOFA_Setting)

        # 端口checkbox点击事件
        self.window2.checkBox_FOFASetting_export_port.clicked.connect(self.checkbox_port_click)
        self.window2.checkBox_FOFASetting_export_ip.clicked.connect(self.checkbox_ip_click)
        self.window2.checkBox_FOFASetting_export_host.clicked.connect(self.checkbox_host_click)
        self.window2.checkBox_FOFASetting_export_domain.clicked.connect(self.checkbox_domain_click)
        self.window2.checkBox_FOFASetting_export_title.clicked.connect(self.checkbox_title_click)
        self.window2.checkBox_FOFASetting_export_country.clicked.connect(self.checkbox_country_click)
        self.window2.checkBox_FOFASetting_export_country_name.clicked.connect(self.checkbox_country_name_click)
        self.window2.checkBox_FOFASetting_export_protocol.clicked.connect(self.checkbox_protocol_click)
        self.window2.checkBox_FOFASetting_export_province.clicked.connect(self.checkbox_province_click)
        self.window2.checkBox_FOFASetting_export_city.clicked.connect(self.checkbox_city_click)
        self.window2.checkBox_FOFASetting_export_header.clicked.connect(self.checkbox_header_click)
        self.window2.checkBox_FOFASetting_export_server.clicked.connect(self.checkbox_server_click)
        self.window2.checkBox_FOFASetting_export_cert.clicked.connect(self.checkbox_cert_click)
        self.window2.checkBox_FOFASetting_export_banner.clicked.connect(self.checkbox_banner_click)

    def checkbox_port_click(self):
        flag = "port"
        if self.window2.checkBox_FOFASetting_export_port.isChecked() == True:
            self.checkbox_num += 1
            self.config.config["fofa"]["save"][flag][1] = self.checkbox_num
            # 表示为选中状态
            self.config.config["fofa"]["save"][flag][0] = 1
        else:
            temp = self.config.config["fofa"]["save"][flag][1]
            self.checkbox_1(temp)
            # 表示为未选中状态
            self.config.config["fofa"]["save"][flag][0] = 0
            # 未选中状态下的"顺序"标记为0
            self.config.config["fofa"]["save"][flag][1] = 0
            self.checkbox_num -= 1
        print(self.config.config["fofa"]["save"])
    def checkbox_ip_click(self):
        flag = "ip"
        if self.window2.checkBox_FOFASetting_export_ip.isChecked() == True:
            self.checkbox_num += 1
            self.config.config["fofa"]["save"][flag][1] = self.checkbox_num
            # # 表示为选中状态
            self.config.config["fofa"]["save"][flag][0] = 1
        else:
            temp = self.config.config["fofa"]["save"][flag][1]
            self.checkbox_1(temp)
            # 表示为未选中状态
            self.config.config["fofa"]["save"][flag][0] = 0
            # 未选中状态下的"顺序"标记为0
            self.config.config["fofa"]["save"][flag][1] = 0
            self.checkbox_num -= 1
        # print(self.config.config["fofa"]["save"])
    def checkbox_host_click(self):
        flag = "host"
        if self.window2.checkBox_FOFASetting_export_host.isChecked() == True:
            self.checkbox_num += 1
            self.config.config["fofa"]["save"][flag][1] = self.checkbox_num
            # # 表示为选中状态
            self.config.config["fofa"]["save"][flag][0] = 1
        else:
            temp = self.config.config["fofa"]["save"][flag][1]
            self.checkbox_1(temp)
            # 表示为未选中状态
            self.config.config["fofa"]["save"][flag][0] = 0
            # 未选中状态下的"顺序"标记为0
            self.config.config["fofa"]["save"][flag][1] = 0
            self.checkbox_num -= 1
        print(self.config.config["fofa"]["save"])
    def checkbox_title_click(self):
        flag = "title"
        if self.window2.checkBox_FOFASetting_export_title.isChecked() == True:
            self.checkbox_num += 1
            self.config.config["fofa"]["save"][flag][1] = self.checkbox_num
            # # 表示为选中状态
            self.config.config["fofa"]["save"][flag][0] = 1
        else:
            temp = self.config.config["fofa"]["save"][flag][1]
            self.checkbox_1(temp)
            # 表示为未选中状态
            self.config.config["fofa"]["save"][flag][0] = 0
            # 未选中状态下的"顺序"标记为0
            self.config.config["fofa"]["save"][flag][1] = 0
            self.checkbox_num -= 1
        print(self.config.config["fofa"]["save"])
    def checkbox_domain_click(self):
        flag = "domain"
        if self.window2.checkBox_FOFASetting_export_domain.isChecked() == True:
            self.checkbox_num += 1
            self.config.config["fofa"]["save"][flag][1] = self.checkbox_num
            # # 表示为选中状态
            self.config.config["fofa"]["save"][flag][0] = 1
        else:
            temp = self.config.config["fofa"]["save"][flag][1]
            self.checkbox_1(temp)
            # 表示为未选中状态
            self.config.config["fofa"]["save"][flag][0] = 0
            # 未选中状态下的"顺序"标记为0
            self.config.config["fofa"]["save"][flag][1] = 0
            self.checkbox_num -= 1
        print(self.config.config["fofa"]["save"])
    def checkbox_country_click(self):
        flag = "country"
        if self.window2.checkBox_FOFASetting_export_country.isChecked() == True:
            self.checkbox_num += 1
            self.config.config["fofa"]["save"][flag][1] = self.checkbox_num
            # # 表示为选中状态
            self.config.config["fofa"]["save"][flag][0] = 1
        else:
            temp = self.config.config["fofa"]["save"][flag][1]
            self.checkbox_1(temp)
            # 表示为未选中状态
            self.config.config["fofa"]["save"][flag][0] = 0
            # 未选中状态下的"顺序"标记为0
            self.config.config["fofa"]["save"][flag][1] = 0
            self.checkbox_num -= 1
        print(self.config.config["fofa"]["save"])
    def checkbox_province_click(self):
        flag = "province"
        if self.window2.checkBox_FOFASetting_export_province.isChecked() == True:
            self.checkbox_num += 1
            self.config.config["fofa"]["save"][flag][1] = self.checkbox_num
            # # 表示为选中状态
            self.config.config["fofa"]["save"][flag][0] = 1
        else:
            temp = self.config.config["fofa"]["save"][flag][1]
            self.checkbox_1(temp)
            # 表示为未选中状态
            self.config.config["fofa"]["save"][flag][0] = 0
            # 未选中状态下的"顺序"标记为0
            self.config.config["fofa"]["save"][flag][1] = 0
            self.checkbox_num -= 1
        print(self.config.config["fofa"]["save"])
    def checkbox_city_click(self):
        flag = "city"
        if self.window2.checkBox_FOFASetting_export_city.isChecked() == True:
            self.checkbox_num += 1
            self.config.config["fofa"]["save"][flag][1] = self.checkbox_num
            # # 表示为选中状态
            self.config.config["fofa"]["save"][flag][0] = 1
        else:
            temp = self.config.config["fofa"]["save"][flag][1]
            self.checkbox_1(temp)
            # 表示为未选中状态
            self.config.config["fofa"]["save"][flag][0] = 0
            # 未选中状态下的"顺序"标记为0
            self.config.config["fofa"]["save"][flag][1] = 0
            self.checkbox_num -= 1
        print(self.config.config["fofa"]["save"])
    def checkbox_country_name_click(self):
        flag = "country_name"
        if self.window2.checkBox_FOFASetting_export_country_name.isChecked() == True:
            self.checkbox_num += 1
            self.config.config["fofa"]["save"][flag][1] = self.checkbox_num
            # # 表示为选中状态
            self.config.config["fofa"]["save"][flag][0] = 1
        else:
            temp = self.config.config["fofa"]["save"][flag][1]
            self.checkbox_1(temp)
            # 表示为未选中状态
            self.config.config["fofa"]["save"][flag][0] = 0
            # 未选中状态下的"顺序"标记为0
            self.config.config["fofa"]["save"][flag][1] = 0
            self.checkbox_num -= 1
        print(self.config.config["fofa"]["save"])
    def checkbox_header_click(self):
        flag = "header"
        if self.window2.checkBox_FOFASetting_export_header.isChecked() == True:
            self.checkbox_num += 1
            self.config.config["fofa"]["save"][flag][1] = self.checkbox_num
            # # 表示为选中状态
            self.config.config["fofa"]["save"][flag][0] = 1
        else:
            temp = self.config.config["fofa"]["save"][flag][1]
            self.checkbox_1(temp)
            # 表示为未选中状态
            self.config.config["fofa"]["save"][flag][0] = 0
            # 未选中状态下的"顺序"标记为0
            self.config.config["fofa"]["save"][flag][1] = 0
            self.checkbox_num -= 1
        print(self.config.config["fofa"]["save"])
    def checkbox_server_click(self):
        flag = "server"
        if self.window2.checkBox_FOFASetting_export_server.isChecked() == True:
            self.checkbox_num += 1
            self.config.config["fofa"]["save"][flag][1] = self.checkbox_num
            # # 表示为选中状态
            self.config.config["fofa"]["save"][flag][0] = 1
        else:
            temp = self.config.config["fofa"]["save"][flag][1]
            self.checkbox_1(temp)
            # 表示为未选中状态
            self.config.config["fofa"]["save"][flag][0] = 0
            # 未选中状态下的"顺序"标记为0
            self.config.config["fofa"]["save"][flag][1] = 0
            self.checkbox_num -= 1
        print(self.config.config["fofa"]["save"])
    def checkbox_protocol_click(self):
        flag = "protocol"
        if self.window2.checkBox_FOFASetting_export_protocol.isChecked() == True:
            self.checkbox_num += 1
            self.config.config["fofa"]["save"][flag][1] = self.checkbox_num
            # # 表示为选中状态
            self.config.config["fofa"]["save"][flag][0] = 1
        else:
            temp = self.config.config["fofa"]["save"][flag][1]
            self.checkbox_1(temp)
            # 表示为未选中状态
            self.config.config["fofa"]["save"][flag][0] = 0
            # 未选中状态下的"顺序"标记为0
            self.config.config["fofa"]["save"][flag][1] = 0
            self.checkbox_num -= 1
        print(self.config.config["fofa"]["save"])
    def checkbox_banner_click(self):
        flag = "banner"
        if self.window2.checkBox_FOFASetting_export_banner.isChecked() == True:
            self.checkbox_num += 1
            self.config.config["fofa"]["save"][flag][1] = self.checkbox_num
            # # 表示为选中状态
            self.config.config["fofa"]["save"][flag][0] = 1
        else:
            temp = self.config.config["fofa"]["save"][flag][1]
            self.checkbox_1(temp)
            # 表示为未选中状态
            self.config.config["fofa"]["save"][flag][0] = 0
            # 未选中状态下的"顺序"标记为0
            self.config.config["fofa"]["save"][flag][1] = 0
            self.checkbox_num -= 1
        print(self.config.config["fofa"]["save"])
    def checkbox_cert_click(self):
        flag = "cert"
        if self.window2.checkBox_FOFASetting_export_cert.isChecked() == True:
            self.checkbox_num += 1
            self.config.config["fofa"]["save"][flag][1] = self.checkbox_num
            # # 表示为选中状态
            self.config.config["fofa"]["save"][flag][0] = 1
        else:
            temp = self.config.config["fofa"]["save"][flag][1]
            self.checkbox_1(temp)
            # 表示为未选中状态
            self.config.config["fofa"]["save"][flag][0] = 0
            # 未选中状态下的"顺序"标记为0
            self.config.config["fofa"]["save"][flag][1] = 0
            self.checkbox_num -= 1
        print(self.config.config["fofa"]["save"])
    def checkbox_1(self,temp):
        if "save" in self.config.config["fofa"]:
            for i in self.config.config["fofa"]["save"]:
                if self.config.config["fofa"]["save"][i][1] > temp:
                    self.config.config["fofa"]["save"][i][1] -=1


    def Google_Init(self):
        # 加载配置文件到GUi
        self.Load_GoogleSetting_To_GUI()
        # Google设置中的buttonBox点击保存。
        self.window2.buttonBox_GoogleSetting_button.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.Google_Setting)

    def Google_Setting(self):
        # 定义保存代理信息的字典
        proxy_set = {}
        # 获取代理协议名称
        protocol = self.window2.comboBox_GoogleSetting_protocol.currentText()
        ip = self.window2.lineEdit_GoogleSetting_ip.text()
        port = self.window2.lineEdit_GoogleSetting_port.text()

        proxy_set["proxy"] = protocol+ip+":"+port

        self.config.config["google"] = proxy_set
        # 如果ip和port都为空，则删除proxy键
        if ip == "" and port == "":
            self.config.config.pop("proxy")
        self.config.save()
        # self.window2.buttonBox.
        # print(self.window2.buttonBox.standardButton())

    def FOFA_Setting(self):
        # 保存email和key的字典
        fofa_setting = {}
        # 获取FOFA所需的key
        email = self.window2.lineEdit_FOFASetting_Email.text().strip()
        key = self.window2.lineEdit_FOFASetting_Key.text().strip()
        if email != "":
            self.config.config["fofa"]["email"] = email
        if key != "":
            self.config.config["fofa"]["key"] = key

        # print(self.config.config["fofa"]["save"])
        self.config.save()
        self.close()

