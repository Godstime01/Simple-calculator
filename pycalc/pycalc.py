from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont

ERROR_MSG = 'ERROR'

class PyCalcUi(QWidget):
    """calculator UI 
    provides a good interface for users to interact with the application
    """
    def __init__(self):
        super().__init__()

        # self.setGeometry(200, 200, 200, 250)
        self.setFixedSize(195,250)
        self.setWindowTitle('Calculator')

        # creating general layout
        self.genLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        # self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.genLayout)

        self._create_display()
        self._create_btns()

    def _create_display(self):
        self.screen = QLineEdit()
        self.screen.setFixedHeight(50)
        self.screen.setFont(QFont('calibri',10))
        self.screen.setAlignment(Qt.AlignRight) # make input align Right
        self.screen.setReadOnly(True) # does not allow editing

        # adding self.screen to genlayout with vHboxlayout
        self.genLayout.addWidget(self.screen)

    def _create_btns(self):
        buttonsLayout = QGridLayout()
        self.btn = {}
        buttons = {
            '1':(0,0),
            '2':(0,1),
            '3':(0,2),
            '/':(0,3),
            '4':(1,0),
            '5':(1,1),
            '6':(1,2),
            '*':(1,3),
            '7':(2,0),
            '8':(2,1),
            '9':(2,2),
            '-':(2,3),
            '0':(3,0),
            '00':(3,1),
            '.':(3,2),
            '=':(3,3),
        }
        for btnText, pos in buttons.items():
            self.btn[btnText] = QPushButton(btnText)
            self.btn[btnText].setFixedSize(40,40)

            buttonsLayout.addWidget(self.btn[btnText], pos[0], pos[1])

        self.genLayout.addLayout(buttonsLayout)

    def setScreenText(self, text):
        self.screen.setText(text)
        self.screen.setFocus()

    def screenText(self):
        return self.screen.text()

    def clearScreen(self):
        self.setScreenText('')

class PyCalcCtrl:
    '''
    connect the UI with model
    '''
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._connectSignals()

    def _calcc(self):
        result = self._model(expression = self._view.screenText())
        self._view.setScreenText(str(result))

    def _connectSignals(self):
        
        """"""
        for btnText, btn in self._view.btn.items():
            if btnText not in {'='}:
                btn.clicked.connect(partial(self._buildExpression, btnText))

        self._view.btn['='].clicked.connect(self._calcc)
        self._view.screen.returnPressed.connect(self._calcc)

    def _buildExpression(self, supExp):
        if self._view.screenText() == ERROR_MSG:
            self._view.clearScreen()

        exps = self._view.screenText() + supExp
        self._view.setScreenText(exps)


def calcModel(expression):
    try:
        result = eval(expression)
    except Exception:
        result = ERROR_MSG
    return result

def main():
    app = QApplication([])
    window = PyCalcUi()
    PyCalcCtrl(view = window, model = calcModel)
    window.show()
    app.exec_()



if __name__ == "__main__":
    main()
    