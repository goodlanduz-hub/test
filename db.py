import sqlite3
from datetime import datetime, timedelta, timezone

# Toshkent vaqti (O'zbekistonda yozgi vaqt yo'q)
TZ = timezone(timedelta(hours=5))

_conn: sqlite3.Connection | None = None


def _now() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")


def init(path: str) -> None:
    global _conn
    _conn = sqlite3.connect(path)
    _conn.row_factory = sqlite3.Row
    _conn.execute(
        """
        CREATE TABLE IF NOT EXISTS leads (
            user_id      INTEGER PRIMARY KEY,
            username     TEXT,
            tg_name      TEXT,
            source       TEXT NOT NULL,
            name         TEXT,
            rooms        TEXT,
            phone        TEXT,
            started_at   TEXT NOT NULL,
            completed_at TEXT
        )
        """
    )
    _conn.commit()


def touch(user_id: int, username: str | None, tg_name: str, source: str) -> None:
    """Botga kirgan foydalanuvchini yozib qo'yadi.

    Manba faqat yangi reklama havolasi bilan kelganda yangilanadi, shunda
    keyinroq oddiy /start bosgan odam reklamadan kelgani yo'qolmaydi.
    """
    _conn.execute(
        """
        INSERT INTO leads (user_id, username, tg_name, source, started_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            tg_name  = excluded.tg_name,
            source   = CASE WHEN excluded.source = 'direct' THEN leads.source
                            ELSE excluded.source END
        """,
        (user_id, username, tg_name, source, _now()),
    )
    _conn.commit()


def complete(user_id: int, name: str, rooms: str, phone: str) -> None:
    _conn.execute(
        "UPDATE leads SET name = ?, rooms = ?, phone = ?, completed_at = ? WHERE user_id = ?",
        (name, rooms, phone, _now(), user_id),
    )
    _conn.commit()


def get(user_id: int) -> sqlite3.Row | None:
    return _conn.execute("SELECT * FROM leads WHERE user_id = ?", (user_id,)).fetchone()


def is_completed(user_id: int) -> bool:
    row = get(user_id)
    return bool(row and row["completed_at"])


def stats() -> tuple[int, int, list[sqlite3.Row]]:
    total, completed = _conn.execute(
        "SELECT COUNT(*), COUNT(completed_at) FROM leads"
    ).fetchone()
    by_source = _conn.execute(
        """
        SELECT source, COUNT(*) AS started, COUNT(completed_at) AS completed
        FROM leads GROUP BY source ORDER BY started DESC
        """
    ).fetchall()
    return total, completed, by_source


def all_leads() -> list[sqlite3.Row]:
    return _conn.execute("SELECT * FROM leads ORDER BY started_at").fetchall()
