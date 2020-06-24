from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene


class GraphicsScene(QGraphicsScene):

    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)

    def mousePressEvent(self, event):
        x = int(event.scenePos().x())
        y = int(event.scenePos().y())
        self.parent().receive_click(x, y)

    def mouseMoveEvent(self, event):
        x = int(event.scenePos().x())
        y = int(event.scenePos().y())
        self.parent().update_cursor_position(x, y)


class GraphicsView(QGraphicsView):

    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)

        self.current_scale = 1

    def zoom(self, value):
        transformation = value / self.current_scale
        super(GraphicsView, self).scale(transformation, transformation)
        self.current_scale = value

    def scale(self, value):
        self.current_scale *= value
        super(GraphicsView, self).scale(value, value)
