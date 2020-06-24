from PyQt5.QtWidgets import (QToolBar, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QWidget, QLabel, QSlider, QGroupBox, QCheckBox, QSplitter)
from PyQt5.QtCore import Qt


class ToolbarOptions(QToolBar):

    def __init__(self, parent=None):
        super(ToolbarOptions, self).__init__('Options', parent)

        self.button_thinning = QPushButton('Thinning')
        self.button_detect = QPushButton('Detect')
        self.button_delete = QPushButton('Delete Minutiae')

        self.minutiae_groupbox = QGroupBox("Minutiae")
        self.minutiae_vbox = QVBoxLayout()
        self.minutiae_groupbox.setLayout(self.minutiae_vbox)
        self.single_point_chck = QCheckBox("Single point")
        self.edge_end_chck = QCheckBox("Edge End")
        self.fork_chck = QCheckBox("Fork")
        self.crossing_chck = QCheckBox("Crossing")

        self.minutiae_vbox.addWidget(self.single_point_chck)
        self.minutiae_vbox.addWidget(self.crossing_chck)
        self.minutiae_vbox.addWidget(self.edge_end_chck)
        self.minutiae_vbox.addWidget(self.fork_chck)

        self.single_point_chck.stateChanged.connect(lambda: self.on_checkbox_state_change(self.single_point_chck))
        self.edge_end_chck.stateChanged.connect(lambda: self.on_checkbox_state_change(self.edge_end_chck))
        self.fork_chck.stateChanged.connect(lambda: self.on_checkbox_state_change(self.fork_chck))
        self.crossing_chck.stateChanged.connect(lambda: self.on_checkbox_state_change(self.crossing_chck))

        self.minutiae_options = [False, False, False, False]
        layout = QVBoxLayout()
        layout.addWidget(self.button_thinning)
        layout.addWidget(self.button_detect)
        layout.addWidget(self.button_delete)
        layout.addWidget(QSplitter(Qt.Vertical))
        layout.addWidget(self.minutiae_groupbox)

        widget = QWidget()

        widget.setLayout(layout)

        self.addWidget(widget)
        self.button_thinning.clicked.connect(parent.thinning)
        self.button_detect.clicked.connect(parent.minutiae_detection)
        self.button_delete.clicked.connect(parent.filter)

    def on_checkbox_state_change(self, obj=None):
        if obj is not None:
            if self.single_point_chck.isChecked():
                self.minutiae_options[0] = True
            else:
                self.minutiae_options[0] = False

            if self.crossing_chck.isChecked():
                self.minutiae_options[1] = True
            else:
                self.minutiae_options[1] = False

            if self.edge_end_chck.isChecked():
                self.minutiae_options[2] = True
            else:
                self.minutiae_options[2] = False

            if self.fork_chck.isChecked():
                self.minutiae_options[3] = True
            else:
                self.minutiae_options[3] = False


    #@staticmethod
    def get_minutiae_options(self):
        return self.minutiae_options


class ToolbarZoom(QToolBar):

    def __init__(self, parent=None):
        super(ToolbarZoom, self).__init__('Coordinates', parent)

        self.zoom_value = QLabel()
        self.zoom_value.setMinimumWidth(50)
        self.zoom_value.setMaximumWidth(50)
        self.zoom_value.setText('x ' + str(round(self.parent().centralWidget().current_scale, 2)))

        self.zoom_slider = QSlider(Qt.Horizontal, self)
        self.zoom_slider.setMinimum(-400)
        self.zoom_slider.setMaximum(1000)
        self.zoom_slider.setValue(0)
        self.zoom_slider.valueChanged.connect(self.parent().scale)

        layout = QHBoxLayout()
        layout.addItem(QSpacerItem(10, 0))
        layout.addWidget(self.zoom_slider)
        layout.addItem(QSpacerItem(10, 0))
        layout.addWidget(self.zoom_value)

        widget = QWidget(self)
        widget.setLayout(layout)
        self.addWidget(widget)

        self.setAllowedAreas((Qt.TopToolBarArea | Qt.BottomToolBarArea))

    def update_scale(self, scale):
        self.zoom_value.setText('x ' + str(round(self.parent().centralWidget().current_scale, 2)))
