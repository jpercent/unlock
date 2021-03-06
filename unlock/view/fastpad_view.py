from unlock.view.view import UnlockView

import sys

if sys.platform.startswith("linux"):
    try:
        from espeak import espeak
    except:
        raise Exception("ERROR: Missing python-espeak module")
elif sys.platform.startswith("darwin"):
    import subprocess
elif sys.platform.startswith('win'):
    try:
        import win32com.client
    except:
        raise Exception("ERROR: Missing pywin32")
        
class FastPadButton(UnlockView):
    """
    Class for a FastPad button.
    """
    def __init__(self, rect, labels, actions, canvas):
        """
        Initialize the internal data structures and
        graphical button layout.
        
        Input:
            screen -- (Unlock Screen) Drawing area
            rect -- (tuple(int, int, int, int)) Rectangle
                with x, y, width, and height
            labels -- (list(str)) Strings to display on
                the button; first is the biggest
            actions -- (list(funcs)) Actions to perform
                when labels are selected; a function will
                be passed the label as its argument
        
        Raises an Exception if anything goes wrong.
        """
        super(FastPadButton, self).__init__()
        self.canvas = canvas
        # Draw the button border -- hack around Unlock's drawRect()
        #drawRect(*rect) # This would be nicer...
        self.rect = rect
        self.drawLine(rect[0], rect[1],
                rect[0], rect[1] + rect[3], self.canvas)
        self.drawLine(rect[0], rect[1] + rect[3],
                rect[0] + rect[2], rect[1] + rect[3], self.canvas)
        self.drawLine(rect[0] + rect[2], rect[1] + rect[3],
                rect[0] + rect[2], rect[1], self.canvas)
        self.drawLine(rect[0] + rect[2],
                rect[1], rect[0], rect[1], self.canvas)
            
        # Draw the labels
        self.texts = []
        self.rects = []
        self.texts.append(self.drawText(labels[0],
                rect[0] + (.5 * rect[2]), rect[1] + (.75 * rect[3]), self.canvas))
        self.rects.append((
            rect[0] + (.5 * rect[2]) - self.texts[-1].content_width/2,
            rect[1] + (.75 * rect[3]) - self.texts[-1].content_height * 0.35,
            self.texts[-1].content_width,
            self.texts[-1].content_height * .65))
        if len(labels) > 1:
            # Calculate the sub-label positions
            width = rect[2] / (len(labels) - 1)
                
            # Draw the sub-labels
            left = rect[0] + (width / 2)
            for label in labels[1:]:
                self.texts.append(self.drawText(label,
                    left, rect[1] + (.25 * rect[3]), self.canvas, size=int(.65 * self.texts[0].font_size)))
                self.rects.append((
                    left - self.texts[-1].content_width/2,
                    rect[1] + (.25 * rect[3]) - self.texts[-1].content_height * 0.35,
                    self.texts[-1].content_width,
                    self.texts[-1].content_height * 0.65))
                left += width
                
        # Store the labels and actions
        self.labels = labels
        self.actions = actions
        while len(self.actions) < len(self.labels):
            
            # Expand function pointers, if necessary
            self.actions.append(self.actions[-1])
            
        # Initialize links to other buttons
        self.up = None
        self.down = None
        self.left = None
        self.right = None
    def render(self):
        pass
    
class FastPadView(UnlockView):
    BG_COLOR = (0, 0, 0) # Color of the background
    CURSOR_COLOR = (0, 0, 255) # Color of the cursor
    CURSOR_MARGIN = 2 # Margin around the cursor, in pixels
    def __init__(self, model, canvas):
        """
        Initialize internal data structures.

        Input:
            screen -- (Unlock Screen) Drawing area

        Raises an Exception if anything goes wrong.
        """
        # Call our parent's constructor
        super(UnlockView, self).__init__()
        self.model = model

        # Get the GUI calculations
        self.canvas = canvas
        textH = .08 * canvas.height
        padW = .25 * canvas.width
        padH = canvas.height - textH
        padL = (canvas.width - padW) / 2
        buttonW = padW / 3
        buttonH = (canvas.height - textH) / 10
        self.batch = canvas.batch

#      def drawRect(self, x_offset, y_offset, width, height, batch, color=(255,255,255), fill=False,
        # Create the text bar
        
        self.textRect = self.drawRect(canvas.width / 4, canvas.height * .65 , canvas.width / 2, textH, self.batch)
        
#    def drawText(self, text, x, y, batch, font='Helvetica', size=48,
#                 color=(255,255,255,255), group=None, xoffset=0, yoffset=0):
        
        self.text = self.drawText("",
                canvas.width / 4 + canvas.width/2/2, canvas.height * .65 + textH/2, canvas)
        self.text.width = canvas.width / 4
        startH = canvas.height / 4
        # Create the buttons
