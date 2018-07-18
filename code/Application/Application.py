import logging, os
import MotionStartDetector, UserHandler, MotionTimeUserMatching, CutExtractor

logger = logging.getLogger(__name__)  #Set logger to reflect the current file

class Application:
    def __init__(self):
        logger.debug("Appliation created")
        self.motion_start_detector = MotionStartDetector.MotionStartDetector()
        self.user_handler = UserHandler.UserHandler()
        self.motion_time_user_matching = MotionTimeUserMatching.MotionTimeUserMatching()
        self.full_clip_cut_extractor = CutExtractor.CutExtractor()

    def run(self, arg_input_video_folder, arg_user_root_folder, arg_selection):
        logger.info("Running Application with video folder: " + arg_input_video_folder + " user folder: " + arg_user_root_folder + "\n")
        if not os.path.exists(arg_input_video_folder):
            raise ValueError("Video folder is not a valid folder: " + arg_input_video_folder)
        if not os.path.exists(arg_user_root_folder):
            raise ValueError("User folder is not a valid folder: " + arg_user_root_folder)

        if 0 in arg_selection:
            self.motion_start_detector.create_motion_start_files(arg_input_video_folder)

        if 1 in arg_selection:
            self.user_handler.init(arg_user_root_folder)

        if 2 in arg_selection:
            self.motion_time_user_matching.match_motion_start_times_with_users(arg_input_video_folder, self.user_handler)

        if 3 in arg_selection:
            clip_specification_list = self.user_handler.create_full_clip_specifications()
            self.full_clip_cut_extractor.extract_full_clip_specifications(clip_specification_list)
