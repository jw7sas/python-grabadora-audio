# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import  QApplication
from recorder import Record, RecordingAppInterface

class Aplicacion():
	def __init__(self):
		app = QApplication(sys.argv)
		interface = RecordingAppInterface()
		record = Record(interface)
		interface.btnRecord.setAction(record.recordAudio)
		sys.exit(app.exec_())


def main():
	app = Aplicacion()
	return 0


if __name__ == '__main__':
    main()