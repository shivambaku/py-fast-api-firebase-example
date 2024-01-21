from server.utils.models import UserModel


async def test_get_user(http_client_for_test_1, test_user_1_id):
    response = await http_client_for_test_1.get("/user/")
    assert response.status_code == 200

    user_model = UserModel.model_validate(response.json())
    assert user_model.id == test_user_1_id
