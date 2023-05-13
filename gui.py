import utils
import sys
from PySide6 import QtWidgets, QtCore, QtGui


class Reader(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.news = {}
        self.listNews = QtWidgets.QListWidget()
        self.listNews.setMaximumHeight(250)
        self.listNews.itemDoubleClicked.connect(self.get_article)
        self.tag = QtWidgets.QLineEdit()
        self.buttonGet = QtWidgets.QPushButton("Получить новости")
        self.buttonSave = QtWidgets.QPushButton("Сохранить новость")
        self.textNews = QtWidgets.QTextBrowser()
        self.textNews.setOpenLinks(False)
        self.buttonGet.clicked.connect(self.get_news)
        self.buttonSave.clicked.connect(self.save_article)
        self.baseLayout = QtWidgets.QVBoxLayout(self)
        buttonLayout = QtWidgets.QHBoxLayout()
        self.baseLayout.addWidget(self.listNews)
        self.baseLayout.addWidget(self.textNews)
        self.baseLayout.addWidget(self.tag)
        buttonLayout.addWidget(self.buttonGet)
        buttonLayout.addWidget(self.buttonSave)
        self.baseLayout.addLayout(buttonLayout)
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
        print(self.tag.text() == "")
        for n in self.news.keys():
            self.listNews.addItem(n)

    @QtCore.Slot()
    def get_article(self):
        url = self.news[self.listNews.currentItem().text()]
        self.textNews.clear()
        self.textNews.setText(str(utils.get_text(url)))

    @QtCore.Slot()
    def save_article(self):
        name = self.listNews.currentItem().text()
        utils.save_article(self.news[name], name)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Reader()
    widget.resize(800, 400)
    widget.show()
    sys.exit(app.exec())
