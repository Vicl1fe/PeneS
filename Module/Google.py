from PyQt5 import QtWidgets
import requests
from threading import Thread
import json
import re
import os
import queue
from bs4 import BeautifulSoup

class Google:
    def __init__(self,config):
        self.config = config
        # QHeaderView.
        # exploit-db 的google hakc爬取页数
        # self.GoogleHackNum = 2
        dirs = "config"
        self.GoogleHackCachFileName = dirs + "/GoogleHackCache.json"
        # 历史记录文件
        self.historyName = dirs + "/googleHistory.txt"
        # 线程列表
        self.thread_list = []
        # 请求头
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        }
        self.ajaxHeader = {
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        }
        self.isSuccess = False

    def init(self,mainWindow,global_ms,):
        self.mainWindow = mainWindow
        self.ui = mainWindow.ui
        self.global_ms = global_ms
        # 初始化页数
        self.ui.spinBox_GoogleNum.setValue(5)
        # 设置google的列宽
        self.ui.tableWidget_GoogleHack.setColumnWidth(0, 520)
        self.ui.tableWidget_GoogleHackResult.setColumnWidth(0, 350)
        self.ui.tableWidget_GoogleHackResult.setColumnWidth(1, 350)

        # 加载Exploit-db的Google Hack
        if os.path.exists(self.config.exePath + "/" + self.GoogleHackCachFileName):
            # 插入到 QTableWidget
            self.insert_GoogleHacking()
        else:
            self.get_GoogleHacking_Thread()
        # 加载历史记录
        if os.path.exists(self.config.exePath + "/" + self.historyName):
            with open(self.config.exePath + "/" + self.historyName,"r",encoding="utf-8") as f:
                self.ui.comboBox_HistoryHack.addItems(f.readlines())
        # 历史记录点击事件绑定
        self.ui.comboBox_HistoryHack.activated.connect(self.historyClick)
        # 查询按钮绑定事件
        self.ui.pushbutton_chaxun.clicked.connect(self.googleSpider_1_re)
        # 给GoogleHack 表格绑定点击事件
        self.ui.tableWidget_GoogleHack.clicked.connect(self.GoogleHackClick)
        # 刷新按钮绑定点击事件
        self.ui.pushButton_flush.clicked.connect(self.get_GoogleHacking_Thread)
        # 警告弹窗信号
        self.global_ms.messagebox_Warning.connect(self.messagebox_Warning)

        # 导出按钮点击事件
        self.ui.pushButton_save.clicked.connect(self.saveData)

        # 状态栏
        self.mainWindow.statusBar_showMessage("[+] 准备就绪。")

    def historyClick(self):
        self.ui.lineedit_url.setText(self.ui.comboBox_HistoryHack.currentText())

    def messagebox_Warning(self, msg):
        QtWidgets.QMessageBox.warning(self.mainWindow, "警告", msg)

    def messagebox_About(self, msg):
        QtWidgets.QMessageBox.about(self.mainWindow, "提示", msg)

    # 获取exploit-db中的googlehack
    def get_GoogleHacking(self,page = 0):
        # 清空表格
        self.clear_GoogleHackTable()
        filename = self.config.exePath + "/" + self.GoogleHackCachFileName
        #
        proxy = ""
        if "proxy" in self.config.config["google"]:
            if self.config.config["google"]["proxy"] != "":
                proxy = self.config.config["google"]["proxy"]
                proxies = {"http": proxy, "https": proxy}

        def get_json(page):
            json_url = "https://www.exploit-db.com/google-hacking-database?draw={}&columns%5B0%5D%5Bdata%5D=date&columns%5B0%5D%5Bname%5D=date&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=url_title&columns%5B1%5D%5Bname%5D=url_title&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=cat_id&columns%5B2%5D%5Bname%5D=cat_id&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=author_id&columns%5B3%5D%5Bname%5D=author_id&columns%5B3%5D%5Bsearchable%5D=false&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=desc&start={}&length=120&search%5Bvalue%5D=&search%5Bregex%5D=false&author=&category=&_=1596415372353".format(
                page, (page - 1) * 120)
            if proxy == "":
                return requests.get(json_url, headers=self.ajaxHeader).text
            else:
                return requests.get(json_url, headers=self.ajaxHeader,proxies=proxies).text


        # 获取所有json数据，page为获取多少页。
        def get_Alljson(page):
            all_json = []
            for i in range(1, page + 1):
                self.mainWindow.statusBar_showMessage("[+] 正在爬取第" + str(i) + "页...")
                all_json.append(get_json(i))
            return all_json

        def json_parse(all_json):
            # 定义好字典,和子字典
            all_data = []
            all_data_one = {}
            for one_json in all_json:
                one_data = json.loads(one_json)
                for j in range(0, len(one_data['data'])):
                    # print(one_data['data'][j]['url_title'])
                    all_data_one['date'] = one_data['data'][j]['date']
                    url_title = re.search("<a (.*?)>(.*?)</a>", one_data['data'][j]['url_title'])
                    all_data_one['url_title'] = url_title.groups()[1]
                    # 修改all_data_one字典相当于修改了内存地址的值，循环修改的是同一个变量,所以导致列表中所有的字典相同。因为循环添加的是就是同一款内存地址的值。虽然一直在修改字典的值，但是内存地址没变
                    # 需要重新定义一个变量all_data_one，这两个变量不是同一个内存地址
                    all_data.append(all_data_one)
                    all_data_one = {}
            # 去重后整合为字典
            return all_data

        def saveJson(data):
            result = {}
            # 计数
            count = 0
            for i in data:
                result[count] = i
                count += 1
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(json.dumps(result))

        try:
            # 获取所有json数据
            all_json = get_Alljson(int(self.ui.spinBox_GoogleHackNum.text()))
            # 将所有json数据解析为字典并提取关键数据
            all_data = json_parse(all_json)
            self.mainWindow.statusBar_showMessage("[+] 爬取成功。")
            # 保存数据
            saveJson(all_data)
            self.mainWindow.statusBar_showMessage("[+] 保存成功。")
        except Exception as e:
            # self.messagebox_warning(str(e))
            self.global_ms.messagebox_Warning.emit(str(e))
        # 插入到gui表格中
        self.insert_GoogleHacking()

    def get_GoogleHacking_Thread(self):
        t = Thread(target=self.get_GoogleHacking)
        t.start()

    # 下拉框点击事件，将文本赋值给输入框
    def GoogleHackClick(self):
        currentrow = self.ui.tableWidget_GoogleHack.currentRow()
        self.ui.lineedit_url.setText(self.ui.tableWidget_GoogleHack.item(currentrow, 0).text())

    # expdb中的googlehack插入到gui的表格中
    def insert_GoogleHacking(self):
        if os.path.exists(self.config.exePath + "/" + self.GoogleHackCachFileName):
            with open(self.config.exePath + "/" + self.GoogleHackCachFileName, 'r', encoding='utf-8') as f:
                all_data = json.loads(f.readline().strip())
                for i in range(len(all_data)):
                    column = 0
                    item = all_data[str(i)]
                    row = self.ui.tableWidget_GoogleHack.rowCount()
                    # 插入一行
                    self.ui.tableWidget_GoogleHack.insertRow(row)
                    # 给插入的行添加第一列数据
                    item = QtWidgets.QTableWidgetItem(str(all_data[str(i)]["url_title"]))
                    self.ui.tableWidget_GoogleHack.setItem(row, column, item)
                    column += 1
                    # 给插入的行添加第二列数据
                    item = QtWidgets.QTableWidgetItem(str(all_data[str(i)]["date"]))
                    self.ui.tableWidget_GoogleHack.setItem(row, column, item)


    def clear_GoogleHackTable(self):
        self.ui.tableWidget_GoogleHack.clearContents()
        self.ui.tableWidget_GoogleHack.setRowCount(0)


    def googleSpider_1_re(self):


        self.clear_GoogleHackResult()
        if "proxy" in self.config.config["google"]:
            self.proxy = self.config.config["google"]["proxy"]
        else:
            self.messagebox_Warning("请设置代理！")
            return
        url = "https://www.google.com/search?q={}&start={}"
        # 队列
        self.que_ue = queue.Queue()
        # 查询语句
        q = self.ui.lineedit_url.text()
        # 历史记录,创建文件
        if not os.path.exists(self.config.exePath + "/" + self.historyName):
            open(self.config.exePath + "/" + self.historyName, 'w').close()
        with open(self.config.exePath + "/" + self.historyName, "r+", encoding="utf-8") as f:
            if q not in f.readlines():
                f.write(q+"\n")
        # 页数
        pageNum = self.ui.spinBox_GoogleNum.text()
        for num in range(int(pageNum)):
            self.que_ue.put(url.format(q,10*num))

        self.mainWindow.statusBar_showMessage("[+] 正在爬取中...")
        # 线程数量
        for num in range(1,int(pageNum)+1):
            self.mainWindow.statusBar_showMessage("[+] 正在爬取第"+str(num)+"页")
            t = Thread(target=self.googleSpider_thread)
            self.thread_list.append(t)
            t.start()

        # 设置按钮不可点击
        self.ui.pushbutton_chaxun.setEnabled(False)
        # 判断线程是否结束
        Thread(target=self.thread_is_die).start()

    def thread_is_die(self):
        while True:
            flag = True
            for i in self.thread_list:
                if i.isAlive() == True:
                    flag = False
            if flag:
                self.isSuccess = True
                break
        self.ui.pushbutton_chaxun.setEnabled(True)
        if self.isSuccess:
            self.mainWindow.statusBar_showMessage("[+] 爬取完成！")
    def googleSpider_thread(self):
        try:
            while not self.que_ue.empty():
                url = self.que_ue.get()

                result = {}
                proxies = {"http":self.proxy,"https":self.proxy}
                html = requests.get(url,proxies=proxies,headers=self.header)
                if "Our systems have detected unusual traffic from your computer network." in html.text:
                    self.mainWindow.statusBar_showMessage("[-] 检测到IP已被封禁！请更换节点！")
                    return
                soup = BeautifulSoup(html.text, "lxml")
                resultTitle = re.findall(r"<h3 class=\"LC20lb DKV0Md\">(.*?)</h3>", html.text)
                resultUrl = re.findall(r"<div class=\"yuRUbf\"><a href=\"(.*?)\" data-ved", html.text)

                for i in resultUrl:
                    for j in range(len(resultTitle)):
                        result[i] = resultTitle[j]

                self.googleSpider_result_re(result)
        except Exception as e:
            self.mainWindow.statusBar_showMessage("[-] "+str(e))
            self.isSuccess = False
            return

    def googleSpider_result_re(self,result):

        for url in result:
            column = 0
            # 插入一行
            row = self.ui.tableWidget_GoogleHackResult.rowCount()
            self.ui.tableWidget_GoogleHackResult.insertRow(row)
            # 给插入的行添加第一列数据
            item = QtWidgets.QTableWidgetItem(str(url))
            self.ui.tableWidget_GoogleHackResult.setItem(row, column, item)
            column += 1
            # 给插入的行添加第二列数据
            item = QtWidgets.QTableWidgetItem(str(result[url]))
            self.ui.tableWidget_GoogleHackResult.setItem(row, column, item)

    def clear_GoogleHackResult(self):
        self.ui.tableWidget_GoogleHackResult.clearContents()
        self.ui.tableWidget_GoogleHackResult.setRowCount(0)

    def saveData(self):
        try:
            filename, rel = QtWidgets.QFileDialog.getSaveFileName(self.mainWindow, "导出数据", ".", "TXT(*.txt)")
            file = open(filename, "w", encoding="utf-8")

            rowCount = self.ui.tableWidget_GoogleHackResult.rowCount()
            for row in range(rowCount):
                urlResult = self.ui.tableWidget_GoogleHackResult.item(row, 0).text()
                file.write(urlResult + "\n")
            self.messagebox_About("保存成功！")
            file.close()
        except:
            pass
            # self.messagebox_Warning("没有选择保存的文件！")

    def exit(self):
        pass