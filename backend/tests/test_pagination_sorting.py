import pytest

@pytest.fixture
def setup_many_notes(client):
    """Membuat 10 catatan untuk pengujian paginasi."""
    for i in range(10):
        client.post("/notes/", json={
            "title": f"Note {i:02d}", 
            "content": f"Content {i}",
            "category_id": None
        })

def test_notes_pagination(client, setup_many_notes):
    # Tes limit: Pastikan hanya 3 catatan yang dikembalikan
    response = client.get("/notes/", params={"limit": 3})
    data = response.json()
    assert len(data) == 3

    # Tes skip: Lewati 8 catatan, harus ada sisa catatan (dari 10 + seed awal)
    response = client.get("/notes/", params={"skip": 8, "limit": 10})
    data = response.json()
    assert len(data) >= 2 

def test_notes_sorting(client, setup_many_notes):
    # Tes sort ascending (A-Z) berdasarkan judul
    response = client.get("/notes/", params={"sort": "title", "limit": 5})
    data = response.json()
    titles = [n["title"] for n in data]
    test_titles = [t for t in titles if t.startswith("Note")]
    assert test_titles == sorted(test_titles)

    # Tes sort descending (Z-A) berdasarkan judul
    response = client.get("/notes/", params={"sort": "-title", "limit": 5})
    data = response.json()
    titles = [n["title"] for n in data]
    test_titles = [t for t in titles if t.startswith("Note")]
    assert test_titles == sorted(test_titles, reverse=True)

def test_action_items_sorting(client):
    # Buat item dengan deskripsi tertentu untuk tes urutan
    client.post("/action-items/", json={"description": "Apel"})
    client.post("/action-items/", json={"description": "Zebra"})
    
    response = client.get("/action-items/", params={"sort": "description"})
    data = response.json()
    descriptions = [item["description"] for item in data]
    # Pastikan 'Apel' muncul sebelum 'Zebra'
    assert descriptions.index("Apel") < descriptions.index("Zebra")