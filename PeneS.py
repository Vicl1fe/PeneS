from PyQt5 import QtWidgets
from PyQt5.QtGui import  QIcon
from PyQt5.QtCore import pyqtSignal,QObject
from ui_main import Ui_MainWindow
from Module.setting import Setting
from Module.Google import Google
from Module.Fofa import Fofa
from Module.Config import Config
from sys import exit

config = Config()
module_dict = {
    "Google":Google(config),
    "Fofa":Fofa(config)
}

# 自定义信号源对象类型，一定要继承自 QObject
class MySignals(QObject):

    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    # text_print = pyqtSignal(str)
    # clear_GoogleHackTable = pyqtSignal(str)
    messagebox_Warning = pyqtSignal(str)
global_ms = MySignals()

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self,config):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui = Ui_MainWindow()
        # 初始化界面
        self.ui.setupUi(self)

        # 信号处理
        # global_ms.text_print.connect(self.Google_getGoogleHack)


        # self.menu_setting.triggered.connect()
        # 初始化一些参数
        for module in module_dict:
            module_dict[module].init(self,global_ms)


    def statusBar_showMessage(self,msg):
        self.statusBar().showMessage(str(msg))

    def closeEvent(self, event):
        """重写该方法主要是解决打开子窗口时，如果关闭了主窗口但子窗口仍显示的问题，使用sys.exit(0) 时就会只要关闭了主窗口，所有关联的子窗口也会全部关闭"""
        try:
            for module in module_dict:
                module_dict[module].exit()
        except Exception as e:
            pass
if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    mainw = MainWindow(config)
    app.setWindowIcon(QIcon('INI/logo.png'))
    # 将主窗口和子窗口联系起来，不能在父窗口的类中联系起来
    dialog_Setting = Setting(config)
    mainw.ui.action_setting_2.triggered.connect(dialog_Setting.show)
    # self.menu_setting.triggered.connect()
    mainw.show()
    app.exec_()