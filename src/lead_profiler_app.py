# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LeadProfiler.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from .lead_profile import LeadProfile

class LeadProfilerApp(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 1200)
        MainWindow.setMouseTracking(False)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 1031, 111))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        
        self.labelPreName = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelPreName.setObjectName("labelPreName")
        self.gridLayout.addWidget(self.labelPreName, 0, 0, 1, 1)
        
        self.labelTopic = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelTopic.setObjectName("labelTopic")
        self.gridLayout.addWidget(self.labelTopic, 2, 0, 1, 1)
        
        self.LeadCompany = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.LeadCompany.setObjectName("LeadCompany")
        self.gridLayout.addWidget(self.LeadCompany, 0, 5, 1, 1)
        
        self.progressBar = QtWidgets.QProgressBar(self.gridLayoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 2, 5, 1, 1)
        
        self.LeadPreName = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.LeadPreName.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.LeadPreName.setObjectName("LeadPreName")
        self.gridLayout.addWidget(self.LeadPreName, 0, 1, 1, 1)
        
        self.LeadPostName = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.LeadPostName.setAccessibleName("")
        self.LeadPostName.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.LeadPostName.setObjectName("LeadPostName")
        self.gridLayout.addWidget(self.LeadPostName, 0, 3, 1, 1)
        
        self.labelBranch = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelBranch.setObjectName("labelBranch")
        self.gridLayout.addWidget(self.labelBranch, 2, 2, 1, 1)
        
        self.Search_Button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.Search_Button.setObjectName("Search_Button")
        self.gridLayout.addWidget(self.Search_Button, 2, 4, 1, 1)
        
        self.Topic = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.Topic.setObjectName("Topic")
        self.gridLayout.addWidget(self.Topic, 2, 1, 1, 1)
        
        self.labelCompany = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelCompany.setObjectName("labelCompany")
        self.gridLayout.addWidget(self.labelCompany, 0, 4, 1, 1)
        
        self.labelPostName = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelPostName.setObjectName("labelPostName")
        self.gridLayout.addWidget(self.labelPostName, 0, 2, 1, 1)
        
        self.LeadBranch = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.LeadBranch.setObjectName("LeadBranch")
        self.gridLayout.addWidget(self.LeadBranch, 2, 3, 1, 1)
        
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 140, 1051, 21))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(20, 210, 201, 241))
        self.graphicsView.setObjectName("graphicsView")
        
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 660, 1031, 311))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.textBrowserTopicNews = QtWidgets.QTextBrowser(self.horizontalLayoutWidget)
        self.textBrowserTopicNews.setObjectName("textBrowserTopicNews")
        self.textBrowserTopicNews.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
        self.textBrowserTopicNews.setOpenLinks(False)
        self.horizontalLayout.addWidget(self.textBrowserTopicNews)
        
        self.textBrowserCompanyNews = QtWidgets.QTextBrowser(self.horizontalLayoutWidget)
        self.textBrowserCompanyNews.setObjectName("textBrowserCompanyNews")
        self.textBrowserCompanyNews.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
        self.textBrowserCompanyNews.setOpenLinks(False)
        self.horizontalLayout.addWidget(self.textBrowserCompanyNews)
        
        self.textBrowserPerson = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowserPerson.setGeometry(QtCore.QRect(240, 210, 481, 241))
        self.textBrowserPerson.setObjectName("textBrowserPerson")
        
        self.textBrowserInfobox = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowserInfobox.setGeometry(QtCore.QRect(740, 210, 311, 411))
        self.textBrowserInfobox.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
        self.textBrowserInfobox.setOpenLinks(False)
        self.textBrowserInfobox.setObjectName("textBrowserInfobox")
        
        self.textBrowserWikiSummary = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowserWikiSummary.setGeometry(QtCore.QRect(20, 500, 701, 121))
        self.textBrowserWikiSummary.setObjectName("textBrowserWikiSummary")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 630, 171, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(540, 630, 171, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 470, 171, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(740, 180, 171, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 180, 171, 16))
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1085, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # no Designer Code:
        self.Search_Button.clicked.connect(self.searchLead)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelPreName.setText(_translate("MainWindow", "Vorname:"))
        self.labelTopic.setText(_translate("MainWindow", "Thema:"))
        self.LeadCompany.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.LeadPreName.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.LeadPostName.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.labelBranch.setText(_translate("MainWindow", "Branche"))
        self.Search_Button.setText(_translate("MainWindow", "Search"))
        self.Topic.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.labelCompany.setText(_translate("MainWindow", "Firma"))
        self.labelPostName.setText(_translate("MainWindow", "Nachname:"))
        self.label.setText(_translate("MainWindow", "News zum Thema in der Branche:"))
        self.label_2.setText(_translate("MainWindow", "News zur Firma:"))
        self.label_3.setText(_translate("MainWindow", "Wiki Zusammenfassung zur Firma:"))
        self.label_4.setText(_translate("MainWindow", "Wiki Infobox zur Firma:"))
        self.label_5.setText(_translate("MainWindow", "Info über den Lead:"))

    def searchLead(self):
        
        name = self.LeadPreName.toPlainText() + ' ' + self.LeadPostName.toPlainText()
        company = self.LeadCompany.toPlainText() 
        topic = self.Topic.toPlainText() 
        branch = self.LeadBranch.toPlainText() 
            
        self.progressBar.setProperty("value", 0)
            
        lead_profile = LeadProfile(name, company, topic, branch)
        self.progressBar.setProperty("value", 15)  
            
            # Company Info: --------------------------------------------------
        try:
            company_info = lead_profile.get_company_info(return_value = 'dict')
            company_info_string = ''
            for key in company_info:
                if type(company_info[key]) is list:
                    value_string = ', '.join(str(i) for i in company_info[key])
                else: 
                    value_string = str(company_info[key])
                if key == 'Website':
                    value_string = """<a href="{url}">{url}</a>""".format(url=value_string)
                company_info_string = company_info_string + key + ': ' + value_string + '\n\n'  
                self.textBrowserInfobox.append(key + ':') 
                self.textBrowserInfobox.append(value_string) 
                self.textBrowserInfobox.append('_______________________________________________')
        except:
            self.textBrowserInfobox.setText('Company Info not found')
        self.progressBar.setProperty("value", 30)
            
            # Company Summary: -----------------------------------------------
        try:
            company_summary = lead_profile.get_company_summary()
            self.textBrowserWikiSummary.setText(company_summary)
        except:
            self.textBrowserWikiSummary.setText('Company Summary not found')
        self.progressBar.setProperty("value", 50)
            
            # Company News: --------------------------------------------------
        try:
            company_news = lead_profile.get_company_news(return_value = 'data') 
            company_news_string = ''
            for index, row in company_news.iterrows():
                self.textBrowserCompanyNews.append(row['title'])
                self.textBrowserCompanyNews.append("""<a href="{url}">{url}</a>""".format(url=row['link']))
                self.textBrowserCompanyNews.append(row['date'])
                self.textBrowserCompanyNews.append('________________________________________________________________________________')    
        except:
            self.textBrowserCompanyNews.setText('Company News not found')
        self.progressBar.setProperty("value", 75)
            
            # Topic News: ----------------------------------------------------
        try:
            topic_news = lead_profile.get_topic_news(return_value = 'data') 
            topic_news_string = ''
            for index, row in topic_news.iterrows():
                self.textBrowserTopicNews.append(row['title'])
                self.textBrowserTopicNews.append("""<a href="{url}">{url}</a>""".format(url=row['link']))
                self.textBrowserTopicNews.append(row['date'])
                self.textBrowserTopicNews.append('________________________________________________________________________________')
        except:
            self.textBrowserTopicNews.setText('Topic News not found')
        self.progressBar.setProperty("value", 100)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = LeadProfilerApp()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())