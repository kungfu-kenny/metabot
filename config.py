import os
import piexif
from dotenv import load_dotenv

load_dotenv()

bot_key = os.getenv('BOT_KEY')

callback_separator = os.getenv('CALLBACK_SEPARATOR')

callback_data_show = os.getenv('CALLBACK_DATA_SHOW')
callback_data_update = os.getenv('CALLBACK_DATA_UPDATE')
callback_data_delete = os.getenv('CALLBACK_DATA_DELETE')

callback_data_show_un = os.getenv('CALLBACK_DATA_SHOW_UN')
callback_data_update_un = os.getenv('CALLBACK_DATA_UPDATE_UN')
callback_data_delete_un = os.getenv('CALLBACK_DATA_DELETE_UN')

callback_data_show_f = os.getenv('CALLBACK_DATA_SHOW_F') #750f3081-7ff4-472c-b1c2-dca32c09550c
callback_data_delete_f = os.getenv('CALLBACK_DATA_DELETE_F') #d688bfa1-5937-4f64-bfe5-8ff28ed8ee94
callback_data_update_f = os.getenv('CALLBACK_DATA_UPDATE_F') #326839a7-4f85-4c51-ac36-cd9e6e32c601

ifd_zeroth = {
            piexif.ImageIFD.Make: u"Our daddy told us not to be ashamed of our dicks",
            piexif.ImageIFD.XResolution: (300, 1),
            piexif.ImageIFD.YResolution: (300, 1), 
            piexif.ImageIFD.Software: u"Sorry for what?"
            }

ifd_exif = {
            piexif.ExifIFD.DateTimeOriginal: u"2077:99:99 44:44:00",
            piexif.ExifIFD.LensMake: u"I'm sorry",
            piexif.ExifIFD.Sharpness: 300,
            piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),
            }
ifd_gps = {
           piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
           piexif.GPSIFD.GPSAltitudeRef: 1,
           piexif.GPSIFD.GPSDateStamp: u"2000:99:99 44:44:00",
           }
ifd_first = {
             piexif.ImageIFD.Make: u"I rip the skin",
             piexif.ImageIFD.XResolution: (300, 1),
             piexif.ImageIFD.YResolution: (300, 1),
             piexif.ImageIFD.Software: u"Hhhhmmmm"
             }


ifd_zeroth_exp = {
            271:['piexif.ImageIFD.Make', 'Make', 'str'],
            282:['piexif.ImageIFD.XResolution', 'X Resolution', 'tuple of int'],
            283:['piexif.ImageIFD.YResolution', 'Y Resolution', 'tuple of int'],
            305:['piexif.ImageIFD.Software', 'Software', 'str'],
            }

ifd_exif_exp = {
            36867:['piexif.ExifIFD.DateTimeOriginal', 'Date Time Original', 'str'],
            42035:['piexif.ExifIFD.LensMake', 'Lens Make', 'str'],
            41994:['piexif.ExifIFD.Sharpness', 'Sharpness', 'int'], 
            42034:['piexif.ExifIFD.LensSpecification', 'Lens Specification', 'tuple of tuples with int (4x2)']
            }

ifd_gps_exp = {
           0:['piexif.GPSIFD.GPSVersionID', 'GPS Version ID', 'tuple of int'],
           5:['piexif.GPSIFD.GPSAltitudeRef', 'GPS Altitude Ref', 'int'],
           29:['piexif.GPSIFD.GPSDateStamp', 'GPS DateStamp', 'str'],
           }

ifd_first_exp = {
             271: ['piexif.ImageIFD.Make', 'Make', 'str'],
             282: ['piexif.ImageIFD.XResolution', 'X Resolution', 'tuple of int'],
             283: ['piexif.ImageIFD.YResolution', 'Y Resolution', 'tuple of int'],
             305: ['piexif.ImageIFD.Software', 'Software', 'str']
             }

json_name = 'settings.json'
json_name_translate = 'check_changes.json'
json_keys_default = {"0th": ifd_zeroth, "Exif": ifd_exif, "GPS": ifd_gps, "1st": ifd_first, "thumbnail": None}
json_keys_translate = {"0th": ifd_zeroth_exp, "Exif": ifd_exif_exp, "GPS": ifd_gps_exp, "1st": ifd_first_exp, "thumbnail": None}

list_image_ext = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')

folder_config = 'config'
folder_img = 'img_input'
folder_out = 'img_output'
folder_tmp = 'img_tmp'
folder_tmp_uncompressed = 'img_tmp_uncompressed'

args_deletion_necessary = ('-n', '--necessary', 'argument which is dedicated to delete original images after the work with them', 'store_true', False)
args_update_json = ('-u', '--update', 'argument which is dedicated to update the json value from the config', 'store_true', False)
args_analyse_pictures = ('-a', '--analyse', 'argument which is dedicated to analyse pictures of the inserted and return values to the file', 'store_true', False)
args_recheck_upd = ('-r', '--recheck', 'argument which is dedicated to show the user that we successfully changed the metadata about all pictures', 'store_true', False) 
args_recheck_rem = ('-o', '--observe', 'argument which is dedicated to show the user that we successfully removed the metadata about all pictures', 'store_true', False)
args_change_meta = ('-c', '--change', 'argument which is dedicated to remove the metadata and change to json values', 'store_true', False)
args_delete_meta = ('-d', '--delete', 'argument which is dedicated to remove all metadata', 'store_true', False)
args_use_selected = ('-s', '--selected', 'argument which is dedicated to use only selected pictures which were listed via comma(,); with or without extension', str, False, '')
description = 'This is a module to deal with the images and their metadata. It creates folders for input of the pictures and the config folder if user wants to ' +\
            'change the metadata in his own selection. Also, it contains another JSON to show what keys user can change. User is allowed to select what images he wants to use, ' +\
            'see metadata of selected values in the input, update its metadata to the selected one; remove metadata from it at all'    
