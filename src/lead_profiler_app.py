# -*- coding: utf-8 -*-

# Originally generated from LeadProfiler.ui by the PyQt5 UI code generator.
# This file is now hand-maintained (searchLead, exportBriefing, and the
# widgets they use were added by hand) — do NOT regenerate with pyuic5,
# doing so would discard those changes. LeadProfiler.ui is kept only as a
# historical reference of the original layout.

import logging

import requests
import wikipedia
from PyQt5 import QtCore, QtGui, QtWidgets

from .briefing import Briefing, build_markdown
from .config import load_config
from .lead_profile import InfoboxNotFoundError, LeadProfile
from .logging_setup import setup_logging
from .talking_points import TalkingPointsError, TalkingPointsGenerator

logger = logging.getLogger(__name__)


class LeadProfilerApp(object):
    def setupUi(self, MainWindow):
        self.config = load_config()

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
        self.textBrowserPerson.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
        self.textBrowserPerson.setOpenLinks(False)

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

        # New widgets: LLM talking points, adjustable news window, export.
        self.labelTalkingPoints = QtWidgets.QLabel(self.centralwidget)
        self.labelTalkingPoints.setGeometry(QtCore.QRect(1080, 180, 300, 16))
        self.labelTalkingPoints.setObjectName("labelTalkingPoints")

        self.textBrowserTalkingPoints = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowserTalkingPoints.setGeometry(QtCore.QRect(1080, 210, 480, 620))
        self.textBrowserTalkingPoints.setObjectName("textBrowserTalkingPoints")

        self.labelMonths = QtWidgets.QLabel(self.centralwidget)
        self.labelMonths.setGeometry(QtCore.QRect(1080, 850, 200, 16))
        self.labelMonths.setObjectName("labelMonths")

        self.spinBoxMonths = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBoxMonths.setGeometry(QtCore.QRect(1080, 870, 100, 30))
        self.spinBoxMonths.setMinimum(1)
        self.spinBoxMonths.setMaximum(60)
        self.spinBoxMonths.setValue(self.config.news_months)
        self.spinBoxMonths.setObjectName("spinBoxMonths")

        self.Export_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Export_Button.setGeometry(QtCore.QRect(1080, 910, 200, 30))
        self.Export_Button.setObjectName("Export_Button")
        self.Export_Button.setEnabled(False)

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
        self.Export_Button.clicked.connect(self.exportBriefing)
        self.current_briefing = None

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
        self.labelTalkingPoints.setText(_translate("MainWindow", "Gesprächspunkte (KI):"))
        self.labelMonths.setText(_translate("MainWindow", "Zeitraum (Monate):"))
        self.Export_Button.setText(_translate("MainWindow", "Export (Markdown)"))

    def searchLead(self):
        name = self.LeadPreName.toPlainText() + ' ' + self.LeadPostName.toPlainText()
        company = self.LeadCompany.toPlainText()
        topic = self.Topic.toPlainText()
        branch = self.LeadBranch.toPlainText()

        # Clear previous results — the widgets use append(), so without this
        # a second search would accumulate on top of the first.
        self.textBrowserInfobox.clear()
        self.textBrowserWikiSummary.clear()
        self.textBrowserCompanyNews.clear()
        self.textBrowserTopicNews.clear()
        self.textBrowserPerson.clear()
        self.textBrowserTalkingPoints.clear()
        self.Export_Button.setEnabled(False)
        self.current_briefing = None

        self.progressBar.setProperty("value", 0)
        self.config.news_months = self.spinBoxMonths.value()

        lead_profile = LeadProfile(name, company, topic, branch, self.config)
        briefing = Briefing(person=name, company=company, topic=topic, branch=branch)
        self.progressBar.setProperty("value", 10)
        QtWidgets.QApplication.processEvents()

        # Company Info: --------------------------------------------------
        try:
            company_info = lead_profile.get_company_info()
            briefing.company_info = company_info
            for key, value in company_info.items():
                if isinstance(value, list):
                    value_string = ', '.join(str(i) for i in value)
                else:
                    value_string = str(value)
                if key == 'Website':
                    value_string = """<a href="{url}">{url}</a>""".format(url=value_string)
                self.textBrowserInfobox.append(key + ':')
                self.textBrowserInfobox.append(value_string)
                self.textBrowserInfobox.append('_______________________________________________')
        except InfoboxNotFoundError:
            self.textBrowserInfobox.setText('Keine Unternehmens-Infobox im Wikipedia-Artikel gefunden.')
        except wikipedia.exceptions.DisambiguationError as e:
            self.textBrowserInfobox.setText('Mehrdeutiger Begriff. Meinten Sie: ' + ', '.join(e.options[:5]))
        except wikipedia.exceptions.PageError:
            self.textBrowserInfobox.setText("Kein Wikipedia-Artikel zu '{}' gefunden.".format(company))
        except wikipedia.exceptions.HTTPTimeoutError:
            self.textBrowserInfobox.setText('Wikipedia nicht erreichbar (Timeout).')
        except wikipedia.exceptions.WikipediaException as e:
            logger.exception("Wikipedia error while fetching company info")
            self.textBrowserInfobox.setText('Wikipedia-Fehler: {}'.format(e))
        except requests.exceptions.RequestException:
            logger.exception("Network error while fetching company info")
            self.textBrowserInfobox.setText('Netzwerkfehler — bitte Internetverbindung prüfen.')
        self.progressBar.setProperty("value", 25)
        QtWidgets.QApplication.processEvents()

        # Company Summary: -----------------------------------------------
        try:
            company_summary = lead_profile.get_company_summary()
            briefing.company_summary = company_summary
            self.textBrowserWikiSummary.setText(company_summary)
        except wikipedia.exceptions.DisambiguationError as e:
            self.textBrowserWikiSummary.setText('Mehrdeutiger Begriff. Meinten Sie: ' + ', '.join(e.options[:5]))
        except wikipedia.exceptions.PageError:
            self.textBrowserWikiSummary.setText("Kein Wikipedia-Artikel zu '{}' gefunden.".format(company))
        except wikipedia.exceptions.HTTPTimeoutError:
            self.textBrowserWikiSummary.setText('Wikipedia nicht erreichbar (Timeout).')
        except wikipedia.exceptions.WikipediaException as e:
            logger.exception("Wikipedia error while fetching company summary")
            self.textBrowserWikiSummary.setText('Wikipedia-Fehler: {}'.format(e))
        except requests.exceptions.RequestException:
            logger.exception("Network error while fetching company summary")
            self.textBrowserWikiSummary.setText('Netzwerkfehler — bitte Internetverbindung prüfen.')
        self.progressBar.setProperty("value", 40)
        QtWidgets.QApplication.processEvents()

        # Company News: --------------------------------------------------
        try:
            company_news = lead_profile.get_company_news()
            briefing.company_news = company_news
            if not company_news:
                self.textBrowserCompanyNews.setText(
                    'Keine News gefunden (ggf. Suchbegriff prüfen oder Google-Rate-Limit — später erneut versuchen).'
                )
            for item in company_news:
                self.textBrowserCompanyNews.append(item['title'])
                self.textBrowserCompanyNews.append("""<a href="{url}">{url}</a>""".format(url=item['link']))
                self.textBrowserCompanyNews.append(item['date'] or '')
                self.textBrowserCompanyNews.append('________________________________________________________________________________')
        except requests.exceptions.RequestException:
            logger.exception("Network error while fetching company news")
            self.textBrowserCompanyNews.setText('Netzwerkfehler — bitte Internetverbindung prüfen.')
        except Exception:
            logger.exception("Unexpected error while fetching company news")
            self.textBrowserCompanyNews.setText('Company News not found')
        self.progressBar.setProperty("value", 55)
        QtWidgets.QApplication.processEvents()

        # Topic News: ----------------------------------------------------
        try:
            topic_news = lead_profile.get_topic_news()
            briefing.topic_news = topic_news
            if not topic_news:
                self.textBrowserTopicNews.setText(
                    'Keine News gefunden (ggf. Suchbegriff prüfen oder Google-Rate-Limit — später erneut versuchen).'
                )
            for item in topic_news:
                self.textBrowserTopicNews.append(item['title'])
                self.textBrowserTopicNews.append("""<a href="{url}">{url}</a>""".format(url=item['link']))
                self.textBrowserTopicNews.append(item['date'] or '')
                self.textBrowserTopicNews.append('________________________________________________________________________________')
        except requests.exceptions.RequestException:
            logger.exception("Network error while fetching topic news")
            self.textBrowserTopicNews.setText('Netzwerkfehler — bitte Internetverbindung prüfen.')
        except Exception:
            logger.exception("Unexpected error while fetching topic news")
            self.textBrowserTopicNews.setText('Topic News not found')
        self.progressBar.setProperty("value", 70)
        QtWidgets.QApplication.processEvents()

        # Person Info: -----------------------------------------------------
        try:
            person_info = lead_profile.get_person_info()
            briefing.person_info = person_info
            summary = person_info.get('wiki_summary')
            news = person_info.get('news') or []
            if summary:
                self.textBrowserPerson.append(summary)
                self.textBrowserPerson.append('_______________________________________________')
            if not summary and not news:
                self.textBrowserPerson.setText('Keine Informationen zur Person gefunden.')
            for item in news:
                self.textBrowserPerson.append(item['title'])
                self.textBrowserPerson.append("""<a href="{url}">{url}</a>""".format(url=item['link']))
                self.textBrowserPerson.append(item['date'] or '')
                self.textBrowserPerson.append('_______________________________________________')
        except requests.exceptions.RequestException:
            logger.exception("Network error while fetching person info")
            self.textBrowserPerson.setText('Netzwerkfehler — bitte Internetverbindung prüfen.')
        except Exception:
            logger.exception("Unexpected error while fetching person info")
            self.textBrowserPerson.setText('Info über den Lead nicht gefunden.')
        self.progressBar.setProperty("value", 85)
        QtWidgets.QApplication.processEvents()

        # Talking Points (KI): ----------------------------------------------
        generator = TalkingPointsGenerator(self.config)
        if generator.is_available():
            try:
                talking_points = generator.generate(briefing)
                briefing.talking_points = talking_points
                self.textBrowserTalkingPoints.setText(talking_points)
            except TalkingPointsError as e:
                logger.exception("Talking points generation failed")
                self.textBrowserTalkingPoints.setText(str(e))
        else:
            self.textBrowserTalkingPoints.setText(
                'KI-Gesprächspunkte deaktiviert: Umgebungsvariable ANTHROPIC_API_KEY nicht gesetzt.'
            )
        self.progressBar.setProperty("value", 100)

        self.current_briefing = briefing
        self.Export_Button.setEnabled(True)

    def exportBriefing(self):
        if not self.current_briefing:
            return

        safe_company = (self.current_briefing.company or 'lead').strip().replace(' ', '_') or 'lead'
        default_name = "briefing_{}_{}.md".format(
            safe_company, self.current_briefing.created_at.strftime('%Y-%m-%d')
        )
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            None, "Briefing exportieren", default_name, "Markdown (*.md)"
        )
        if not path:
            return

        try:
            content = build_markdown(self.current_briefing)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            logger.exception("Failed to export briefing")
            self.statusbar.showMessage("Export fehlgeschlagen: {}".format(e), 5000)
            return

        self.statusbar.showMessage("Exportiert: {}".format(path), 5000)


if __name__ == "__main__":
    import sys

    config = load_config()
    setup_logging(config.log_level)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = LeadProfilerApp()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
