import utils
import sys
from PySide6 import QtWidgets, QtCore, QtGui


class Reader(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.news = {}
        self.newsDates = {}
        self.listNews = QtWidgets.QListWidget()
        self.listNews.setMaximumHeight(250)
        self.listNews.itemDoubleClicked.connect(self.get_article)
        self.tag = QtWidgets.QLineEdit()
        self.date_min = QtWidgets.QDateEdit()
        self.date_min_check = QtWidgets.QCheckBox()
        self.date_min_check.setText("игнорировать")
        self.date_min_check.setChecked(True)
        self.date_max_check = QtWidgets.QCheckBox()
        self.date_max_check.setText("игнорировать")
        self.date_max_check.setChecked(True)
        self.date_max = QtWidgets.QDateEdit()
        self.buttonGet = QtWidgets.QPushButton("Получить новости")
        self.buttonSave = QtWidgets.QPushButton("Сохранить новость")
        self.textNews = QtWidgets.QTextBrowser()
        self.textNews.setOpenLinks(False)
        self.buttonGet.clicked.connect(self.get_news)
        self.buttonSave.clicked.connect(self.save_article)
        self.baseLayout = QtWidgets.QVBoxLayout(self)
        buttonLayout = QtWidgets.QHBoxLayout()
        dateLayout1 = QtWidgets.QVBoxLayout()
        dateLayout2 = QtWidgets.QVBoxLayout()
        self.baseLayout.addWidget(self.listNews)
        self.baseLayout.addWidget(self.textNews)
        self.baseLayout.addWidget(self.tag)
        buttonLayout.addWidget(self.buttonGet)
        buttonLayout.addWidget(self.buttonSave)
        dateLayout1.addWidget(self.date_min)
        dateLayout1.addWidget(self.date_min_check)
        dateLayout2.addWidget(self.date_max)
        dateLayout2.addWidget(self.date_max_check)
        self.baseLayout.addLayout(buttonLayout)
        buttonLayout.addLayout(dateLayout1)
        buttonLayout.addLayout(dateLayout2)
        self.shortcutGet = QtGui.QShortcut(QtGui.QKeySequence("Return"), self)
        self.shortcutGet.activated.connect(self.get_news)

    @QtCore.Slot()
    def get_news(self):
        self.news.clear()
        self.listNews.clear()
        if (self.tag.text() == ""):
            self.news = {n.name: n.url for n in utils.get_news()}
        else:
            self.news = {
                n.name: n.url for n in utils.get_news_by_tag(self.tag.text()
                                                             .lower())}
            self.newsDates = {n.name: n.date for n in utils.get_news_by_tag(self.tag.text()
                                                                            .lower())}
        print(self.tag.text() == "")
        for n in self.news.keys():
            if ((not self.date_min_check.isChecked() and not self.date_max_check.isChecked())
                    and self.date_min.date().toPython() <= self.newsDates[n] <= self.date_max.date().toPython()):
                self.listNews.addItem(n)
            elif ((self.date_min_check.isChecked() and not self.date_max_check.isChecked()) and
                    self.newsDates[n] <= self.date_max.date().toPython()):
                self.listNews.addItem(n)
            elif ((not self.date_min_check.isChecked() and  self.date_max_check.isChecked()) and
                    self.newsDates[n] >= self.date_min.date().toPython()):
                self.listNews.addItem(n)
            elif (self.date_min_check.isChecked() and self.date_max_check.isChecked()):
                self.listNews.addItem(n)

    @QtCore.Slot()
    def get_article(self):
        url = self.news[self.listNews.currentItem().text()]
        self.textNews.clear()
        self.textNews.setText(str(utils.get_text(url)))
        print(self.date_min_check.isChecked())
        print(self.date_min_check.isChecked())

    @QtCore.Slot()
    def save_article(self):
        if self.listNews.currentItem() is not None:
            name = self.listNews.currentItem().text()
            utils.save_article(self.news[name], name)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Reader()
    widget.resize(800, 400)
    widget.show()
    sys.exit(app.exec())
