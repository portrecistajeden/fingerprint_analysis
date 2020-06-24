import math
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QImage, QPixmap

from actions import *
from helpers import History
from Toolbar import *
from Logic import *
from widgets import GraphicsView


class FingerprintAnalyser(QMainWindow):

    def __init__(self, parent=None):
        super(FingerprintAnalyser, self).__init__(parent)
        self.setCentralWidget((GraphicsView(self)))
        self.scene = None
        self.pixmap = None
        self.minutiae = None
        self.history = History(self)

        self.action_undo = ActionUndo(self)
        self.action_redo = ActionRedo(self)

        self.toolbar_options = ToolbarOptions(self)
        self.toolbar_zoom = ToolbarZoom(self)

        self.filename = None
        self.image = None
        self.q_image = None
        self.IMAGE_LOADED = False
        
        self.prepare_gui()

        self.show()

    def prepare_gui(self):
        self.setWindowTitle('Fingerprint Analyser')
        self.setGeometry(270, 100, 1000, 650)

        # create actions
        action_open = ActionOpen(self)
        action_save = ActionSave(self)
        action_close = ActionClose(self)
        # create menubar
        menu = self.menuBar()
        action_menu = menu.addMenu('&File')
        action_menu.addAction(action_open)
        action_menu.addAction(action_save)
        action_menu.addAction(action_close)
        edit_menu = menu.addMenu('&Edit')
        edit_menu.addAction(self.action_undo)
        edit_menu.addAction(self.action_redo)

        #create toolbar
        self.addToolBar(Qt.RightToolBarArea, self.toolbar_options)
        self.addToolBar(Qt.BottomToolBarArea, self.toolbar_zoom)

    def scale(self, value):
        scale = math.pow(2, value / 200)
        self.centralWidget().zoom(scale)
        self.toolbar_zoom.update_scale(value)

    def open(self):
        filepath, filters = QFileDialog.getOpenFileName(
            self,
            'Choose file',
            './',
            filter='Image files (*.jpg *.jpeg *.png *.bmp *.gif *.tif *.tiff)'
        )
        if not filepath:
            return
        self.filename = filepath.split('/')[-1].split('.')[0]
        self.load_image(filepath)
        self.reload_canvas()
        self.DETECT = True
        self.DELETE = True
        self.IMAGE_LOADED = True

    def load_image(self, filepath):
        if filepath.split('.')[-1] == 'gif':
            pil_image = Image.open(filepath).convert('RGB')
            numpy_image = np.array(pil_image)
            self.set_image(cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR))
        else:
            self.set_image(cv2.imread(filepath))

    def set_image(self, image):
        self.image = image
        self.history.append()

    def reload_canvas(self):
        self.q_image = QImage(
            self.image.data,
            self.image.shape[1],
            self.image.shape[0],
            self.image.strides[0],
            QImage.Format_RGB888
        ).rgbSwapped()
        self.scene = QGraphicsScene(self)
        self.pixmap = QPixmap.fromImage(self.q_image)
        self.scene.addPixmap(self.pixmap)
        self.centralWidget().setScene(self.scene)

    def save(self):
        if self.IMAGE_LOADED == True:
            filepath, filters = QFileDialog.getSaveFileName(
                self,
                'Choose output directory',
                './' + self.filename,
                filter='*.jpg;;*.jpeg;;*.png;;*.bmp;;*.gif;;*.tif;;*.tiff'
            )
            if not filepath:
                return
            if filepath.split('.')[-1] == 'gif':
                pil_image = Image.fromarray(
                    cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                )
                pil_image.save(filepath)
            else:
                cv2.imwrite(filepath, self.image)

    def thinning(self):
        if self.IMAGE_LOADED == True:
            img = K3M(self.image)
            self.set_image(img)
            #self.minutiae = minutiae
            self.reload_canvas()

    def minutiae_detection(self):
        if self.IMAGE_LOADED == True and self.DETECT == True:
            minutiae_checkboxes = self.toolbar_options.get_minutiae_options()
            img, minutiae, flag = detect_minutiae(self.image, minutiae_checkboxes)
            self.set_image(img)
            self.minutiae = minutiae
            self.reload_canvas()
            if flag == True:
                self.DETECT = False

    def filter(self):
        if self.IMAGE_LOADED == True and self.DETECT == False and self.DELETE == True:
            img = delete_false_minutiae(self.image, self.minutiae)
            self.set_image(img)
            self.reload_canvas()
            self.DELETE = False