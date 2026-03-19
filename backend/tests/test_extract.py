from backend.app.services.extract import extract_action_items


def test_extract_action_items_advanced():
    text = """
    - [ ] Task dari checkbox
    - FIXME: Perbaiki bug ini
    - CHECK: Verifikasi data
    - Segera kirim laporan!
    - Ini cuma catatan biasa
    """.strip()

    items = extract_action_items(text)

    assert "Task dari checkbox" in items
    assert "Perbaiki bug ini" in items
    assert "Verifikasi data" in items
    assert "Segera kirim laporan!" in items
    assert "Ini cuma catatan biasa" not in items


def test_extract_empty_text():
    assert extract_action_items("") == []
    assert extract_action_items(None) == []