# fast_pad_model, rect, labels, actions):        
        self.buttonB = FastPadButton(
            
                (padL, startH, buttonW, buttonH),
                ["<"],
                [self.removeText],
                canvas
                )
        self.button0 = FastPadButton(
                (padL + buttonW, startH, buttonW, buttonH),
                ["0", "_"],
                [self.addText],
                canvas,
                )
        self.buttonE = FastPadButton(
                (padL + (2 * buttonW), startH, buttonW, buttonH),
                [">"],
                [self.speakText],
                canvas,
                )
        self.button7 = FastPadButton(
                (padL, startH+buttonH, buttonW, buttonH),
                ["7", "P", "Q", "R", "S"],
                [self.addText],
                canvas,
                )
        self.button8 = FastPadButton(
                (padL + buttonW, startH+buttonH, buttonW, buttonH),
                ["8", "T", "U", "V"],
                [self.addText],
                canvas,
                )
        self.button9 = FastPadButton(
                (padL + (2 * buttonW), startH+buttonH, buttonW, buttonH),
                ["9", "W", "X", "Y", "Z"],
                [self.addText],
                canvas,
                )
        self.button4 = FastPadButton(
                (padL, startH+buttonH * 2, buttonW, buttonH),
                ["4", "G", "H", "I"],
                [self.addText],
                canvas,
                )
        self.button5 = FastPadButton(
                (padL + buttonW, startH+buttonH * 2, buttonW, buttonH),
                ["5", "J", "K", "L"],
                [self.addText],
                canvas,
                )
        self.button6 = FastPadButton(
                (padL + (2 * buttonW), startH+buttonH * 2, buttonW, buttonH),
                ["6", "M", "N", "O"],
                [self.addText],
                canvas,
                )
        self.button1 = FastPadButton(
                (padL, startH+buttonH * 3, buttonW, buttonH),
                ["1"],
                [self.addText],
                canvas,
                )
        self.button2 = FastPadButton(
                (padL + buttonW, startH+buttonH * 3, buttonW, buttonH),
                ["2", "A", "B", "C"],
                [self.addText],
                canvas,
                )
        self.button3 = FastPadButton(
                (padL + (2 * buttonW), startH+buttonH * 3, buttonW, buttonH),
                ["3", "D", "E", "F"],
                [self.addText],
                canvas,
                )
                
        # Link the buttons to each other
        self.button1.up = self.buttonB
        self.button1.down = self.button4
        self.button1.left = self.button3
        self.button1.right = self.button2
        self.button2.up = self.button0
        self.button2.down = self.button5
        self.button2.left = self.button1
        self.button2.right = self.button3
        self.button3.up = self.buttonE
        self.button3.down = self.button6
        self.button3.left = self.button2
        self.button3.right = self.button1
        self.button4.up = self.button1
        self.button4.down = self.button7
        self.button4.left = self.button6
        self.button4.right = self.button5
        self.button5.up = self.button2
        self.button5.down = self.button8
        self.button5.left = self.button4
        self.button5.right = self.button6
        self.button6.up = self.button3
        self.button6.down = self.button9
        self.button6.left = self.button5
        self.button6.right = self.button4
        self.button7.up = self.button4
        self.button7.down = self.buttonB
        self.button7.left = self.button9
        self.button7.right = self.button8
        self.button8.up = self.button5
        self.button8.down = self.button0
        self.button8.left = self.button7
        self.button8.right = self.button9
        self.button9.up = self.button6
        self.button9.down = self.buttonE
        self.button9.left = self.button8
        self.button9.right = self.button7
        self.buttonB.up = self.button7
        self.buttonB.down = self.button1
        self.buttonB.left = self.buttonE
        self.buttonB.right = self.button0
        self.button0.up = self.button8
        self.button0.down = self.button2
        self.button0.left = self.buttonB
        self.button0.right = self.buttonE
        self.buttonE.up = self.button9
        self.buttonE.down = self.button3
        self.buttonE.left = self.button0
        self.buttonE.right = self.buttonB

        # Initialize the state
#        self.mode = "CURSOR"

        self.currButton = self.button5
        self.model.currButton = self.button5
        self.model.button = self.button5
        self.currIndex = 0
 #       self.selTime = 0
#        self.setMode(self.mode, self.currButton)

    def addText(self, label):
        """
        Add the given label to the current text if
        there is enough space.

        Input:
            label -- (str) The text to add

        Raises an Exception if anything goes wrong.
        """
