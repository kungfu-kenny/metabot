import os
import io
from PIL import Image
from uuid import uuid4
from image_parser import ImageParser
from config import (list_image_ext,
                    folder_tmp,
                    folder_tmp_uncompressed)


class TelegramUsage:
    """
    class which is dedicated to work with telegram files
    """
    def __init__(self) -> None:
        self.folder_current = os.getcwd()
        self.folder_tmp = os.path.join(self.folder_current, folder_tmp)
        self.folder_tmp_unc = os.path.join(self.folder_current, folder_tmp_uncompressed)
        self.create_folder = lambda x: os.path.exists(x) or os.mkdir(x)
        self.create_name_tmp = lambda: f"{uuid4()}.jpg"
        self.create_name_unc = lambda x: f"{uuid4()}{x}"

    def detect_less_compressed(self, file_list:list) -> str:
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
        return used_name

    @staticmethod
    def detect_image_ext(value_name:str) -> bool:
        """
        Static method which is dedicated to work with the extention of the files
        Input:  value_name = name of selected files
        Output: True if it has image extention else False
        """
        return value_name.lower().endswith(list_image_ext)

    def detect_image_value(self, bytes_io:object) -> bool:
        """
        Method which is dedicated to detect the mage from the inserted bytes of the text
        Input:  bytes_io = bytes from the telegram which were sent via message
        Output: True if it is image else False
        """
        try:
            im = Image.open(io.BytesIO(bytes_io))
            im.verify()
            im.close()
            return True
        except Exception as e:
            return False

    def detect_usage_location(self, value_name_ext:str, value_type:str) -> set:
        """
        Method which is dedicated to return 
        Input:  value_name_ext = name of the temporary value without ext
                value_type = type of the inserted value
        Output: returned name and it's path
        """
        if value_type == 1:
            a = 2
        return 0, 0

    def save_tmp_file(self, bytes_io:bytes, value_compressed:bool=True, value_ext:str='') -> str:
        """
        Method which is dedicated to save the compressed picture from the telegram
        Input:  bytes_io = byte value of the sent picture
        Output: we successfully saved temporary image and returned name of it
        """
        new_image = Image.open(io.BytesIO(bytes_io))
        folder_used = self.folder_tmp if value_compressed else self.folder_tmp_unc
        if value_compressed and not value_ext: 
            value_name = self.create_name_tmp()
        else: 
            value_name = self.create_name_unc(value_ext)
        self.create_folder(folder_used)
        new_image.save(os.path.join(folder_used, value_name))
        return value_name

    