import tkinter as tk
import os
import math
import simpleaudio as sa

class musicbutton():
    def __init__(self, Songframe, element, title, gui):
        self.title = title
        self.element = element
        Musicbutton = tk.Button(Songframe, text=self.title[0:len(self.title)-4], font=("Helvetica", gui.fontsize))
        Musicbutton.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        Musicbutton.bind('<Button-1>', lambda e:
            gui.playmusic(self.element))

class dirbutton():
    def __init__(self, FolderFrame, directory):
        self.directory = directory
        dir_button = tk.Button(FolderFrame, text=self.directory, height="1", font=("Helvetica", 17), command=lambda:
            gui.SwitchDirectory(self.directory))
        dir_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

class soundInfo():
    def __init__(self, element, title):
        self.title = title
        self.element = element

class Application(tk.Frame, object):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.pack()
        self.play_obj = 0
        self.playlist = []
        self.shift = False
        self.loadDirectories()
        if(len(self.directories) > 0):
            self.setDirectory(self.directories[0])
        else:
            self.setDirectory("")
        self.loadSongs()
        self.createFrames()
        self.createFolders()
        self.createMenu()
        self.createSongbuttons()

    def loadDirectories(self):
        self.directories = next(os.walk('.'))[1]

    def setDirectory(self, directory):
        self.directory = directory
        print(self.directory)

    def loadSongs(self):
        self.listofsounds = []
        listlength = 0
        if (self.directory != ""):
            for file in os.listdir(self.directory):
                if file.endswith(".wav"):
                    wave_obj = sa.WaveObject.from_wave_file(self.directory + "/" + file)
                    s = soundInfo(wave_obj, file)
                    self.listofsounds.append(s)
                    listlength += 1

        self.Framenum = math.ceil(math.sqrt(listlength)/2)
        if(self.Framenum == 0):
            self.Songnum = 0
        else:
            self.Songnum = math.ceil(listlength/self.Framenum)

    def createFrames(self):
        self.FolderFrame = tk.Frame(self)
        self.FolderFrame.pack(side=tk.TOP, fill=tk.X, expand=0)
        self.Menu = tk.Frame(self)
        self.Menu.pack(side=tk.TOP, fill=tk.X, expand=0)
        self.SoundboardTopFrame = tk.Frame(self)
        self.SoundboardTopFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.playlistlabel = tk.Label(self,
                                      text="Dit soundboard is medemogenlijk geklust door uw commissaris evenementen, Mark van der Smagt. Ratatoele 14'15'",
                                      height="1", font=("Helvetica", 5))
        self.playlistlabel.pack(side=tk.TOP, fill=tk.X, expand=0)
        self.update()
        self.SoundboardBottomFrame = tk.Frame(self.SoundboardTopFrame)
        self.SoundboardBottomFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def createFolders(self):
        for element in self.directories:
            dirbutton(self.FolderFrame, element)

    def createMenu(self):
        self.ShiftButton = tk.Button(self.Menu, text="Layer Sounds (shift)", height="2", font=("Helvetica", 25),
                                     command=self.ToggleShift)
        self.ShiftButton.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.CtrlButton = tk.Button(self.Menu, text="Remove last layer (ctrl)", height="2", font=("Helvetica", 25),
                                    command=self.ControlPress)
        self.CtrlButton.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.silencebutton = tk.Button(self.Menu, text="Remove all Layers", height="2", font=("Helvetica", 25),
                                       command=self.SilenceSound)
        self.silencebutton.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.reloadButton = tk.Button(self.Menu, text="Reload Songs", height="2", font=("Helvetica", 25),
                                      command=self.reloadSongs)
        self.reloadButton.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.closebutton = tk.Button(self.Menu, text="close", height="3", font=("Helvetica", 25),
                                     command=self.exitProgram)
        self.closebutton.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


    def createSongbuttons(self):
        self.fontsize = int((self.SoundboardBottomFrame.winfo_height() / max(self.Songnum, 1)) / 4)
        for number in range(0, self.Framenum):
            Songframe = tk.Frame(self.SoundboardBottomFrame)
            Songframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

            for element in self.listofsounds[(number)*self.Songnum:((number)*self.Songnum)+self.Songnum]:
                musicbutton(Songframe, element.element, element.title, self)

    def playmusic(self, wave_obj):
        print(wave_obj)
        print("playmusic")
        if self.shift == False:
            for element in self.playlist:
                element.stop()
            self.playlist = []

        self.play_obj = wave_obj.play()
        self.playlist.append(self.play_obj)

    def onShiftPress(self, event):
        self.shift = True
        self.ShiftButton.config(relief="sunken")

    def onShiftRelease(self, event):
        self.shift = False
        self.ShiftButton.config(relief="raised")

    def ToggleShift(self):
        if self.shift == False:
            self.shift = True
            self.ShiftButton.config(relief="sunken")
        else:
            self.shift = False
            self.ShiftButton.config(relief="raised")

    def reloadSongs(self):
        self.SoundboardBottomFrame.destroy()
        self.loadSongs()
        self.SoundboardBottomFrame = tk.Frame(self.SoundboardTopFrame)
        self.SoundboardBottomFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.createSongbuttons()

    def ControlPress(self):
        if len(self.playlist) > 0:
            self.playlist[len(self.playlist)-1].stop()
            self.playlist = self.playlist[0:len(self.playlist)-1]

    def onControlPress(self, event):
        if len(self.playlist) > 0:
            self.playlist[len(self.playlist)-1].stop()
            self.playlist = self.playlist[0:len(self.playlist)-1]

    def exitProgram(self):
        root.destroy()

    def SilenceSound(self):
        for element in self.playlist:
            element.stop()
        self.playlist = []

    def SwitchDirectory(self, directory):
        self.setDirectory(directory)
        self.reloadSongs()


root = tk.Tk()
root.attributes("-fullscreen", False)
gui = Application(root)
gui.pack(fill=tk.BOTH, expand=1)
root.bind('<KeyPress-Shift_L>', gui.onShiftPress)
root.bind('<KeyRelease-Shift_L>', gui.onShiftRelease)
root.bind('<KeyPress-Control_L>', gui.onControlPress)
root.mainloop()





