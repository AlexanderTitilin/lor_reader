from gui import Reader
import sys
from PySide6 import QtWidgets
app = QtWidgets.QApplication([])
widget = Reader()
widget.resize(800, 400)
widget.show()
sys.exit(app.exec())
