import sys
from PyQt5 import QtWidgets, QtGui, QtCore

import design
import extended
import calculate
import only_territory_graph


class Extended_window(QtWidgets.QDialog, extended.Ui_Dialog):
    def __init__(self):
        super().__init__(None, QtCore.Qt.WindowCloseButtonHint)
        self.setupUi(self)
        self.lineEdit_4.setValidator(QtGui.QtGui.QRegExpValidator(QtCore.QRegExp('\d{1,3}(?:\.\d{1,8})?'), self))
        self.lineEdit.setValidator(QtGui.QtGui.QRegExpValidator(QtCore.QRegExp('\d{1,3}'), self))
        self.lineEdit_2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('\d{1,3}'), self))
        self.lineEdit_3.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('\d{1,3}'), self))


class MainWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.extended = None
        self.extended_data = None

        val = QtGui.QRegExpValidator(QtCore.QRegExp('\d{1,3}(?:\.\d{1,5})?'), self)
        self.lineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('(\d{1,3}\.?\d{0,2} *)+'), self))
        self.lineEdit_2.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('(\d{1,3}\.?\d{0,2} *)+'), self))
        self.lineEdit_5.setValidator(val)
        self.lineEdit_3.setValidator(val)
        self.lineEdit_7.setValidator(
            QtGui.QRegExpValidator(QtCore.QRegExp('6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25'), self))
        self.lineEdit_8.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('\d{1,2}(?:\.\d{1,2})?'), self))
        self.lineEdit_9.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('[1-9][0-9]?|100'), self))
        self.lineEdit_4.setValidator(val)
        self.lineEdit_6.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('0\.[0-9]{1,6}'), self))

        self.horizontalSlider.actionTriggered.connect(self.set_precipitation)
        self.horizontalSlider_2.actionTriggered.connect(self.set_temperature)
        self.horizontalSlider_3.actionTriggered.connect(self.set_moisture)
        self.pushButton.clicked.connect(self.show_extended_window)
        self.pushButton_2.clicked.connect(self.start)
        self.pushButton_3.clicked.connect(self.territory_graph)
        self.comboBox.highlighted[int].connect(self.set_k_filtration)
        self.checkBox.stateChanged.connect(self.activate_evaporation)
        self.checkBox_2.stateChanged.connect(self.activate_filtration)
        self.lineEdit.textEdited.connect(self.check)
        self.lineEdit_2.textEdited.connect(self.check)
        self.lineEdit_3.editingFinished.connect(self.update_precipitation_slider)
        self.lineEdit_7.editingFinished.connect(self.update_temperature_slider)
        self.lineEdit_9.editingFinished.connect(self.update_moisture_slider)

        self.show()

    def territory_graph(self):
        if len(self.lineEdit_2.text().split()) != len(self.lineEdit.text().split()):
            self.error_box('Різна кількість вхідних даних для Х та Y')
        else:
            only_territory_graph.graph(self.lineEdit_2.text(), self.lineEdit.text())

    def show_extended_window(self):
        if self.extended:
            self.extended.exec_()
        else:
            self.extended = Extended_window()
            self.extended.exec_()
        self.extended_data = [self.extended.lineEdit_4.text(), self.extended.lineEdit.text(),
                              self.extended.lineEdit_2.text(), self.extended.lineEdit_3.text()]

    def check(self):
        if len(self.lineEdit_2.text().split()) != len(self.lineEdit.text().split()):
            self.lineEdit_2.setStyleSheet('background-color: rgb(255, 190, 190);')
            self.lineEdit.setStyleSheet('background-color: rgb(255, 190, 190);')

        else:
            self.lineEdit_2.setStyleSheet('background-color: rgb(255, 255, 255);')
            self.lineEdit.setStyleSheet('background-color: rgb(255, 255, 255);')

    def update_precipitation_slider(self):
        if float(self.lineEdit_3.text()) <= self.horizontalSlider.minimum():
            self.horizontalSlider.setValue(self.horizontalSlider.minimum())
        elif float(self.lineEdit_3.text()) < self.horizontalSlider.maximum():
            self.horizontalSlider.setValue(float(self.lineEdit_3.text()))
        elif float(self.lineEdit_3.text()) >= self.horizontalSlider.maximum():
            self.horizontalSlider.setValue(self.horizontalSlider.maximum())

    def update_temperature_slider(self):
        if not self.lineEdit_7.hasAcceptableInput():
            self.lineEdit_7.setText('6')
        self.horizontalSlider_2.setSliderPosition(int(self.lineEdit_7.text()))

    def update_moisture_slider(self):
        if not self.lineEdit_9.hasAcceptableInput():
            self.lineEdit_9.setText('50')
        self.horizontalSlider_3.setSliderPosition(int(self.lineEdit_9.text()))

    def set_precipitation(self):
        self.lineEdit_3.setText(str(self.horizontalSlider.sliderPosition()))

    def set_temperature(self):
        self.lineEdit_7.setText(str(self.horizontalSlider_2.sliderPosition()))

    def set_moisture(self):
        self.lineEdit_9.setText(str(self.horizontalSlider_3.sliderPosition()))

    def activate_evaporation(self):
        if self.checkBox.checkState():
            self.lineEdit_7.setEnabled(True)
            self.lineEdit_8.setEnabled(True)
            self.lineEdit_9.setEnabled(True)
            self.label_12.setEnabled(True)
            self.label_13.setEnabled(True)
            self.label_14.setEnabled(True)
            self.horizontalSlider_2.setEnabled(True)
            self.horizontalSlider_3.setEnabled(True)
        else:
            self.lineEdit_7.setEnabled(False)
            self.lineEdit_8.setEnabled(False)
            self.lineEdit_9.setEnabled(False)
            self.label_12.setEnabled(False)
            self.label_13.setEnabled(False)
            self.label_14.setEnabled(False)
            self.horizontalSlider_2.setEnabled(False)
            self.horizontalSlider_3.setEnabled(False)

    def activate_filtration(self):
        if self.checkBox_2.checkState():
            self.label_6.setEnabled(True)
            self.label_7.setEnabled(True)
            self.label_10.setEnabled(True)
            self.label_11.setEnabled(True)
            self.lineEdit_4.setEnabled(True)
            self.lineEdit_6.setEnabled(True)
            self.comboBox.setEnabled(True)
        else:
            self.label_6.setEnabled(False)
            self.label_7.setEnabled(False)
            self.label_10.setEnabled(False)
            self.label_11.setEnabled(False)
            self.lineEdit_4.setEnabled(False)
            self.lineEdit_6.setEnabled(False)
            self.comboBox.setEnabled(False)

    def set_k_filtration(self, param):
        if param == 0:
            self.lineEdit_4.setText(str(0.005))
        elif param == 1:
            self.lineEdit_4.setText(str(0.05))
        elif param == 2:
            self.lineEdit_4.setText(str(0.25))
        elif param == 3:
            self.lineEdit_4.setText(str(0.75))
        elif param == 4:
            self.lineEdit_4.setText(str(2.5))

    def start(self):
        lenght = list(
            map(len, [self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), self.lineEdit_5.text(),
                      self.lineEdit_6.text(), self.lineEdit_7.text(), self.lineEdit_8.text(), self.lineEdit_9.text()]))
        if len(self.lineEdit_2.text().split()) != len(self.lineEdit.text().split()):
            self.error_box('Різна кількість вхідних даних для Х та Y')
        elif not self.lineEdit_7.hasAcceptableInput():
            self.error_box('Не вірне значення температури поверхні води')
        elif not all(lenght):
            self.error_box('Відсутні деякі значення вхідних даних')
        else:
            calculate.calculate(self.lineEdit_2.text(), self.lineEdit.text(), self.lineEdit_5.text(),
                                self.lineEdit_3.text(), self.checkBox.checkState(), self.lineEdit_7.text(),
                                self.lineEdit_8.text(), self.lineEdit_9.text(),
                                self.checkBox_2.checkState(), self.lineEdit_4.text(), self.lineEdit_6.text(),
                                self.extended_data
                                )

    def error_box(self, cause):
        error = QtWidgets.QMessageBox()
        error.setWindowTitle('Error')
        error.setText("Error occurred")
        error.setIcon(QtWidgets.QMessageBox.Critical)
        error.setInformativeText(cause)
        error.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())
