import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_salud():
    res = client.get("/salud")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_preguntas_devuelve_las_24():
    res = client.get("/preguntas")
    assert res.status_code == 200
    body = res.json()
    assert len(body["questions"]) == 24
    assert set(body["domains"].keys()) == {"accesos", "wifi", "backups", "actualizaciones", "continuidad"}
    # el campo help debe viajar (aunque sea vacio para las que no lo tienen)
    assert all("help" in q for q in body["questions"])


def test_recomendaciones_devuelve_las_24():
    res = client.get("/recomendaciones")
    assert res.status_code == 200
    assert len(res.json()) == 24


def test_evaluar_calcula_el_mismo_motor():
    res = client.post("/evaluar", json={"respuestas": {q_id: "yes" for q_id in _all_question_ids()}})
    assert res.status_code == 200
    body = res.json()
    assert body["global_score"] == 100.0
    assert body["risk_level"] == "BAJO"
    assert body["top_actions"] == []


def test_evaluar_detecta_brechas_y_prioriza():
    res = client.post("/evaluar", json={"respuestas": {q_id: "no" for q_id in _all_question_ids()}})
    assert res.status_code == 200
    body = res.json()
    assert body["global_score"] == 0.0
    assert body["risk_level"] == "CRITICO"
    assert len(body["top_actions"]) == 24
    priorities = [a["priority"] for a in body["top_actions"]]
    assert priorities == sorted(priorities)


def test_evaluar_rechaza_respuesta_invalida():
    res = client.post("/evaluar", json={"respuestas": {"ACC-01": "tal_vez"}})
    assert res.status_code == 422


def test_guia_hardening_devuelve_las_24_ordenadas_por_prioridad():
    res = client.get("/guia-hardening")
    assert res.status_code == 200
    body = res.json()
    assert len(body) == 24
    priority_order = {"P1": 0, "P2": 1, "P3": 2}
    priorities = [priority_order[a["priority"]] for a in body]
    assert priorities == sorted(priorities)
    assert {a["question_id"] for a in body} == set(_all_question_ids())


def _all_question_ids():
    return [q["id"] for q in client.get("/preguntas").json()["questions"]]
