import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, jsonify
from bcb_client import get_all_bcb_data

app = Flask(__name__)

DATABASE_URL = os.getenv("AIVEN_DB_URL", "")

def get_db_connection():
    if not DATABASE_URL:
        return None
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL da Aiven: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS bcb_series (
                        id SERIAL PRIMARY KEY,
                        serie_nome VARCHAR(50) NOT NULL,
                        data_referencia VARCHAR(20),
                        valor NUMERIC(10, 4),
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                conn.commit()
        except Exception as e:
            print(f"Erro ao inicializar tabela no banco: {e}")
        finally:
            conn.close()

init_db()

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/stats')
@app.route('/api/bcb')
def get_bcb_stats():
    data = get_all_bcb_data()
    
    conn = get_db_connection()
    db_status = "connected" if conn else "disconnected"
    if conn:
        conn.close()

    return jsonify({
        "status": "ok",
        "database": db_status,
        "series": data
    })

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