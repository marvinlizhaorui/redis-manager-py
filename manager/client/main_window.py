#!/usr/bin/python
# -*- coding: UTF-8 -*- 

'''
主窗体
'''

import sys

from PyQt5.QtWidgets import QMainWindow, QTreeView, QTreeWidget, QWidget, QTabWidget, QHBoxLayout, QFrame, QPushButton, QLabel, QLineEdit, QTextEdit, QTableWidget, QAbstractItemView, QTableWidgetItem, QTreeWidgetItem, QAction, QMessageBox, QDesktopWidget, QApplication
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication
import show_window

class ManagerWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 700)
        # 标签页设置
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        # 设置标签页关闭
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabel('数据库')
        self.tree.setMaximumWidth(200)

        self.init_UI()

    def init_UI(self):
        '''
        初始化UI
        '''
        self.init_menubar()
        self.init_UI_body()
        self.resize(1000, 700)
        self.center()
        self.setWindowTitle("Redis Manager")

        # self.set_statusbar('ready')

        #设置icon
        # self.setWindowIcon(QIcon('./icon/redis.png'))
        self.show()

    def init_UI_body(self):
        '''
        初始化窗体内容
        '''
        # 使用网格布局
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)

        self.set_show_tree('链接-1')
        self.set_show_tree('连接-2')
        self.set_show_tree('连接-3')
        self.set_show_tree('连接-4')
        for index in range(10):
            self.create_tab('str' + str(index))

        layout.addWidget(self.tree)
        layout.addWidget(self.tabs)

        self.setCentralWidget(widget)
        self.tree.itemClicked.connect(self.test)

    def create_tab(self, tab_name):
        '''
        创建标签页
        '''
        self.tabs.addTab(tab(), tab_name)

    def close_tab(self, index):
        '''
        关闭标签页
        '''
        if index > -1:
            self.tabs.removeTab(index)

    def set_show_tree(self, title):
        '''
        设置左侧树组件
        '''
        root = QTreeWidgetItem(self.tree)
        root.setText(0, title)
        for i in range(10):
            item = QTreeWidgetItem(root)
            item.setText(0, str(i))
            
            root.addChild(item)

    def test(self, item, column):
        print()

    def init_menubar(self):
        '''
        初始化菜单栏
        '''
        menubar = self.menuBar()

        menu = menubar.addMenu('&connect')
        createConnAct = QAction('&新建连接', self)
        createConnAct.setToolTip('新建连接')
        createConnAct.setShortcut('Ctrl+N')

        menu.addAction(createConnAct)
        delConnAct = QAction('&删除连接', self)
        delConnAct.setToolTip('删除连接')
        delConnAct.setShortcut('Ctrl+D')
        menu.addAction(delConnAct)

        exitAct = QAction('&退出',self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setToolTip("退出客户端")
        exitAct.triggered.connect(self.close)
        menu.addAction(exitAct)

    def set_statusbar(self, msg):
        '''
        设置状态栏
        '''
        self.statusBar().showMessage(msg)

    def closeEvent(self, event):
        '''
        关闭窗口提示
        '''
        replay = QMessageBox.question(self, '提示', '确定退出！！！', QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if replay == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        '''
        将窗口放在屏幕中
        '''
        # 获得这个QT组件的框架位置
        qr = self.frameGeometry()
        # 找到屏幕的中心
        cp = QDesktopWidget().availableGeometry().center()
        # 将这个矩形的中心放在当前这个屏幕的中心
        qr.moveCenter(cp)
        # 将创建的窗口移动
        self.move(qr.topLeft())

class tab(QFrame):
    '''
    详细数据展示面板
    '''

    def __init__(self):
        super().__init__()
        # 设置字号
        self.setFont(QFont('SansSerif', 10))
        self.ttl_btn = QPushButton('set TTL', self)
        self.reload_btn = QPushButton('reload data', self)
        self.del_btn = QPushButton('delete', self)
        self.reset_btn = QPushButton('set value', self)
        self.key_text = QLineEdit(self)
        self.val_text = QTextEdit(self)
        self.data_table = None
        # 选择的列表行索引
        self.row_index = -1
        self.key = None

        self.init_UI()

    def init_UI(self):
        '''
        初始化面板
        '''
        self.set_show_label()
        self.set_key_value()
        self.set_show_btn()
        self.set_show_data()

    def set_show_btn(self):
        '''
        设置展示面板的按钮
        '''
        # 设置TTL
        self.ttl_btn.move(200, 5)
        self.ttl_btn.clicked.connect(self.set_TTL_btn)
        # 刷新数据
        self.reload_btn.move(300, 5)
        self.reload_btn.clicked.connect(self.reload_data)
        # 删除
        self.del_btn.move(400, 5)
        self.del_btn.clicked.connect(self.del_data)
        # 设置值
        self.reset_btn.move(600, 100)
        self.reset_btn.clicked.connect(self.reset_data)

    def set_TTL_btn(self):
        '''
        设置TTL按钮的点击事件
        '''
        win = show_window.TTL(self.key, 'TTL')
        win.exec_()

    def reload_data(self):
        '''
        刷新面板数据
        '''
        # TODO 刷新面板数据
        pass

    def del_data(self, key):
        '''
        删除数据
        '''
        msg = '是否删除该键'
        if (self.row_index == -1):
            msg = '请选择要删除的键'
        replay = QMessageBox.question(self, '提示', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes:
            # TODO 执行删除
            self.data_table.removeRow(self.row_index)
            self.row_index = -1
            self.key = None
            print('执行删除操作')

    def reset_data(self):
        '''
        设置键的值
        '''
        if (self.row_index == -1):
            replay = QMessageBox.question(self, '提示', '请选择需设置的键', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        else:
            win = show_window.TTL(self.key, 'value')
            win.exec_()
            self.row_index = -1
            self.key = None

    def set_show_label(self):
        '''
        设置展示的label
        '''
        # 使用绝对定位添加label
        QLabel('type： ', self).move(5, 10)
        QLabel('String', self).move(40, 10)
        QLabel('TTL : ',self).move(100, 10)
        QLabel('-1', self).move(140, 10)
        QLabel('key： ', self).move(5, 500)
        QLabel('value: ', self).move(5, 540)

    def set_key_value(self):
        '''
        设置键值显示框
        '''
        self.key_text.move(50, 495)
        self.key_text.setFixedWidth(500)

        self.val_text.move(50, 540)
        self.val_text.setFixedWidth(500)
        self.val_text.setFixedHeight(80)

    def set_show_data(self):
        '''
        设置展示数据的列表
        '''
        # 展示数据的Table
        self.data_table = QTableWidget(10, 2, self)
        # 设置表头
        self.data_table.setHorizontalHeaderLabels(['键', '值'])
        self.data_table.move(5, 50)
        self.data_table.setFixedWidth(560)
        self.data_table.setFixedHeight(430)
        # 禁止编辑
        self.data_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 整行选择
        self.data_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置单元格宽度，参数： （单元格索引， 宽度）
        self.data_table.setColumnWidth(0, 267)
        self.data_table.setColumnWidth(1, 267)

        # 添加数据
        for col in range(2):
            for row in range(10):
                self.data_table.setItem(row, col, QTableWidgetItem(str(col) +' : ' + str(row)))

        self.data_table.currentItemChanged.connect(self.show_item_data)

    def show_item_data(self, item):
        '''
        展示键值对数据
        '''
        index = self.data_table.currentRow()
        self.row_index = index
        key_item = self.data_table.item(index, 0)
        val_item = self.data_table.item(index, 1)
        self.key_text.setText(key_item.data(0))
        self.val_text.setPlainText(val_item.data(0))
        self.key = key_item.data(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ManagerWindow()
    sys.exit(app.exec_())