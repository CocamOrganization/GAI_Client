import sys
# PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
# 导入designer工具生成的login模块
from Gui.crawler_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui
from Spider import main_spider
import os
# import Word_Statis

# getter = Getter.Getter()
# cal_words = Word_Statis.Cal_Words()


class EmittingStr(QtCore.QObject):
        textWritten = QtCore.pyqtSignal(str)  #定义一个发送str的信号
        def write(self, text):
            self.textWritten.emit(str(text))


class MyMainForm(Ui_MainWindow):
    def __init__(self):
        super(MyMainForm, self).__init__()
        self.setupUi(self)
        self.resize(1000, 800)
        self.pushButton.clicked.connect(self.start_crawl)

    def console_desplay(self, str):
        '''
        信号自定义槽函数
        :param str:用于将信号函数中的str传递给textbrowser
        :return:
        '''
        self.textBrowser.append(str)

    def msg(self):
        # QFileDialog.getExistingDirectory(self, "请选择保存的文件夹路径", "C:\\Users\\86178\\Desktop")
        file_path = QFileDialog.getExistingDirectory(self, "请选择保存的文件夹路径", "C:\\Users\\86178\\Desktop")  # 返回选中的文件夹路径
        return file_path

    def start_crawl(self):
        if self.textEdit.document().isEmpty():
            self.console_desplay('请先输入关键词')
        else:
            file_path = self.msg()
            # print(file_path)
            inputs = self.textEdit.toPlainText()
            all_need_crawl = inputs.split('\n')
            self.spider = main_spider.all_title_spider(all_need_crawl, file_path)
            self.spider.signal.connect(self.console_desplay)  # 将信号与槽函数链接
            self.spider.start()




if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())

