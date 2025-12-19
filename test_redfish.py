import pytest
import requests
import time
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

BASE_URL = "https://localhost:2443/redfish/v1"
AUTH = HTTPBasicAuth("root", "0penBmc")

@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    s.verify = False
    s.auth = AUTH
    return s

# Тест 1: Аутентификация в OpenBMC через Redfish API
def test_authentication(session):
    response = session.get(f"{BASE_URL}/")
    assert response.status_code == 200, f"Ошибка аутентификации: {response.status_code}"
    data = response.json()

    assert "Systems" in data, "Отсутствует ссылка на [Systems]"
    assert "Chassis" in data, "Отсутствует ссылка на [Chassis]"

# Тест 2: Получение информации о системе
def test_get_system_info(session):
    response = session.get(f"{BASE_URL}/Systems/system")
    assert response.status_code == 200, f"Не удалось получить информацию о системе: {response.status_code}"
    data = response.json()

    assert "PowerState" in data, "Отсутствует [PowerState]"
    assert "Status" in data, "Отсутствует [Status]"

# Тест 3: "Управление" питанием
def test_power_control(session):
    power_url = f"{BASE_URL}/Systems/system/Actions/ComputerSystem.Reset"

    resp = session.post(power_url, json={"ResetType": "On"})
    assert resp.status_code == 204, f"Команда 'On' не принята: {resp.status_code}"

    time.sleep(3)

    resp = session.post(power_url, json={"ResetType": "GracefulShutdown"})
    assert resp.status_code == 204, f"Команда 'GracefulShutdown' не принята: {resp.status_code}"

# Тест 4: "Проверка температуры" CPU
def test_cpu_temperature_interface_exists(session):
    response = session.get(f"{BASE_URL}/Chassis/chassis")

    assert response.status_code == 200, "Ресурс [Chassis] недоступен"

    data = response.json()

    links = data.get("Links", {})
    thermal_present = "Thermal" in links or any("Thermal" in str(v) for v in data.values())
    assert thermal_present, "Ссылка на [Thermal] отсутствует в ресурсе [Chassis]"

# Тест 5: Сравнение источников данных (Redfish vs IPMI)
def test_redfish_and_ipmi_interfaces_available(session):
    import subprocess

    # 1. Redfish
    r = session.get(f"{BASE_URL}/")
    redfish_ok = (r.status_code == 200)

    # 2. IPMI
    try:
        result = subprocess.run(
            ["ipmitool", "-I", "lanplus", "-H", "localhost", "-p", "2623",
             "-U", "root", "-P", "0penBmc", "fru", "print"],
            capture_output=True, text=True, timeout=10
        )
        ipmi_ok = (result.returncode == 0)
    except Exception:
        ipmi_ok = False

    assert redfish_ok, "Redfish API недоступен"
    assert ipmi_ok, "IPMI не отвечает"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])