import logging, os, re, csv, datetime


logger = logging.getLogger(__name__)

motion_file_ending = "_motion_start_times"
motion_file_ending_regex = re.compile(".+" + motion_file_ending + "\.csv$")

motion_start_time_entry_regex = re.compile("\d{8}\_\d{2}\_\d{2}\_\d{2}")


class MotionFilesHandler:
    def __init__(self):
        return

    @staticmethod
    def has_associated_motion_file(arg_motion_file_list, arg_video_file):
        logger.debug("Checking if motion file already exists for file: " + arg_video_file.name)
        for motion_file in arg_motion_file_list:  # look through all found motion files for a match
            # logger.debug("Matching: " + motion_file.name + " and " + os.path.splitext(arg_video_file.name)[0] + motion_file_ending + ".csv")
            if motion_file.name == os.path.splitext(arg_video_file.name)[0] + motion_file_ending + ".csv":
                return True

        return False  #Not match found

    @staticmethod
    def get_motion_file_list(arg_input_video_folder):
        motion_file_list = []
        for dir_file in os.scandir(arg_input_video_folder):
            # logger.debug("Checking if the following file is a motion start file: " + dir_file.name)
            if motion_file_ending_regex.match(dir_file.name):
                logger.debug("Motion start file found: " + dir_file.name)
                motion_file_list.append(dir_file)

        return motion_file_list  # list of found motion files

    @staticmethod
    def read_motion_file(arg_motion_file):
        logger.debug("Reading motion file: " + arg_motion_file.path)
        csv_file = open(arg_motion_file, 'r', newline='')
        file_reader = csv.reader(csv_file)
        motion_start_times_list = []
        for row in file_reader:  # row is here a list
            for entry in row:
                if motion_start_time_entry_regex.match(entry):
                    #print("Matching entry: " + entry)
                    motion_start_time = datetime.datetime.strptime(entry, "%Y%m%d_%H_%M_%S")
                    motion_start_times_list.append(motion_start_time)
                    logger.debug("Motion time for readout of file: " + arg_motion_file.path + " : " + motion_start_time.strftime("%Y%m%d_%H_%M_%S"))

        return motion_start_times_list  # list of datetimes

    @staticmethod
    def write_motion_file(arg_video_file, arg_motion_start_times_list):
        output_filename_short = os.path.splitext(arg_video_file.name)[0] + motion_file_ending + ".csv"
        output_dir = os.path.dirname(arg_video_file.path)
        output_filename = os.path.join(output_dir, output_filename_short)

        logger.debug("Writing motion file: " + output_filename + "with " + str(len(arg_motion_start_times_list)) + " entries")
        csv_file = open(output_filename, 'w', newline='')
        output_writer = csv.writer(csv_file)

        for start_time in arg_motion_start_times_list:
            start_time_str = start_time.strftime("%Y%m%d_%H_%M_%S")
            output_writer.writerow([start_time_str])

        logger.debug("Finished writing motion file: " + output_filename)
        return True  # true for success