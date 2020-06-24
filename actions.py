from PyQt5.QtWidgets import QAction


class ActionOpen(QAction):

    def __init__(self, parent):
        super(ActionOpen, self).__init__('&Open', parent)
        self.setShortcut('Ctrl+O')
        self.setStatusTip('Load image from file')
        self.triggered.connect(self.parent().open)


class ActionSave(QAction):

    def __init__(self, parent):
        super(ActionSave, self).__init__('&Save', parent)
        self.setShortcut('Ctrl+S')
        self.setStatusTip('Save to file')
        self.triggered.connect(self.parent().save)


class ActionClose(QAction):

    def __init__(self, parent):
        super(ActionClose, self).__init__('&Close', parent)
        self.setShortcut('Ctrl+W')
        self.setStatusTip('Close program')
        self.triggered.connect(self.parent().close)


class ActionUndo(QAction):

    def __init__(self, parent):
        super(ActionUndo, self).__init__('&Undo', parent)
        self.setShortcut('Ctrl+Z')
        self.setEnabled(False)
        self.triggered.connect(self.parent().history.undo)


class ActionRedo(QAction):

    def __init__(self, parent):
        super(ActionRedo, self).__init__('&Redo', parent)
        self.setShortcut('Shift+Ctrl+Z')
        self.setEnabled(False)
        self.triggered.connect(self.parent().history.redo)

