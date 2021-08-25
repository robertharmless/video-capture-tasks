"""
Metadata from Just In Capture task.
"""


class Metadata:
    """
    Metadata from Just In Capture task.
    """

    alert_type = None
    renamed = None
    script_start_time = None
    # video related variables
    full_clipname = None
    clipname = None
    timecode_source = None
    container = None
    framerate = None
    aspect_ratio = None
    capture_codec = None
    audio_channels = None
    capture_resolution = None
    capture_width = None
    capture_height = None
    capture_duration = None
    inpoint = None
    outpoint = None

    def __init__(self, **args) -> None:
        self.alert_type = args[1]
        self.renamed = "False"
        # video related variables
        self.full_clipname = args[2]
        self.clipname = args[3]
        self.timecode_source = args[4]
        self.container = args[5]
        self.framerate = args[6]
        self.aspect_ratio = args[7]
        self.capture_codec = args[8]
        self.audio_channels = args[9]
        self.capture_resolution = args[10]
        self.capture_width = args[11]
        self.capture_height = args[12]
        self.capture_duration = args[13]
        self.inpoint = args[14]
        self.outpoint = args[15]
