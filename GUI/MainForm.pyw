# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 11:34:28 2015

@author: Binoy
"""

#from PySide.QtCore import *
#from PySide import QtGui

from PyQt4 import QtGui
from PyQt4.QtCore import *
import os, subprocess
from ui_MainForm import Ui_MainWindow 
from ui_Settings import Ui_frmSettings
from ui_dlgOutput import Ui_dlgOut
import shutil
 
class settings(QtGui.QDialog, Ui_frmSettings):
    """
    Settings widget
    """
    def __init__(self):
        

        super(settings, self).__init__()
        if self.checkFiles(): return 
        
        self.setupUi(self)
        self.cmdOk.clicked.connect(self.accept)
        self.exec_()

        
    
    def checkFiles(self):
        cwd = os.getcwd()
        bpath = os.path.exists(os.path.join(cwd,'sflow.path'))

        if bpath:
            spath = os.path.join(cwd,'sflow.path')
            _fylSflow = open(spath,'r')
            self.sflowpath = _fylSflow.read()
            _fylSflow.close()
            print self.sflowpath
            if not os.path.exists(self.sflowpath):
                return 0 
            else:
                return 1
                
    @pyqtSignature("")
    def on_cmd_sflow_clicked(self):
        sflow_path = QtGui.QFileDialog.getOpenFileName(self, \
        caption = "Browse for shipflow bat file")
        
        if os.path.exists(sflow_path):
            self.wid_le_sflow.setText(sflow_path)
            self.sflowpath = sflow_path
            cwd = os.getcwd()
            spath = os.path.join(cwd,'sflow.path')
            _fylSflow = open(spath,'w')
            _fylSflow.write(self.sflowpath)
            _fylSflow.close()
            
    def returnValues(self):
        return self.sflowpath
        
class viewOutput(QtGui.QDialog, Ui_dlgOut):
    """
    View output file4
    """
    def __init__(self, fpath):
        super(viewOutput, self).__init__()
        self.setupUi(self)
        try:
            
            f = open(fpath, 'r')
            
            for line in f:
                self.plainTextEdit.appendPlainText(line.strip())
            f.close()
            self.wid_lbl_fname.setText(fpath)
            self.wid_le_saveas.setText(fpath)
        except Exception as e:
            self.plainTextEdit.appendPlainText("Error in file open" + str(e))
            self.cmdSave.setEnabled(0)
            
    @pyqtSignature("")
    def on_cmdSave_clicked(self):
        msgbox = QtGui.QMessageBox(self)
        text = self.plainTextEdit.toPlainText()
        try:
            f = open(str(self.wid_le_saveas.text()), 'w')
            for line in text.split('\n'):
                f.write(line +'\n')
            f.close()
            msgbox.setWindowTitle("Success")
            msgbox.setText("File Save")
            msgbox.setDetailedText(self.wid_le_saveas.text())
           
        except Exception as e:
            
            msgbox.setWindowTitle("Failed")
            msgbox.setText(e.message)
            
        msgbox.show()
        msgbox.exec_()   
        

        
class mainWin(QtGui.QMainWindow, Ui_MainWindow):
    """
    Main Window class
    """
    writesig = pyqtSignal(str) 
    def __init__(self):
        """"
        Initialization
        """
        super(mainWin, self).__init__()
        self.setupUi(self)
        self.statusbar.showMessage("Good Day -- Binoy", 0)
        self.wid_lstConfigfiles.setContextMenuPolicy(Qt.CustomContextMenu)
        
        
        # Qmenu settings
        self.listMenu= QtGui.QMenu()
        self.menu_rem = self.listMenu.addAction("Remove config file.")
        self.menu_runthis = self.listMenu.addAction("Run this config file.")
        self.menu_openresult = self.listMenu.addAction("Show Result")
        self.menu_viewfile = self.listMenu.addAction("View File")
        self.menu_clean = self.listMenu.addAction("Clean Output")
        self.connect(self.wid_lstConfigfiles, SIGNAL("customContextMenuRequested(QPoint)" ),\
        self.listItemRightClicked)
        self.connect(self.menu_runthis, SIGNAL("triggered()"), self.on_menu_runthis_triggered) 
        self.connect(self.menu_rem, SIGNAL("triggered()"), self.on_wid_btnRemfile_clicked)
        self.connect(self.menu_openresult, SIGNAL("triggered()"), self.on_menu_showresult_triggered)
        self.connect(self.menu_viewfile, SIGNAL("triggered()"), self.on_menu_viewfile_triggered)
        self.connect( self.menu_clean, SIGNAL("triggered()"), self.cleanSflowfile)
        
        ## Initial path readings
        dlg_setting = settings()
        self.sflowpath = dlg_setting.sflowpath
        
        ## Custom Signal
    
        self.writesig.connect(self.appendtole)
        
    def getFile(self):
        fpath = QtGui.QFileDialog.getOpenFileNames(self, 'Open file',
                    os.getcwd())
        return fpath
        
        
    def listItemRightClicked(self, QPos):
        if self.wid_lstConfigfiles.count()==0:
            self.listMenu.setDisabled(1)
            
        else:
#        self.connect(menu_item, SIGNAL("triggered()"), self.menuItemClicked) 
    
            parentPosition = self.wid_lstConfigfiles.mapToGlobal(QPoint(0, 0))   
            self.listMenu.setDisabled(0)
            self.listMenu.move(parentPosition + QPos)
            self.listMenu.show() 
        
    @pyqtSignature("")
    def on_wid_btnAddfile_clicked(self):
        files = self.getFile()
        for f in files:
            self.wid_lstConfigfiles.addItem(f)
        
    @pyqtSignature("")
    def on_wid_btnRemfile_clicked(self):
        currentItem = self.wid_lstConfigfiles.currentItem()
        print currentItem.text()
        self.wid_lstConfigfiles.takeItem(self.wid_lstConfigfiles.row(currentItem))
        
    @pyqtSignature("")
    def on_cmdRun_clicked(self):
        
        if self.wid_Chkbatchrun.isChecked():
            self.batchRun()
        else:
            self.on_menu_runthis_triggered()
            
    @pyqtSignature("")
    def on_cmdClearout_clicked(self):
        self.wid_Txtout.clear()
    
            
    @pyqtSlot(str)
    def appendtole(self, line):
        self.wid_Txtout.appendPlainText(line)
        QtGui.QApplication.processEvents()
    

    def on_menu_runthis_triggered(self):
        currentItem = self.wid_lstConfigfiles.currentItem()
#        self.writesig.emit("s")
#        print currentItem.text()
        self.runSflow(str(currentItem.text()))
        
    def on_menu_showresult_triggered(self):
        currentItem = self.wid_lstConfigfiles.currentItem()
        p = str(currentItem.text())
        curdir = os.path.dirname(p)
        curfile = os.path.basename(p)
        resfolder = curfile + "_RUN_DIR"
        resfile = curfile + "_OUTPUT"

        out_fpath = os.path.join(curdir, resfolder, resfile)
        dispres = viewOutput(out_fpath)
        dispres.setWindowTitle(resfile)
        dispres.show()
        dispres.exec_()
    
    def on_menu_viewfile_triggered(self):
        currentItem = self.wid_lstConfigfiles.currentItem()
        p = str(currentItem.text())
        dispres = viewOutput(p)
        dispres.setWindowTitle(p)
        dispres.show()
        dispres.exec_()
    
    def batchRun(self):
        if self.wid_lstConfigfiles.count()>0:
            for i in range(self.wid_lstConfigfiles.count()):
                currentitem = self.wid_lstConfigfiles.item(i)
                self.runSflow(str(currentitem.text()))
        
    
    def runSflow(self, path=None):

        SFLOW = self.sflowpath
        _dir = os.path.dirname(path)
        
        os.chdir(_dir)
        
        
        cmd = SFLOW + ' -c ' + path
        self.wid_Txtout.appendPlainText("Running the command:\n"+cmd+"\n")
        pr = subprocess.Popen(cmd,shell= 1, stdout = subprocess.PIPE)
        
        
        for line in iter(pr.stdout.readline, b''):
            print line
            self.writesig.emit(line.strip())
        pr.stdout.close()
        pr.wait()
    
    def cleanSflowfile(self):
        currentItem = self.wid_lstConfigfiles.currentItem()
        p = str(currentItem.text())
        curdir = os.path.dirname(p)
        curfile = os.path.basename(p)
        
        resfolder = os.path.join(curdir, curfile + "_RUN_DIR")
        
        repfolder = os.path.join(curdir, curfile + "_REPORT")
        cgns_file = p + ".cgns"
        output_file = p + "_OUTPUT"
        res = ""
        details = ""
        try:
            if os.path.exists(resfolder):
                shutil.rmtree(resfolder)
            else:
                details += "No OUTPUT folder\n"
            if os.path.exists(repfolder): 
                shutil.rmtree(repfolder)
            else:
                details += "No Report folder\n"
        
        except Exception as e:
            res += str(e)+'\n'
        try:
            os.remove(cgns_file)
            os.remove(output_file)
        except Exception as e:
            res += str(e)+'\n'
            details += "No output files deleted\n"
        msgbox = QtGui.QMessageBox(self)
        if res:
            msgbox.setText(res)
            
        else: msgbox.setText("Cleansed")
        msgbox.setDetailedText(details)
        msgbox.setWindowTitle("ShipFlow Clean results")
        msgbox.show()
        msgbox.exec_()
#        while True:
#          line = pr.stdout.readline()
#          print line
#          self.writesig.emit(line)
##          self.wid_Txtout.appendPlainText(line.strip())
#          if not line: 
#              self.wid_Txtout.appendPlainText("Run Finished")
#              break

        
        
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)    
    app.setStyle("Cleanlooks")
    window = mainWin()

    window.show()
    r = app.exec_()
    r = raw_input("Hit enter")