"""
File Processes
"""
# Built-in
from app import Metadata
from os import path
from shutil import move

# Special

# App
from api.event import post_event
from .config import App

app = App()


def get_destination(metadata: Metadata):
    """
    Verify the destination folder is valid.
    """

    func = f"{__name__}.get_destination"

    metadata["destination"] = metadata["full_clipname"].replace(
        f"/{app.capture_folder_name}/", f"/{app.destination_folder_name}/"
    )

    if path.exists(metadata["destination"]):
        metadata["renamed"] = "True"
        print(f"file exists:{metadata['destination']}")
        directory = path.dirname(metadata["destination"])
        filename = path.splitext(path.basename(metadata["destination"]))[0]
        extension = path.splitext(path.basename(metadata["destination"]))[1]
        number = 1
        dest = path.join(directory, f"{filename}-{number:0>2d}{extension}")
        metadata["destination"] = dest
        print(f"Will now test with:{dest}")
        while path.exists(dest):
            number += 1
            dest = path.join(directory, f"{filename}-{number:0>2d}{extension}")
            print(f"Will now test with:{dest}")

        metadata["destination"] = dest

    post_event(
        "log_info",
        f"{func}",
        f"The destination is: {metadata['destination']} - was renamed: {metadata['renamed']}",
    )

    return metadata


def move_to_complete(metadata: Metadata):
    """
    Move the finished file into the Completed folder.
    """

    func = f"{__name__}.move_to_complete"

    metadata_updated = get_destination(metadata)
    moved = move(metadata["full_clipname"], metadata_updated["destination"])
    metadata_updated["destination"] = moved

    post_event(
        "log_info",
        f"{func}",
        f"The file was moved from: {metadata_updated['full_clipname']}",
    )
    post_event(
        "log_info",
        f"{func}",
        f"The file was moved to: {metadata_updated['destination']}",
    )

    return metadata_updated
