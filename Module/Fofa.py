import requests
from base64 import b64encode
import json
from PyQt5 import QtWidgets,QtCore
import queue
import threading
import os
import time
from Module.GlobalC import GlobalC

from Module.fofa_help import Ui_Fofa_Help


class Fofa:
    def __init__(self,config):
        self.config = config
        self.dirs = "config"
        self.historyName = self.dirs +"/fofaHistory.txt"
        self.apiUrl = "https://fofa.info/api/v1/search/all"
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        }
        # 判断爬取结果是否成功
        self.isSuccess = True
        self.thread_list = []


    def init(self,mainWindow,global_ms):
        self.global_ms = global_ms
        self.mainWindow = mainWindow
        self.ui = mainWindow.ui

        # 加载历史记录
        if os.path.exists(self.config.exePath + "/" + self.historyName):
            with open(self.config.exePath + "/" + self.historyName, "r", encoding="utf-8") as f:
                self.ui.comboBox_FOFAMain_HistoryName.addItems(f.readlines())

        # Fofa表格的初始化
        self.fofa_table_init()


        # 历史记录点击事件绑定
        self.ui.comboBox_FOFAMain_HistoryName.activated.connect(self.historyClick)
        # 查询按钮事件绑定
        self.ui.pushButton_FOFAMain_chaxun.clicked.connect(self.chaxun)

        # 语法按钮事件绑定
        self.ui.pushButton_FOFAMain_Syntax.clicked.connect(self.syntax_help)

        # 表格双击绑定事件
        self.ui.tableWidget_FOFAMain_result.doubleClicked.connect(self.fofa_table_doubleclick_to_brower)

        # 导出按钮事件绑定
        self.ui.pushButton_FOFAMain_save.clicked.connect(self.save)

    # fofa表格初始化
    def fofa_table_init(self):
        self.order_list = self.Fofa_Get_Checkbox_Order_List()
        self.order_list_len = len(self.order_list)
        self.ui.tableWidget_FOFAMain_result.setColumnCount(len(self.order_list))
        self.ui.tableWidget_FOFAMain_result.setHorizontalHeaderLabels(self.order_list)

        # 设置默认行高和列宽
        self.ui.tableWidget_FOFAMain_result.horizontalHeader().setDefaultSectionSize(170)
        # 行高
        self.ui.tableWidget_FOFAMain_result.verticalHeader().setDefaultSectionSize(100)

    # 获取 有顺序的checkbox列表
    def Fofa_Get_Checkbox_Order_List(self):
        result = []
        config_temp = self.config.config["fofa"]["save"]
        for number in range(1,len(config_temp) +1):
            if config_temp["host"][1] == number:
                result.append("host")
            elif config_temp["ip"][1] == number:
                result.append("ip")
            elif config_temp["port"][1] == number:
                result.append("port")
            elif config_temp["title"][1] == number:
                result.append("title")
            elif config_temp["domain"][1] == number:
                result.append("domain")
            elif config_temp["country"][1] == number:
                result.append("country")
            elif config_temp["country_name"][1] == number:
                result.append("country_name")
            elif config_temp["city"][1] == number:
                result.append("city")
            elif config_temp["header"][1] == number:
                result.append("header")
            elif config_temp["server"][1] == number:
                result.append("server")
            elif config_temp["protocol"][1] == number:
                result.append("protocol")
            elif config_temp["banner"][1] == number:
                result.append("banner")
            elif config_temp["cert"][1] == number:
                result.append("cert")
            elif config_temp["province"][1] == number:
                result.append("province")

        return result

    def chaxun(self):
        self.clear_FofaResult()
        self.fofa_table_init()
        # 获取key和email
        if "email" in self.config.config["fofa"]:# and self.config.config["fofa"]["email"] != "":
            email = self.config.config["fofa"]["email"].strip()
        else:
            self.messagebox_Warning("请设置email!")
            return
        if "key" in self.config.config["fofa"] and self.config.config["fofa"]["key"] != "":
            key = self.config.config["fofa"]["key"].strip()
        else:
            self.messagebox_Warning("请设置key!")
            return


        # 查询语句
        q = self.ui.lineEdit_FOFAMain_url.text().strip()
        if q == "":
            return
        # 历史记录
        if not os.path.exists(self.config.exePath + "/" + self.historyName):
            open(self.config.exePath + "/" + self.historyName, 'w').close()
        with open(self.config.exePath + "/" + self.historyName, "r+", encoding="utf-8") as f:
            if q+"\n" not in f.readlines():
                f.write(q + "\n")


        # 获取要查询多少条
        size = int(self.ui.spinBox_FOFAMain_OnePageNum.value())
        # 每页固定100条，
        size_immobilization = 100
        # 计算页数
        if size % size_immobilization == 0:
            pageNum = int(size / 100)
        else:
            pageNum = int(size / 100) + 1
            # pageNum = self.ui.spinBox_FOFAMain_PageNum.value()
        # 添加队列
        self.q = queue.Queue()
        for i in range(1,pageNum+1):
            if size > 100:
                size = size - 100
            else:
                size_immobilization = size
            self.q.put({
                "email":email,
                "key":key,
                "full": "true" if self.ui.checkBox_FOFAMain_GetAllData.isChecked() else "false",
                "page":i, # 多少页
                "size": size_immobilization,
                "qbase64":b64encode(q.encode()).decode(),
                "fields":",".join(self.Fofa_Get_Checkbox_Order_List())
            })
        # 获取线程数量
        thread_num = self.ui.spinBox_FOFAMain_ThreadNum.value()
        # 开启线程.
        for i in range(thread_num):
            t = threading.Thread(target=self.chaxun_thread)
            self.thread_list.append(t)
            t.start()
            time.sleep(0.1)

        # 设置按钮不可点击
        self.ui.pushButton_FOFAMain_chaxun.setEnabled(False)
        # 监测线程是否执行完毕
        threading.Thread(target=self.thread_is_die).start()


    # 判断线程是否全部结束
    def thread_is_die(self):
        while True:
            flag = True
            for i in self.thread_list:
                if i.isAlive() == True:
                    flag = False
            if flag:
                break

        self.ui.pushButton_FOFAMain_chaxun.setEnabled(True)
        if self.isSuccess:
            self.mainWindow.statusBar_showMessage("[+] 爬取完成！")


    def chaxun_thread(self):
        while not self.q.empty():
            data = self.q.get()
            self.mainWindow.statusBar_showMessage("[+] 正在爬取第" + str(data["page"]) + "页...")
            html = requests.get(self.apiUrl, params=data, headers=self.header, timeout=10)
            try:
                self.fofa_result(json.loads(html.text))
            except json.decoder.JSONDecodeError as pp:
                if html.status_code == 503:
                    self.q.put(data)
            except Exception as p:
                self.mainWindow.statusBar_showMessage(str(p))
                self.isSuccess = False


    # 将结果插入到gui中
    def fofa_result(self,result):
        # 如果访问错误，则显示错误信息
        # print(result)
        if result["error"] == True:
            self.isSuccess = False
            if "401 Unauthorized, make sure 1.email and apikey is correct" in result["errmsg"]:
                self.mainWindow.statusBar_showMessage("[-] email 或 key错误！")
                return False
            else:
                self.mainWindow.statusBar_showMessage("[-] "+str(result["errmsg"]))
                return False
        else:
            # 添加到gui中
            for one in result["results"]:
                column = 0
                # 插入一行
                row = self.ui.tableWidget_FOFAMain_result.rowCount()
                self.ui.tableWidget_FOFAMain_result.insertRow(row)
                # 每一列插入数据
                if self.order_list_len == 1:
                    if self.order_list[0] == "host":
                        if not one.startswith("http"):
                            one = "http://"+one
                        self.ui.tableWidget_FOFAMain_result.resizeColumnToContents(0)
                    item = QtWidgets.QTableWidgetItem(str(one))
                    self.ui.tableWidget_FOFAMain_result.setItem(row, 0, item)
                else:
                    for i in range(self.order_list_len):

                        item = QtWidgets.QTableWidgetItem(str(one[i]))
                        self.ui.tableWidget_FOFAMain_result.setItem(row, i, item)
            
    def save(self):
        try:
            filename, rel = QtWidgets.QFileDialog.getSaveFileName(self.mainWindow, "导出数据", ".", "TXT(*.txt);;CSV(*.csv)")

            file = open(filename, "w",encoding="utf-8")

            save_option = self.config.config["fofa"]["save"]

            rowCount = self.ui.tableWidget_FOFAMain_result.rowCount()
            columnCount = self.ui.tableWidget_FOFAMain_result.columnCount()
            for row in range(rowCount):
                one_row = ""
                for column in range(columnCount):
                    if self.order_list_len != 1:
                        one_row += self.ui.tableWidget_FOFAMain_result.item(row, column).text().strip() + ","
                    else:
                        one_row += self.ui.tableWidget_FOFAMain_result.item(row, column).text().strip()
                file.write(one_row + "\n")
            self.messagebox_About("保存成功！")
            file.close()
        except:
            pass


    def fofa_table_doubleclick_to_brower(self):
        order_list = self.Fofa_Get_Checkbox_Order_List()
        index = order_list.index("host")
        row = self.ui.tableWidget_FOFAMain_result.selectedItems()[0].row()  # 获取选中文本所在的行
        url = self.ui.tableWidget_FOFAMain_result.item(row,index).text()       #获取选中文本内容
        # 打开浏览器
        GlobalC.brower_open(url)


    def syntax_help(self):
        self.chile_Win = Fofa_help()
        self.chile_Win.show()
        self.chile_Win.exec_()

    def exit(self):
        self.chile_Win.close()

    def messagebox_Warning(self, msg):
        QtWidgets.QMessageBox.warning(self.mainWindow, "警告", msg)

    def messagebox_About(self, msg):
        QtWidgets.QMessageBox.about(self.mainWindow, "提示", msg)

    def historyClick(self):
        self.ui.lineEdit_FOFAMain_url.setText(self.ui.comboBox_FOFAMain_HistoryName.currentText())

    def clear_FofaResult(self):
        self.ui.tableWidget_FOFAMain_result.clearContents()
        self.ui.tableWidget_FOFAMain_result.setRowCount(0)


