"""Capa de datos simple (SQLite, sin dependencias externas) para el CRM de leads."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "crm.db"

ESTADOS = ["Nuevo", "Contactado", "Presupuesto enviado", "Ganado", "Perdido"]


def _conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT,
                tipo_evento TEXT,
                fecha_evento TEXT,
                marca TEXT,
                estado TEXT DEFAULT 'Nuevo',
                notas TEXT,
                creado_en TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def agregar_lead(nombre, telefono, tipo_evento, fecha_evento, marca, notas):
    with _conn() as conn:
        conn.execute(
            """INSERT INTO leads (nombre, telefono, tipo_evento, fecha_evento, marca, notas)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (nombre, telefono, tipo_evento, str(fecha_evento), marca, notas),
        )


def listar_leads():
    with _conn() as conn:
        return conn.execute("SELECT * FROM leads ORDER BY creado_en DESC").fetchall()


def actualizar_estado(lead_id, estado):
    with _conn() as conn:
        conn.execute("UPDATE leads SET estado = ? WHERE id = ?", (estado, lead_id))


def borrar_lead(lead_id):
    with _conn() as conn:
        conn.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
