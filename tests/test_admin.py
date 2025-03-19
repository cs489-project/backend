from db.models import User, Role
from db.client import db_client
from consts import RESEARCHER, ORGANIZATION, ADMIN, PASSWORD

"""
=================================================
-------------------------------------------------
                    delete_user()
-------------------------------------------------
test_delete_user_success
test_delete_user_no_id
test_delete_user_not_found
test_delete_no_perms
=================================================
"""

def test_delete_user_success(client):
    response = client.post('/api/users/register', json={
        "email": "accounttodelete@test.com",
        "password": PASSWORD,
        "name": "AccountToDelete"
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Registered'

    response = client.post('/api/users/login-password', json={
        "email": ADMIN['email'],
        "password": PASSWORD
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Logged in'

    with client.application.app_context():
        user = User.query.filter_by(email='accounttodelete@test.com').first()
        assert user

        response = client.post('/api/admin/delete-user', json={
            "user_id": user.id
        })
    assert response.status_code == 200
    assert response.json['message'] == 'User deleted'

    with client.application.app_context():
        user = User.query.filter_by(email='accounttodelete@test.com').first()
        assert user is None