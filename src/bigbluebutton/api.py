import json
from functools import cached_property
from hashlib import sha1
from typing import Dict, Optional
from urllib.parse import urlencode

import httpx
import xmltodict
from fastapi import Depends
from requests import RequestException

from src.api.dependencies.settings import settings_provider
from src.core.settings import Settings
from src.db.choices import UserRoleChoices
from src.schemas.bigbluebutton import BigbluebuttonServer, MeetingRead
from src.main import app


__all__ = ["MeetingAPI", "ServerAPI"]


class ServerAPI:
    def __init__(self, settings: Settings = Depends(settings_provider)):
        self._server: Optional[BigbluebuttonServer] = None
        self.meetings: Dict[str, MeetingRead]
        self.settings = settings

    async def __aenter__(self):
        meetings = await app.state.redis.get(f"{self.server.url}::meetings")
        try:
            self.meetings = json.loads(meetings)
        except TypeError:
            self.meetings = {}
        return self

    async def __aexit__(self, *excinfo):
        meetings = json.dumps(self.meetings)
        await app.state.redis.set(f"{self.server.url}::meetings", meetings)

    @property
    def server(self) -> BigbluebuttonServer:
        if not self._server:
            self._server = BigbluebuttonServer(
                name=self.settings.bbb_server_name,
                url=self.settings.bbb_server_url,
                secret_key=self.settings.bbb_secret_key,
            )
        return self._server

    def get_checksum(self, api_method: str, query: str) -> str:
        hash_str = api_method + query + self._server.secret_key
        checksum = sha1(hash_str.encode()).hexdigest()
        return checksum

    def get_url(self, api_method: str, params: dict = None) -> str:
        query = urlencode(params or {})
        query += "&checksum=" + self.get_checksum(api_method, query)
        url = f"{self._server.url}{api_method}?{query}"
        return url

    async def create_meeting(self, **params) -> dict:
        api_method = "create"
        response = await self.request(api_method, params)

        await self.refresh()

        return response

    async def request(self, api_method: str, params: dict = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.get_url(api_method, params))

        if response.status_code != 200:
            raise RequestException(
                f"Ошибка с отправкой запроса на сервер. {response.status_code}"
            )

        response_content = xmltodict.parse(response.text)
        response_dict = json.loads(json.dumps(response_content))
        return response_dict.get("response")

    async def refresh(self):
        await self.get_meetings()

    async def get_meetings(self) -> None:
        api_method = "getMeetings"
        response = await self.request(api_method)
        _meetings = self.meetings

        if response["meetings"] is None:
            _meetings = {}

        if not isinstance(response["meetings"]["meeting"], list):
            response["meetings"]["meeting"] = [response["meetings"]["meeting"]]

        for meeting in response["meetings"]["meeting"]:
            meeting_id = meeting["meetingID"]
            del meeting["meetingID"]
            _meetings[meeting_id] = meeting

        self.meetings = _meetings


class MeetingAPI:
    def __init__(self, meeting, settings: Settings = Depends(settings_provider)):
        self.meeting = meeting
        self.settings = settings

    _server_api: Optional[ServerAPI] = None

    @property
    def server_api(self) -> ServerAPI:
        if not self._server_api:
            self._server_api = ServerAPI()
        return self._server_api

    @cached_property
    def data(self) -> dict:
        return {
            "meetingID": self.meeting.id,
            "name": self.meeting.name,
            "welcome": self.meeting.welcome_message,
            "moderatorOnlyMessage": self.meeting.moderator_message,
            "record": self.meeting.record,
            "autoStartRecording": self.meeting.auto_start_recording,
            "allowStartStopRecording": self.meeting.allow_start_stop_recording,
            "webcamsOnlyForModerator": self.meeting.webcams_only_for_moderator,
            "muteOnStart": self.meeting.mute_on_start,
            "allowModsToUnmuteUsers": self.meeting.allow_mods_to_unmute_users,
            "maxParticipants": self.meeting.max_participants,
            "duration": self.meeting.duration,
        }

    async def is_meeting_exists(self) -> bool:
        async with self.server_api as api:
            return str(self.meeting.id) in api.meetings.keys()

    async def create(self) -> dict:
        async with self.server_api as api:
            response = await api.create_meeting(**self.data)
        return response

    async def is_meeting_running(self) -> bool:
        api_method = "isMeetingRunning"
        params = {"meetingID": self.meeting.id}
        async with self.server_api as api:
            response = await api.request(api_method, params)
        is_running = response.get("running")
        if is_running == "true":
            return True
        if is_running == "false":
            return False

    async def end(self) -> dict:
        api_method = "end"
        params = {"meetingID": self.meeting.id, "password": self.settings.bbb_mod_pw}
        async with self.server_api as api:
            response = await api.request(api_method, params)

        return response

    async def get_meeting_info(self) -> dict:
        api_method = "getMeetingInfo"
        params = {"meetingID": self.meeting.id}
        async with self.server_api as api:
            response = await api.request(api_method, params)

        return response

    async def join(self, user) -> str:
        api_method = "join"
        params = {
            "meetingID": self.meeting.id,
            "fullName": user.first_name + " " + user.last_name,
            "password": self._get_password(user),
            "userID": user.id,
        }
        async with self.server_api as api:
            return api.get_url(api_method, params)

    def _get_password(self, user) -> str:
        if user.role == UserRoleChoices.MODERATOR.value:
            return self.settings.bbb_mod_pw
        return self.settings.bbb_attendee_pw
