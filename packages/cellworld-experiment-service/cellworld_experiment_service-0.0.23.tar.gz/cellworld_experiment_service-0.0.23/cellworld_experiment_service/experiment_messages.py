from json_cpp import JsonObject
from cellworld import *
from datetime import datetime

class StartExperimentRequest(JsonObject):
    def __init__(self, prefix: str = "", suffix: str = "", world: World_info = None, subject_name: str = "", duration: int = 0):
        self.prefix = prefix
        self.suffix = suffix
        if not world:
            world = World_info()
        self.world = world
        self.subject_name = subject_name
        self.duration = duration


class ResumeExperimentRequest(JsonObject):
    def __init__(self, experiment_name: str = "", duration_extension: int = 0):
        self.experiment_name = experiment_name
        self.duration_extension = duration_extension


class ResumeExperimentResponse(JsonObject):
    def __init__(self, experiment_name: str = "", start_date: datetime = None, world: World_info = None, subject_name: str = "", duration: int = 0, episode_count: int = 0):
        self.experiment_name = experiment_name
        if not start_date:
            start_date = datetime.now()
        self.start_date = start_date
        if not world:
            world = World_info()
        self.world = world
        self.subject_name = subject_name
        self.duration = duration
        self.episode_count = episode_count


class StartExperimentResponse(JsonObject):
    def __init__(self, experiment_name: str = "", start_date: datetime = None, world: World_info = None, subject_name: str = "", duration: int =0):
        self.experiment_name = experiment_name
        if not start_date:
            start_date = datetime.now()
        self.start_date = start_date
        if not world:
            world = World_info()
        self.world = world
        self.subject_name = subject_name
        self.duration = duration


class StartEpisodeRequest(JsonObject):
    def __init__(self, experiment_name: str = ""):
        self.experiment_name = experiment_name


class SetBehaviorRequest(JsonObject):
    def __init__(self, behavior: int = 0):
        self.behavior = behavior


class FinishExperimentRequest(JsonObject):
    def __init__(self, experiment_name: str = ""):
        self.experiment_name = experiment_name


class GetExperimentRequest(JsonObject):
    def __init__(self, experiment_name: str = ""):
        self.experiment_name = experiment_name


class GetExperimentResponse(JsonObject):
    def __init__(self, experiment_name: str = "", world_info: World_info = None, start_date: datetime = None, subject_name: str = "", duration: int = 0, remaining_time: float =0.0, episode_count: int=0):
        self.experiment_name = experiment_name
        if not world_info:
            world_info = World_info()
        self.world_info = world_info
        if not start_date:
            start_date = datetime.now()
        self.start_date = start_date
        self.subject_name = subject_name
        self.duration = duration
        self.remaining_time = remaining_time
        self.episode_count = episode_count

class CaptureRequest(JsonObject):
    def __init__(self, frame: int = 0):
        self.frame = frame
