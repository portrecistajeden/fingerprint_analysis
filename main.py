import sys
from PyQt5.QtWidgets import QApplication
from GUI import FingerprintAnalyser

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = FingerprintAnalyser()

    sys.exit(app.exec_())
