import os
import piexif

bot_key = 'a'

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

folder_config = 'config'
folder_img = 'img_input'
folder_out = 'img_output'

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
