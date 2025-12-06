from locust import HttpUser, task, between
import json

# Класс для нагрузки OpenBMC
class OpenBMCUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://localhost:2443"
    verify = False

    def on_start(self):
        self.client.auth = ("root", "0penBmc")

    @task(2)
    def get_system_info(self):
        with self.client.get("/redfish/v1/Systems/system", name="OpenBMC: System Info", catch_response=True) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "PowerState" in data:
                        response.success()
                    else:
                        response.failure("[PowerState отсутствует.]")
                except json.JSONDecodeError:
                    response.failure("Некорректный JSON в ответе")
            else:
                response.failure(f"Статус: {response.status_code}")

    @task(1)
    def get_root_redfish(self):
        self.client.get("/redfish/v1/", name="OpenBMC: Root")


# Класс для нагрузки публичного API
class PublicAPIUser(HttpUser):
    wait_time = between(0.5, 2)
    host = "https://jsonplaceholder.typicode.com"

    @task(3)
    def get_posts(self):
        self.client.get("/posts", name="Public API: Get Posts")

    @task(1)
    def get_first_post(self):
        self.client.get("/posts/1", name="Public API: Get Post #1")