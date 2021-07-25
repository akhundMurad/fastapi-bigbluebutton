from datetime import datetime

from core.models.bigbluebutton import Meeting
from utils.tests import process_dict


class TestGetMeetings:
    def test_get_meetings_return_403(self, client):
        response = client.get('/bbb/')

        assert response.status_code == 403

    def test_get_meetings_status_code(self, client, auth_headers):
        response = client.get('/bbb/', headers=auth_headers)

        assert response.status_code == 200

    def test_get_meetings_content(self, client, auth_headers, test_meeting):
        response = client.get('/bbb/', headers=auth_headers)
        data = response.json()

        assert str(test_meeting.id) in [meeting['id'] for meeting in data]


class TestGetMeeting:
    def test_get_meeting_return_403(self, client, test_meeting):
        pk = str(test_meeting.id)
        response = client.get(f'/bbb/{pk}')

        assert response.status_code == 403

    def test_get_meeting_status_code(self, client, test_meeting,
                                     auth_headers):
        pk = str(test_meeting.id)
        response = client.get(f'/bbb/{pk}', headers=auth_headers)

        assert response.status_code == 200

    def test_get_meeting_content(self, client, test_meeting, auth_headers):
        pk = str(test_meeting.id)
        response = client.get(f'/bbb/{pk}', headers=auth_headers)
        data = response.json()

        assert data.get('id') == str(test_meeting.id)


class TestCreateMeeting:
    def test_create_meeting_return_403(self, client, test_meeting):
        data = test_meeting.dict(exclude={'id'})
        data = process_dict(data)

        response = client.post('/bbb/', json=data)

        assert response.status_code == 403

    def test_create_meeting_status_code(self, client, test_meeting,
                                        auth_headers):
        data = test_meeting.dict(exclude={'id'})
        data = process_dict(data)

        response = client.post('/bbb/', json=data,
                               headers=auth_headers)

        assert response.status_code == 201

    def test_create_meeting_content(self, client, test_meeting, auth_headers):
        data = test_meeting.dict(exclude={'id'})
        data = process_dict(data)

        response = client.post('/bbb/', json=data,
                               headers=auth_headers)

        meeting = Meeting(**response.json())
        assert meeting.id is not None

