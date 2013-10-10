# Copyright (c) James Percent, Byron Galbraith and Unlock contributors.
# All rights reserved.
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#    
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of Unlock nor the names of its contributors may be used
#       to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from unlock.model import TimedStimulus, HierarchyGridState, TimedStimuli, OfflineData
from unlock.view import FlickeringPygletSprite, SpritePositionComputer, HierarchyGridView
from unlock.decode import HarmonicSumDecision, RawInlineSignalReceiver, ClassifiedCommandReceiver
from unlock.controller import UnlockController, Canvas
import inspect
import os


class GridSpeak(UnlockControllerFragment):
    def __init__(self,model, view, standalone=False):
        assert grid_state != None 
        super(GridSpeak, self).__init__(model, view, standalone)
        self.standalone = standalone

    @staticmethod
    def create_gridspeak_fragment(self, canvas):
        grid_model = HierarchyGridState(2)
        grid_view = HierarchyGridView(grid_model, canvas)
        gridspeak = GridSpeak(grid_model, grid_view)
        return gridspeak
        
    @staticmethod
    def create_gridspeak(self, window, canvas, signal, timer, base=None, color='bw'):
        gridspeak = GridSpeak.create_gridspeak_fragment(canvas)
        if base == None:
            base = EEGControllerFragment.create_ssvep(canvas, signal, timer, color)
            
        base.views.append(gridview.view)
        gridspeak = GridSpeak(grid_model, gridview)
        controller_chain = UnlockControllerChain(window, canvas, base.command_receiver,
                                                 [base, gridspeak] , 'GridSpeak', 'LazerToggleS.png',
                                                 standalone=False)