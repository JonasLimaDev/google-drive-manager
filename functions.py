import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from magic import Magic

def logar_drive():
    g_login = GoogleAuth()
    g_login.LocalWebserverAuth()
    drive = GoogleDrive(g_login)
    return drive


def upload_drive(local):
    drive = logar_drive()
    file = open(local)
    file_name = os.path.basename(file.name)
    info_mime = Magic(mime=True)
    file_drive = drive.CreateFile({'title': file_name, 'mimeType': info_mime.from_file(local) })
    file_drive.SetContentFile(local)
    file_drive.Upload()
    permission = file_drive.InsertPermission({
                            'type': 'anyone',
                            'value': 'anyone',
                            'role': 'reader'})
    return file_drive['alternateLink']


def send_file_folder(selected_folder):
    data_list_files = os.walk(selected_folder)
    for file_data in data_list_files:
        for current_file in file_data[2]:
            current_path_file = f"{file_data[0]}/{current_file}" 
            if os.path.isfile(current_path_file):
                upload_drive(current_path_file)