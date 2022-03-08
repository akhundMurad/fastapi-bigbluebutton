import json

import pytest

from bigbluebutton.api import MeetingAPI
from core.settings import BBB_SERVER_URL


class TestMeetingAPI:
    @pytest.mark.asyncio
    async def test_create_method(
            self,
            meeting_create_response,
            test_meeting,
            mocker
    ):
        get_meetings_mock = mocker.patch(  # noqa: F841
            'bigbluebutton.api.ServerAPI.get_meetings'
        )

        api = MeetingAPI(test_meeting)

        response = await api.create()

        assert type(response) is dict
        assert response.get('meetingID') == 'Demo Meeting'

    @pytest.mark.asyncio
    async def test_end_method(self, meeting_end_response, test_meeting):
        api = MeetingAPI(test_meeting)

        response = await api.end()

        assert type(response) is dict
        assert response.get('messageKey') == 'sentEndMeetingRequest'

    @pytest.mark.asyncio
    async def test_is_meeting_running_method(
            self,
            meeting_is_meeting_running_response,
            test_meeting
    ):
        api = MeetingAPI(test_meeting)

        response = await api.is_meeting_running()

        assert type(response) is bool
        assert response is True

    @pytest.mark.asyncio
    async def test_get_meeting_info_method(
            self,
            meeting_get_meeting_info_response,
            test_meeting
    ):
        api = MeetingAPI(test_meeting)

        response = await api.get_meeting_info()

        assert type(response) is dict
        assert response.get('meetingID') == 'Demo Meeting'

    @pytest.mark.asyncio
    async def test_join_method(
            self,
            meeting_join_response,
            test_user,
            test_meeting
    ):
        password, user = test_user
        api = MeetingAPI(test_meeting)

        response = await api.join(user)

        assert type(response) is str

    @pytest.mark.asyncio
    async def test_is_meeting_exists_method(self, test_meeting, redis):
        meeting_info = {
            str(test_meeting.id): {'some_structure': 'aaa'}
        }
        await redis.set(f"{BBB_SERVER_URL}::meetings", json.dumps(
            meeting_info
        ))

        api = MeetingAPI(test_meeting)

        response = await api.is_meeting_exists()

        assert type(response) is bool
        assert response is True

    @pytest.mark.asyncio
    async def test_is_meeting_exists_method_return_false(self, test_meeting):
        api = MeetingAPI(test_meeting)

        response = await api.is_meeting_exists()

        assert type(response) is bool
        assert response is False
