import pytest

from capapi.models import APIUser


def test_admin_view(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200


def test_admin_user_create(admin_client):
    data = {
        "email": "bob_lawblaw@example.com",
        "first_name": "Bob",
        "last_name": "Lawblaw",
        "case_allowance": 500,
    }
    response = admin_client.post('/admin/capapi/apiuser/add/', data, follow=True)
    assert response.status_code == 200
    user = APIUser.objects.get(email=data['email'])
    assert user


@pytest.mark.django_db(transaction=True)
def test_admin_user_authenticate(admin_client, user):
    """
    Test if we can authenticate user through the admin panel
    """
    data = {
        'action': 'authenticate_user',
        '_selected_action': user.id,
    }
    response = admin_client.post('/admin/capapi/apiuser/', data, follow=True)
    user.refresh_from_db()

    assert response.status_code == 200
    assert user.is_authenticated
    assert user.get_api_key()


@pytest.mark.django_db(transaction=True)
def test_admin_user_authenticate_without_key_expires(admin_client, user):
    """
    Test if we can authenticate even if key_expires is missing
    """
    user.key_expires = None
    user.save()
    data = {
        'action': 'authenticate_user',
        '_selected_action': user.id,
    }
    response = admin_client.post('/admin/capapi/apiuser/', data, follow=True)
    user.refresh_from_db()

    assert response.status_code == 200
    assert user.is_authenticated
    assert user.get_api_key()

