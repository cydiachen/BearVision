from tkinter import *
from tkinter import filedialog
import os, logging
from ConfigurationHandler import ConfigurationHandler

logger = logging.getLogger(__name__)

#pa_default_input_video_folder = "test/input_video"
#pa_default_user_folder = "test/users"

command_list = ["Generate motion start files",
                "Initialize users",
                "Match user locations to motion files",
                "Generate output videos"]


class BearVisionGUI:
    def __init__(self, arg_master, arg_app_ref):
        tmp_options = ConfigurationHandler.get_configuration()
        self.master = arg_master
        self.app_ref = arg_app_ref
        self.master.title("BearVision - WakeVision")
        self.master.geometry("500x500")

        self.welcome_label = Label(self.master, text="BearVision - WakeVison", bg='red', font=('Helvetica', '20'))
        self.welcome_label.pack(fill=X, side=TOP)

        self.folder_selection_frame = Frame(self.master)
        self.folder_selection_frame.pack(fill=X, pady=10, side=TOP)
        self.folder_selection_frame.columnconfigure(0, weight=3)
        self.folder_selection_frame.columnconfigure(1, weight=1)

        self.video_folder_text = StringVar()
        if tmp_options is not None:
            self.video_folder_text.set( os.path.abspath(tmp_options['GUI']['video_path']) )
        self.video_folder_entry = Entry(self.folder_selection_frame, textvariable=self.video_folder_text)
        self.video_folder_entry.grid(row=0, column=0, sticky=W+E)
        self.video_folder_button = Button(self.folder_selection_frame, text="Select input video folder", command=self.set_input_video_folder)
        self.video_folder_button.grid(row=0, column=1, sticky=W+E)

        self.user_folder_text = StringVar()
        if tmp_options is not None:
            self.user_folder_text.set( os.path.abspath(tmp_options['GUI']['user_path']) )
        self.user_folder_entry = Entry(self.folder_selection_frame, textvariable=self.user_folder_text, width=60)
        self.user_folder_entry.grid(row=1, column=0, sticky=W+E)
        self.user_folder_button = Button(self.folder_selection_frame, text="Select user base folder", command=self.set_user_folder)
        self.user_folder_button.grid(row=1, column=1, sticky=W+E)

        self.run_options = Listbox(self.master, selectmode=MULTIPLE )
        for command_entry in command_list:
            self.run_options.insert(END, command_entry)

        self.run_options.pack(fill=X, pady=10)
        self.run_options.selection_set(0,self.run_options.size())  # select all options

        self.config_load_button = Button(self.master, text="Load Config", command=self.load_config, bg='green3', height=1, width=10, font=('Helvetica', '20'))
        self.config_load_button.pack(side=LEFT)

        self.run_button = Button(self.master, text="Run", command= self.run, bg='green3', height = 1, width = 10, font=('Helvetica', '20'))
        self.run_button.pack(side=RIGHT)

        self.status_label_text = StringVar()
        self.status_label_text.set("Ready")
        if tmp_options is None:
            self.status_label_text.set("No parameters")
        self.status_label = Label(self.master, textvariable=self.status_label_text, bg='yellow', font=('Helvetica', '20'))
        self.status_label.pack(fill=X, side=BOTTOM, pady=10)

    def set_input_video_folder(self, arg_directory_path=None):
        if arg_directory_path is None:
            arg_directory_path = filedialog.askdirectory()
        self.video_folder_text.set(arg_directory_path)
        logger.info("Setting input video folder to: " + arg_directory_path)

    def set_user_folder(self, arg_directory_path=None):
        if arg_directory_path is None:
            arg_directory_path = filedialog.askdirectory()
        self.user_folder_text.set(arg_directory_path)
        logger.info("Setting user folder to: " + arg_directory_path)

    def run(self):
        logger.debug("run()")
        tmp_options = ConfigurationHandler.get_configuration()
        if tmp_options is None:
            self.status_label_text.set("No parameters")
            return
        self.status_label_text.set("Busy")
        self.status_label.update()
        # print("Running selections: " + str(self.run_options.curselection()))
        self.app_ref.run(self.video_folder_text.get(), self.user_folder_text.get(), self.run_options.curselection())
        self.status_label_text.set("Ready")

    def load_config(self):
        logger.debug("load_config()")
        tmp_config_file = filedialog.askopenfilename()
        tmp_options = ConfigurationHandler.read_config_file(tmp_config_file)

        # update file selection boxes and GUI
        self.set_input_video_folder(tmp_options['GUI']['video_path'])
        self.set_user_folder(tmp_options['GUI']['user_path'])
        self.status_label_text.set("Ready")






#GUI_root = Tk()
#my_gui = BearVisionGUI(GUI_root)
#GUI_root.mainloop()
