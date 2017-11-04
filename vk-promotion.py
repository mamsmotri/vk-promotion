# -*- coding: utf-8 -*-
import vk_api
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def main():

    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("vk-promotion").sheet1
    post_data = client.open("vk-promotion").get_worksheet(1)

    full_group_links = sheet.col_values(1)

    login = post_data.cell(7, 3).value
    print (login)
    password = post_data.cell(8, 3).value
    print (password)

    post_text = post_data.cell(2, 3).value
    post_photos = 'photo' + post_data.cell(3, 3).value
    post_audios = 'audio' + post_data.cell(4, 3).value
    post_audio_playlist = 'audio_playlist-64592951_1'
    post_attachments = post_photos + ", " + post_audios
    print (post_attachments)

    print(full_group_links)

    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    for full_group_link in full_group_links:
        if full_group_link == '':
            continue
        group_short_name = full_group_link[15:]
        print (group_short_name)

        group = vk.groups.getById(group_ids=group_short_name)
        group_id = -group[0]['id']
        response = vk.wall.post(owner_id=group_id, message=post_text, attachments=post_audio_playlist)



if __name__ == '__main__':
    main()