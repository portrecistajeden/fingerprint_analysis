import numpy as np


class History:

    def __init__(self, parent):
        self.images = []
        self.current_index = -1
        self.parent = parent

    def undo(self):
        self.current_index -= 1
        self.parent.image = np.copy(self.images[self.current_index])
        self.parent.reload_canvas()
        self.parent.action_redo.setEnabled(True)
        if self.current_index < 1:
            self.parent.action_undo.setEnabled(False)

    def redo(self):
        self.current_index += 1
        self.parent.image = np.copy(self.images[self.current_index])
        self.parent.reload_canvas()
        self.parent.action_undo.setEnabled(True)
        if self.current_index >= len(self.images) - 1:
            self.parent.action_redo.setEnabled(False)

    def append(self):
        if self.current_index < len(self.images) - 1:
            self.images = self.images[:self.current_index + 1]
        if len(self.images) >= 50:
            self.images = self.images[:-1]
        self.images.append(np.copy(self.parent.image))
        self.current_index = len(self.images) - 1
        if self.current_index >= 1:
            self.parent.action_undo.setEnabled(True)
        self.parent.action_redo.setEnabled(False)
