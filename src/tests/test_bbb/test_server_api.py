import json

import pytest

from bigbluebutton.api import ServerAPI
from core.settings import BBB_SERVER_URL
from main import app


class TestServerAPIRequestResponse:
    @pytest.mark.asyncio
    async def test_request_end(self, meeting_end_response):
        async with ServerAPI() as api:
            response = await api.request(api_method='')

        assert type(response) is dict

    @pytest.mark.asyncio
    async def test_request_create(self, meeting_create_response):
        async with ServerAPI() as api:
            response = await api.request(api_method='')

        assert type(response) is dict

    @pytest.mark.asyncio
    async def test_request_meeting_info(
            self,
            meeting_get_meeting_info_response
    ):
        async with ServerAPI() as api:
            response = await api.request(api_method='')

        assert type(response) is dict

    @pytest.mark.asyncio
    async def test_request_meetings(
            self,
            meeting_get_meetings_response
    ):
        async with ServerAPI() as api:
            response = await api.request(api_method='')

        assert type(response) is dict

    @pytest.mark.asyncio
    async def test_request_is_running(
            self,
            meeting_is_meeting_running_response
    ):
        async with ServerAPI() as api:
            response = await api.request(api_method='')

        assert type(response) is dict

    @pytest.mark.asyncio
    async def test_request_join(self, meeting_join_response):
        async with ServerAPI() as api:
            response = await api.request(api_method='')

        assert type(response) is dict


class TestServerAPIGetMeetingsCaching:
    @pytest.mark.asyncio
    async def test_meetings_has_value(self):
        meeting_info = {
            'meetingID': {'some_structure': 'aaa'}
        }

        await app.state.redis.set(f"{BBB_SERVER_URL}::meetings", json.dumps(
            meeting_info
        ))

        async with ServerAPI() as api:
            api_meetings = api.meetings

        assert api_meetings == meeting_info
