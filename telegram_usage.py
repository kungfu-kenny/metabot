import os
import io
from PIL import Image
from uuid import uuid4
from image_parser import ImageParser
from config import (folder_tmp)


class TelegramUsage:
    """
    class which is dedicated to work with telegram files
    """
    def __init__(self) -> None:
        self.folder_current = os.getcwd()
        self.folder_tmp = os.path.join(self.folder_current, folder_tmp)
        self.create_folder = lambda x: os.path.exists(x) or os.mkdir(x)
        self.create_name_tmp = lambda: f"{uuid4()}.jpg"

    def detect_less_compressed(self, file_list:list) -> set:
        """
        Method which is dedicated to detect less compressed file out of them and
        Input:  file_list = list with the files
        Output: string of the least compressed file
        """
        value_lists = []
        for file_name in file_list:
            file_location = os.path.join(self.folder_tmp, file_name) 
            value_lists.append((os.stat(file_location).st_size, file_name, file_location))
        _, used_name, used_location = sorted(value_lists, key=lambda x: x[0])[-1]
        for _, file_name, file_location in value_lists:
            if file_name != used_name and file_location != used_location:
                os.remove(file_location)
        return (used_name, used_location)

    @staticmethod
    def detect_image_ext(value_name:str) -> bool:
        """
        Static method which is dedicated to work with the extention of the files
        Input:  value_name = name of selected files
        Output: True if it has image extention else False
        """
        pass

    def detect_image_value(self, bytes_io:object) -> bool:
        """
        Method which is dedicated to detect the mage from the inserted bytes of the text
        Input:  bytes_io = bytes from the telegram which were sent via message
        Output: True if it is image else False
        """
        pass

    def save_tmp_file(self, bytes_io:object) -> str:
        """
        Method which is dedicated to save the compressed picture from the telegram
        Input:  bytes_io = byte value of the sent picture
        Output: we successfully saved temporary image and returned name of it
        """
        new_image = Image.open(io.BytesIO(bytes_io))
        value_name = self.create_name_tmp()
        self.create_folder(self.folder_tmp)
        new_image.save(os.path.join(self.folder_tmp, value_name))
        return value_name

    