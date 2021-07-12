import json
import httpx
from functools import cached_property
from hashlib import sha1
from typing import Optional, Dict, List
from urllib.parse import urlencode

import xmltodict
from requests import RequestException

from core import settings
from core.models.bigbluebutton import Meeting
from core.models.users import User, UserRoleChoices
from core.schemas.bigbluebutton import BigbluebuttonServer


class ServerAPI:
    _server: Optional[BigbluebuttonServer] = None

    meetings: Dict[str, Meeting]

    @property
    def server(self) -> BigbluebuttonServer:
        if not self._server:
            self._server = BigbluebuttonServer(
                name=settings.BBB_SERVER_NAME,
                url=settings.BBB_SERVER_URL,
                secret_key=settings.BBB_SECRET_KEY
            )
        return self._server

    def get_checksum(self, api_method: str, query: str) -> str:
        hash_str = api_method + query + self._server.secret_key
        checksum = sha1(hash_str.encode()).hexdigest()
        return checksum

    def get_url(self, api_method: str, params: dict = None) -> str:
        query = urlencode(params or {})
        query += "&checksum=" + self.get_checksum(api_method, query)
        url = f'{self._server.url}{api_method}?{query}'
        return url

    async def create_meeting(self, **kwargs) -> dict:
        api_method = 'create'
        params = kwargs['kwargs']
        response = await self.request(api_method, params)

        return response

    async def request(self, api_method: str, params: dict = None) -> dict:
        with httpx.AsyncClient() as client:
            response = await client.get(self.get_url(api_method, params))

        if response.status_code != 200:
            raise RequestException(
                f'Ошибка с отправкой запроса на сервер. {response.status_code}'
            )

        response_content = xmltodict.parse(response.text)
        response_dict = json.loads(json.dumps(response_content))
        return response_dict.get('response')

    async def refresh(self):
        await self.get_meetings()

    async def get_meetings(self) -> None:
        api_method = 'getMeetings'
        response = await self.request(api_method)
        _meetings = self.meetings

        if response["meetings"] is None:
            _meetings = {}

        if not isinstance(response["meetings"]["meeting"], list):
            response["meetings"]["meeting"] = [response["meetings"]["meeting"]]

        for meeting in response["meetings"]['meeting']:
            meeting_id = meeting['meetingID']
            del meeting["meetingID"]
            _meetings[meeting_id] = meeting

        self.meetings = _meetings


class MeetingAPI:
    meeting: Meeting

    _server_api: Optional[ServerAPI] = None

    @property
    def server_api(self) -> ServerAPI:
        if not self._server_api:
            self._server_api = ServerAPI()
        return self._server_api

    @cached_property
    def data(self) -> dict:
        _meeting_data = self.meeting.dict()
        return {
            'meetingID': _meeting_data.get('id'),
            'name': _meeting_data.get('name'),
            'welcome': _meeting_data.get('welcome_message'),
            'moderatorOnlyMessage': _meeting_data.get('moderator_message'),
            'record': _meeting_data.get('record'),
            'autoStartRecording': _meeting_data.get('auto_start_recording'),
            'allowStartStopRecording': _meeting_data.get('allow_start_stop_recording'),
            'webcamsOnlyForModerator': _meeting_data.get('webcams_only_for_moderator'),
            'muteOnStart': _meeting_data.get('mute_on_start'),
            'allowModsToUnmuteUsers': _meeting_data.get('allow_mods_to_unmute_users'),
            'maxParticipants': _meeting_data.get('max_participants'),
            'duration': _meeting_data.get('duration')
        }

    def is_meeting_exists(self) -> bool:
        return self.meeting.id in self.server_api.meetings.keys()

    async def create(self) -> dict:
        response = await self.server_api.create_meeting(
            **self.data
        )
        return response

    async def is_meeting_running(self) -> dict:
        api_method = 'isMeetingRunningAnchor'
        params = {'meetingID': self.meeting.id}
        response = await self._server_api.request(api_method, params)

        return response

    async def end(self) -> dict:
        api_method = 'end'
        params = {
            'meetingID': self.meeting.id,
            'password': settings.BBB_MOD_PW
        }
        response = await self._server_api.request(api_method, params)

        return response

    async def get_meeting_info(self) -> dict:
        api_method = 'getMeetingInfo'
        params = {'meetingID': self.meeting.id}
        response = await self._server_api.request(api_method, params)

        return response

    def join(self, user: User) -> str:
        api_method = 'join'
        params = {
            'meetingID': self.meeting.id,
            'fullName': user.first_name + ' ' + user.last_name,
            'password': self._get_password(user),
            'userID': user.id
        }
        return self.server_api.get_url(api_method, params)

    @staticmethod
    def _get_password(user):
        if user.role == UserRoleChoices.MODERATOR.value:
            return settings.BBB_MOD_PW
        return settings.BBB_ATTENDEE_PW