class Fofa_help(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui = Ui_Fofa_Help()
        # 初始化界面
        self.ui.setupUi(self)

        # 设置窗口置顶，只能每次在fofa_help.py上改
        # Fofa_Help.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # 设置默认行高和列宽
        # 自定义列宽

        self.ui.tableWidget_FOFA_Help.horizontalHeader().setDefaultSectionSize(220)
        # 行高
        self.ui.tableWidget_FOFA_Help.verticalHeader().setDefaultSectionSize(50)


        # 添加数据
        self.addHelpData()

    def addHelpData(self):
        self.header = ["例句", "用途说明", "注"]
        # 添加两列
        self.ui.tableWidget_FOFA_Help.setColumnCount(len(self.header))
        self.ui.tableWidget_FOFA_Help.setHorizontalHeaderLabels(self.header)

        data = [['title="beijing"', '从标题中搜索“北京”', '-'], ['header="elastic"', '从http头中搜索“elastic”', '-'],
         ['body="网络空间测绘"', '从html正文中搜索“网络空间测绘”', '-'], ['domain="qq.com"', '搜索根域名带有qq.com的网站。', '-'],
         ['icp="京ICP证030173号"', '查找备案号为“京ICP证030173号”的网站', '搜索网站类型资产'],
         ['js_name="dojo.js"', '查找网站正文中包含dojo.js的资产', '搜索网站类型资产'],
         ['js_md5="05e51b1db558320f1939f9789ccf5c8f"', 'js内容为“05e51b1db558320f1939f9789ccf5c8f”的资产', '搜索网站类型资产'],
         ['icon_hash="-247388890"', '搜索使用此icon的资产。', '仅限FOFA高级会员使用'],
         ['host=".gov.cn"', '从url中搜索”.gov.cn”', '搜索要用host作为名称'], ['port="6379"', '查找对应“6379”端口的资产', '-'],
         ['ip="1.1.1.1"', '从ip中搜索包含“1.1.1.1”的网站', '搜索要用ip作为名称'],
         ['ip="220.181.111.1/24"', '查询IP为“220.181.111.1”的C网段资产', '-'], ['status_code="402"', '查询服务器状态为“402”的资产', '-'],
         ['protocol="quic"', '查询quic协议资产', '搜索指定协议类型(在开启端口扫描的情况下有效)'], ['country="CN"', '搜索指定国家(编码)的资产。', '-'],
         ['region="Xinjiang"', '搜索指定行政区的资产。', '-'], ['city="Ürümqi"', '搜索指定城市的资产。', '-'],
         ['cert="baidu"', '搜索证书(https或者imaps等)中带有baidu的资产。', '-'],
         ['cert.subject="OracleCorporation"', '搜索证书持有者是OracleCorporation的资产', '-'],
         ['cert.issuer="DigiCert"', '搜索证书颁发者为DigiCertInc的资产', '-'],
         ['cert.is_valid=true', '验证证书是否有效，true有效，false无效', '仅限FOFA高级会员使用'],
         ['banner=users&&protocol=ftp', '搜索FTP协议中带有users文本的资产。', '-'],
         ['type=service', '搜索所有协议资产，支持subdomain和service两种。', '搜索所有协议资产'], ['os="centos"', '搜索CentOS资产。', '-'],
         ['server=="Microsoft-IIS/10"', '搜索IIS10服务器。', '-'],
         ['app="Microsoft-Exchange"', '搜索Microsoft-Exchange设备', '-'],
         ['after="2017"&&before="2017-10-01"', '时间范围段搜索', '-'], ['asn="19551"', '搜索指定asn的资产。', '-'],
         ['org="Amazon.com,Inc."', '搜索指定org(组织)的资产。', '-'], ['base_protocol="udp"', '搜索指定udp协议的资产。', '-'],
         ['is_fraud=false', '排除仿冒/欺诈数据', '-'], ['is_honeypot=false', '排除蜜罐数据', '仅限FOFA高级会员使用'],
         ['is_ipv6=true', '搜索ipv6的资产', '搜索ipv6的资产,只接受true和false。'],
         ['is_domain=true', '搜索域名的资产', '搜索域名的资产,只接受true和false。'], ['port_size="6"', '查询开放端口数量等于"6"的资产', '仅限FOFA会员使用'],
         ['port_size_gt="6"', '查询开放端口数量大于"6"的资产', '仅限FOFA会员使用'],
         ['port_size_lt="12"', '查询开放端口数量小于"12"的资产', '仅限FOFA会员使用'],
         ['ip_ports="80,161"', '搜索同时开放80和161端口的ip', '搜索同时开放80和161端口的ip资产(以ip为单位的资产数据)'],
         ['ip_country="CN"', '搜索中国的ip资产(以ip为单位的资产数据)。', '搜索中国的ip资产'],
         ['ip_region="Zhejiang"', '搜索指定行政区的ip资产(以ip为单位的资产数据)。', '搜索指定行政区的资产'],
         ['ip_city="Hangzhou"', '搜索指定城市的ip资产(以ip为单位的资产数据)。', '搜索指定城市的资产'],
         ['ip_after="2021-03-18"', '搜索2021-03-18以后的ip资产(以ip为单位的资产数据)。', '搜索2021-03-18以后的ip资产']]
        # 添加到gui中
        for one in data:
            column = 0
            # 插入一行
            row = self.ui.tableWidget_FOFA_Help.rowCount()
            self.ui.tableWidget_FOFA_Help.insertRow(row)
            for i in one:
                # 每一列插入数据
                item = QtWidgets.QTableWidgetItem(str(i))
                self.ui.tableWidget_FOFA_Help.setItem(row, column, item)
                column += 1




