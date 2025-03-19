from db.models import User

"""
=================================================
-------------------------------------------------
                    register()
-------------------------------------------------
test_register_success
test_register_too_short_password
test_register_invalid_email
test_register_empty_email
test_register_empty_name
test_register_too_long_password
test_register_duplicate_user
=================================================
"""

def test_register_success(client):
    response = client.post('/api/users/register', json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "password10"
    })
    assert response.status_code == 200  
    assert response.json['message'] == 'Registered'

    with client.application.app_context():
        user = User.query.filter_by(email="test@test.com").first()
        assert user is not None
        assert user.name == "Test User"
    
def test_register_too_short_password(client):
    response = client.post('/api/users/register', json={
        "name": "Test User",
        "email": "bad@test.com",
        "password": "short"
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Password must be between 10 to 64 characters'

    with client.application.app_context():
        user = User.query.filter_by(email="bad@test.com").first()
        assert user is None

def test_register_invalid_email(client):
    response = client.post('/api/users/register', json={
        "name": "Test User",
        "email": "invalid-email",
        "password": "password10"
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid email format'

    with client.application.app_context():
        user = User.query.filter_by(email="invalid-email").first()
        assert user is None

def test_register_empty_email(client):
    response = client.post('/api/users/register', json={
        "name": "Test User",
        "email": "",
        "password": "password10"
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid email format'

    with client.application.app_context():
        user = User.query.filter_by(email="").first()
        assert user is None

def test_register_empty_name(client):
    response = client.post('/api/users/register', json={
        "name": "",
        "email": "emptyname@test.com",
        "password": "password10"
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Name cannot be empty'

    with client.application.app_context():
        user = User.query.filter_by(email="emptyname@test.com").first()
        assert user is None

def test_register_too_long_password(client):
    response = client.post('/api/users/register', json={
        "name": "Test User",
        "email": "longpassword@test.com",
        "password": "p" * 65
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Password must be between 10 to 64 characters'

    with client.application.app_context():
        user = User.query.filter_by(email="longpassword@test.com").first()
        assert user is None

def test_register_duplicate_user(client):
    response = client.post('/api/users/register', json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "password10"
    })
    assert response.status_code == 400
    assert response.json['error'] == 'User already exists'

    with client.application.app_context():
        user = User.query.filter_by(email="test@test.com").all()
        assert len(user) == 1

"""
=================================================
-------------------------------------------------
                login_password()
-------------------------------------------------
test_login_password_success
test_login_password_no_email
test_login_password_incorrect_password
test_login_password_no_user
=================================================
"""

def test_login_password_success(client):
    response = client.post('/api/users/login-password', json={
        "email": "test@test.com",
        "password": "password10"
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Logged in'

def test_login_password_no_email(client):
    response = client.post('/api/users/login-password', json={
        "email": "",
        "password": "password10"
    })
    assert response.status_code == 401
    assert response.json['error'] == 'Error logging in'

def test_login_password_incorrect_password(client):
    response = client.post('/api/users/login-password', json={
        "email": "test@test.com",
        "password": "password"
    })
    assert response.status_code == 401
    assert response.json['error'] == 'Error logging in'

def test_login_password_no_user(client):
    response = client.post('/api/users/login-password', json={
        "email": "nonexistent@test.com",
        "password": "password10"
    })
    assert response.status_code == 401
    assert response.json['error'] == 'Error logging in'