#        print ("ADDing text = ", label)
        prev = self.text.text
        self.text.text += label
        if self.text.content_width > self.text.width:
            self.text.text = prev

    def removeText(self, label):
        """
        Removes 1 character from the end of the current
        text, if available.
        
        Input:
            label -- (str) Unused

        Raises an Exception if anything goes wrong.
        """
        if len(self.text.text) >= 1:
            self.text.text = self.text.text[:-1]

    def speakText(self, label):
        """
        Speaks the current text out via a TTS if we're
        on a supported platform.
            
        Input:
            label -- (str) Unused
            
        Raises an Exception if anything goes wrong.
        """
        text = self.text.text.replace("_", " ")
        if sys.platform.startswith("linux"):
            espeak.synth(text)
        elif sys.platform.startswith("darwin"):
            subprocess.call(["say", text])
        elif sys.platform.startswith('win'):
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(text)
            
        self.text.text = ""
        
    def render(self):
        """
        Set the FastPad into the given state/mode.
        
        Input:
            mode -- (str) One of "CURSOR" or "SELECT"
            button -- (FastPadButton) Where is the cursor
                or selection marker?
                
        Raises an Exception if anything goes wrong.
        """
        
        if self.model.noop == True:
            self.model.noop = False
            return
                
        # Clear the old rectangle
        self.drawRect(
                self.currButton.rect[0] + FastPadView.CURSOR_MARGIN,
                self.currButton.rect[1] + FastPadView.CURSOR_MARGIN,
                self.currButton.rect[2] - (2 * FastPadView.CURSOR_MARGIN),
                self.currButton.rect[3] - (2 * FastPadView.CURSOR_MARGIN),
                self.batch,
                color = FastPadView.BG_COLOR,
                fill = True)
                
        # We're currently in CURSOR mode
        if self.model.previous_mode == "CURSOR":
            
            # And remaining in CURSOR mode
            if self.model.mode == "CURSOR":
                
                # Set the new location
                self.currButton = self.model.button
                # XXX - what a tangled web we weave...
                self.model.currButton = self.model.button                
                # Draw the new rectangle
                self.drawRect(
                        self.currButton.rect[0] + FastPadView.CURSOR_MARGIN,
                        self.currButton.rect[1] + FastPadView.CURSOR_MARGIN,
                        self.currButton.rect[2] - (2 * FastPadView.CURSOR_MARGIN),
                        self.currButton.rect[3] - (2 * FastPadView.CURSOR_MARGIN),
                        self.batch,                     
                        color = FastPadView.CURSOR_COLOR,
                        fill = True,
                        )
                        
            # And switching to SELECT mode
            elif self.model.mode == "SELECT":
                
                # Draw the new rectangle
                self.drawRect(
                        self.currButton.rects[self.currIndex][0],
                        self.currButton.rects[self.currIndex][1],
                        self.currButton.rects[self.currIndex][2],
                        self.currButton.rects[self.currIndex][3],
                        self.batch,                        
                        color = FastPadView.CURSOR_COLOR,
                        fill = True,
                        )
                        
        # We're currently in SELECT mode
        elif self.model.previous_mode == "SELECT":
            
            # And remaining in SELECT mode
            if self.model.mode == "SELECT":
                
                # Rotate the index
                self.currIndex += 1
                if self.currIndex >= len(self.currButton.rects):
                    self.currIndex = 0
                    
                # Draw the new rectangle
                self.drawRect(
                        self.currButton.rects[self.currIndex][0],
                        self.currButton.rects[self.currIndex][1],
                        self.currButton.rects[self.currIndex][2],
                        self.currButton.rects[self.currIndex][3],
                        self.batch,                                                
                        color = FastPadView.CURSOR_COLOR,
                        fill = True,
                        )
                        
            # And switching to CURSOR mode
            elif self.model.mode == "CURSOR":

                # Call the selected item's action
                self.currButton.actions[self.currIndex](
                        self.currButton.labels[self.currIndex])
                        
                # Reset the index
                self.currIndex = 0
                
                # Set the new location
                self.currButton = self.model.button
                #XXX - tangled up in buttons..
                self.model.currButton = self.model.button
                
                # Draw the new rectangle
                self.drawRect(
                        self.currButton.rect[0] + FastPadView.CURSOR_MARGIN,
                        self.currButton.rect[1] + FastPadView.CURSOR_MARGIN,
                        self.currButton.rect[2] - (2 * FastPadView.CURSOR_MARGIN),
                        self.currButton.rect[3] - (2 * FastPadView.CURSOR_MARGIN),
                        self.batch,                                                
                        color = FastPadView.CURSOR_COLOR,
                        fill = True,
                        )
                        
#        print ("Prev Mode = ", self.model.previous_mode)
#        print ("New Mode = ", self.model.mode)        
        # Set the new self.model.mode
        self.model.previous_mode = self.model.mode
    
