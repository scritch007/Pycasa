import gdata.photos.service
import gdata.media
import gdata.geo
import os

import mimetypes


import gdata.photos.service

# Grabbed from
# http://code.google.com/intl/de-DE/apis/picasaweb/docs/2.0/developers_guide_protocol.html
valid_mimetypes = [
'image/bmp',
'image/gif',
'image/jpeg',
'image/png',
'video/3gpp',
'video/avi',
'video/quicktime',
'video/mp4',
'video/mpeg',
'video/mpeg4',
'video/msvideo',
'video/x-ms-asf',
'video/x-ms-wmv',
'video/x-msvideo'
]

# Hack because python gdata client does not accept videos?!
for mtype in valid_mimetypes:
  mayor, minor = mtype.split('/')
  if mayor == 'video':
    gdata.photos.service.SUPPORTED_UPLOAD_TYPES += (minor,)



def debug(string):
    print string

class SyncPicassa(object):

    def __init__(self, userid, password):
        self.userid = userid
        self.password = password
        self.gd_client = gdata.photos.service.PhotosService()
        self.gd_client.email = self.userid
        self.gd_client.password = self.password
        #self.gd_client.source = 'exampleCo-exampleApp-1'
        self.gd_client.source = 'sync_picassa'
        self.gd_client.ProgrammaticLogin()

    def sync_folder(self, folder_name):
        """
        @folder_name, the main folder. Each direct sub folder will be synchronized
        as a new album
        """

        albums = self.gd_client.GetUserFeed()
        album_dict = {}
        for album in albums.entry:
            album_dict[album.title.text] = album
        for l_album in os.listdir(folder_name):
            debug("Found folder %s" % l_album)
            l_album_path = os.path.join(folder_name, l_album)
            if os.path.isdir(l_album_path):
                if l_album not in album_dict:
                    debug("Album not in Picassa %s" % l_album)
                    new_album = self.gd_client.InsertAlbum(title=l_album,
                            summary="Sync of local folder", access='private')
                    album_dict[l_album] = new_album

                album = album_dict[l_album]
                photos = self.gd_client.GetFeed(
                        '/data/feed/api/user/%s/albumid/%s?kind=photo' % (
                            "default", album.gphoto_id.text))
                photos = [photo.title.text for photo in photos.entry]

                for file_name in os.listdir(l_album_path):
                    file_path = os.path.join(l_album_path, file_name)
                    if os.path.isfile(file_path):
                        file_mime_type = mimetypes.guess_type(file_name)
                        if file_mime_type[0].startswith("image/") or file_mime_type[0].startswith("video/"):
                            if not file_name in photos:
                                debug("Adding file %s to album" % file_name)
                                album_url = '/data/feed/api/user/%s/albumid/%s' % ("default", album.gphoto_id.text)
                                photo = self.gd_client.InsertPhotoSimple(album_url,
                                        file_name,
                                    'Uploaded using the API', file_path,
                                    content_type=file_mime_type[0])


