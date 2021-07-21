class TestGetSchedules:
    def test_get_schedules_return_403(self, client):
        response = client.get('/schedule/')

        assert response.status_code == 403

    def test_get_schedules_status_code(self, client, auth_headers):
        response = client.get('/schedule/', headers=auth_headers)

        assert response.status_code == 200

    def test_get_schedules_content(self, client, auth_headers, test_schedule):
        response = client.get('/schedule/', headers=auth_headers)

        assert test_schedule.id in \
               [schedule['id'] for schedule in response.json()]


class TestGetSchedule:
    def test_get_schedule_return_403(self, client, test_schedule):
        print(test_schedule)
        pk = test_schedule.id
        response = client.get(f'/schedule/{pk}')

        assert response.status_code == 403

    def test_get_schedule_status_code(self, client, test_schedule,
                                      auth_headers):
        pk = test_schedule.id
        response = client.get(f'/schedule/{pk}', headers=auth_headers)

        assert response.status_code == 200

    def test_get_schedule_content(self, client, test_schedule, auth_headers):
        pk = test_schedule.id
        response = client.get(f'/schedule/{pk}', headers=auth_headers)

        assert pk == response.json().get('id')


class TestCreateSchedule:
    def test_create_schedule_return_403(self, client):
        response = client.post('/schedule/')

        assert response.status_code == 403

    def test_create_schedule_status_code(self, client, test_user,
                                         auth_headers):
        _, user = test_user
        response = client.post('/schedule/', headers=auth_headers, data=[user])

        assert response.status_code == 201

    def test_create_schedule_content(self, client, test_user,
                                     auth_headers):
        _, user = test_user
        response = client.post('/schedule/', headers=auth_headers, data=[user])

        assert 'id' in response.json().keys()


class TestDeleteSchedule:
    def test_delete_schedule_return_403(self, client, test_schedule):
        pk = test_schedule.id
        response = client.delete(f'/schedule/{pk}')

        assert response.status_code == 403

    def test_delete_schedule_status_code(self, client, test_schedule,
                                         auth_headers):
        pk = test_schedule.id
        response = client.delete(f'/schedule/{pk}', headers=auth_headers)

        assert response.status_code == 204


class TestGetScheduleCells:
    def test_get_schedule_cells_return_403(self):
        pass

    def test_get_schedule_cells_status_code(self):
        pass

    def test_get_schedule_cells_content(self):
        pass


class TestGetScheduleCell:
    def test_get_schedule_cell_return_403(self):
        pass

    def test_get_schedule_cell_status_code(self):
        pass

    def test_get_schedule_cell_content(self):
        pass


class TestCreateScheduleCell:
    def test_create_schedule_cell_return_403(self):
        pass

    def test_create_schedule_cell_status_code(self):
        pass

    def test_create_schedule_cell_content(self):
        pass


class TestDeleteScheduleCell:
    def test_delete_schedule_cell_return_403(self):
        pass

    def test_delete_schedule_cell_status_code(self):
        pass

    def test_delete_schedule_cell_content(self):
        pass
