import sys, os
from PyQt4 import QtCore, QtGui    

class ThumbListWidget(QtGui.QListWidget):
    def __init__(self, type, parent=None):
        super(ThumbListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QtCore.QSize(124, 124))

#    def dragEnterEvent(self, event):
#        if event.mimeData().hasUrls:
#            event.accept()
#        else:
#            event.ignore()
#
#    def dragMoveEvent(self, event):
#        if event.mimeData().hasUrls:
#            event.setDropAction(QtCore.Qt.CopyAction)
#            event.accept()
#        else:
#            event.ignore()
#
#    def dropEvent(self, event):
#        if event.mimeData().hasUrls:
#            event.setDropAction(QtCore.Qt.CopyAction)
#            event.accept()
#            links = []
#            for url in event.mimeData().urls():
#                links.append(str(url.toLocalFile()))
#            self.emit(QtCore.SIGNAL("dropped"), links)
#        else:
#            event.ignore()

class Dialog_01(QtGui.QMainWindow):
    def __init__(self):
        super(QtGui.QMainWindow,self).__init__()
        self.listItems={}

        myQWidget = QtGui.QWidget()
        myBoxLayout = QtGui.QVBoxLayout()
        myQWidget.setLayout(myBoxLayout)
        self.setCentralWidget(myQWidget)

        self.myListWidget = ThumbListWidget(self)  
        self.myListWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.myListWidget.connect(self.myListWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)" ), self.listItemRightClicked)

        myButton = QtGui.QPushButton("Add List Item")

        myBoxLayout.addWidget(self.myListWidget)
        myBoxLayout.addWidget(myButton)
        myButton.clicked.connect(self.addListWidgetItem)                

    def addListWidgetItem(self):
        listItemName='Item '+str(len(self.listItems.keys()))        
        self.listItems[listItemName]=None
        self.rebuildListWidget() 

    def listItemRightClicked(self, QPos): 
        self.listMenu= QtGui.QMenu()
        menu_item = self.listMenu.addAction("Remove Item")
        if len(self.listItems.keys())==0: menu_item.setDisabled(True)
        self.connect(menu_item, QtCore.SIGNAL("triggered()"), self.menuItemClicked) 

        parentPosition = self.myListWidget.mapToGlobal(QtCore.QPoint(0, 0))        
        self.listMenu.move(parentPosition + QPos)

        self.listMenu.show() 

    def menuItemClicked(self):
        if len(self.listItems.keys())==0: print 'return from menuItemClicked'; return
        currentItemName=str(self.myListWidget.currentItem().text() )
        self.listItems.pop(currentItemName, None)
        self.rebuildListWidget()

    def rebuildListWidget(self):
        self.myListWidget.clear()
        items=self.listItems.keys()
        if len(items)>1: items.sort()
        for listItemName in items:
            listItem = QtGui.QListWidgetItem( listItemName, self.myListWidget )
            self.listItems[listItemName]=listItem


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog_1 = Dialog_01()
    dialog_1.show()
    dialog_1.resize(480,320)
    sys.exit(app.exec_())