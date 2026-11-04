"""
Dashboard de Telemetria e Acessos — App Flask
Registra e exibe o histórico de visitas no PostgreSQL da Aiven.io.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

DATABASE_URL = os.getenv("AIVEN_DB_URL", "")

def get_db_connection():
    if not DATABASE_URL:
        return None
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS visits (
                        id SERIAL PRIMARY KEY,
                        path VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                conn.commit()
        except Exception as e:
            print(f"Erro ao inicializar o banco de dados: {e}")
        finally:
            conn.close()

def log_visit(path):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO visits (path) VALUES (%s);", (path,))
                conn.commit()
        except Exception as e:
            print(f"Erro ao registrar visita: {e}")
        finally:
            conn.close()

# Inicializa o esquema de tabelas na inicialização do modulo
init_db()

@app.route('/')
def index():
    log_visit(request.path)
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    conn = get_db_connection()
    if not conn:
        return jsonify({
            "total_visits": 0,
            "visits_per_minute": [],
            "recent_visits": [],
            "status": "database_offline"
        }), 200

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # 1. Total de visitas
            cur.execute("SELECT COUNT(*) as total FROM visits;")
            total_visits = cur.fetchone()["total"]

            # 2. Visitas por minuto
            cur.execute("""
                SELECT TO_CHAR(created_at, 'HH24:MI') as minute, COUNT(*) as count
                FROM visits
                GROUP BY minute
                ORDER BY minute ASC
                LIMIT 15;
            """)
            visits_per_minute = cur.fetchall()

            # 3. Últimos acessos
            cur.execute("""
                SELECT id, path, TO_CHAR(created_at, 'DD/MM/YYYY HH24:MI:SS') as created_at
                FROM visits
                ORDER BY id DESC
                LIMIT 10;
            """)
            recent_visits = cur.fetchall()

        return jsonify({
            "total_visits": total_visits,
            "visits_per_minute": visits_per_minute,
            "recent_visits": recent_visits,
            "status": "ok"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/healthz')
def healthz():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
            conn.close()
            return jsonify({"status": "ok", "database": "connected"}), 200
        except Exception:
            return jsonify({"status": "error", "database": "disconnected"}), 503
    return jsonify({"status": "error", "database": "disconnected"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)