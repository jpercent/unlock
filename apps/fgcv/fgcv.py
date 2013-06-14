from core import UnlockApplication
import numpy as np

class FixedGazeCVEP(UnlockApplication):
    name = 'FixedGazeCVEP'

    def __init__(self, screen):
        super(FixedGazeCVEP, self).__init__(screen)
        cx, cy = screen.get_center()
        self.halo = screen.drawText('+', cx, cy, color=(255, 255, 0))
        #self.halo.anchor_x = 'center'
        #self.halo.anchor_y = 'center'
        self.fixation = screen.drawText('+', cx, cy)
        #self.fixation.anchor_x = 'center'
        #self.fixation.anchor_y = 'center'
        self.halo_size = 100

    def update(self, dt, decision, selection):
        self.halo_size -= (1 + np.random.randint(-4, 4))
        if self.halo_size <= 0:
            self.halo_size = 100
        self.halo.font_size = self.halo_size