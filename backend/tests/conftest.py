import os
import tempfile
from collections.abc import Generator

import pytest
from backend.app.db import get_db
from backend.app.main import app
from backend.app.models import Base
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    # Membuat file database sementara
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)

    # Setup engine dan session
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    # Menjalankan test
    with TestClient(app) as c:
        yield c

    # PERBAIKAN UNTUK WINDOWS:
    # 1. Hapus override agar session tidak tertahan
    app.dependency_overrides.clear()
    # 2. Matikan engine agar koneksi ke file .db benar-benar putus
    engine.dispose()
    
    # Sekarang file bisa dihapus dengan aman
    try:
        os.unlink(db_path)
    except PermissionError:
        # Jika masih gagal, biarkan saja agar tidak menghentikan proses test lainnya
        pass