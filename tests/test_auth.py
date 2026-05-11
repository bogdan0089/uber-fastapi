from httpx import AsyncClient


async def test_register(client: AsyncClient):
    response = await client.post("/auth/register", json={
        "email": "test@gmail.com",
        "password": "test1234",
        "full_name": "Bohdan Kaliushyk"
    })
    assert response.status_code == 201