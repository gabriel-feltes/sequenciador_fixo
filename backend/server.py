from flask import Flask, jsonify, request, send_from_directory
from threading import Lock
import os
import sqlite3

# Configurações de diretórios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.normpath(os.path.join(BASE_DIR, "../frontend/templates"))
STATIC_DIR = os.path.normpath(os.path.join(BASE_DIR, "../frontend/static"))

# Inicialização do Flask
app = Flask(__name__, static_folder=STATIC_DIR)
lock = Lock()  # Exclusão mútua para operações críticas

# Configuração do banco de dados SQLite
DB_PATH = os.path.join(BASE_DIR, "system_state.db")

def init_db():
    """Inicializa o banco de dados para armazenar membros, logs e mensagens."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS membership (
                id TEXT PRIMARY KEY
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sequence (
                key TEXT PRIMARY KEY,
                value INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sequence INTEGER,
                sender TEXT,
                content TEXT
            )
        """)
        # Inicializa o contador de sequência, se necessário
        cursor.execute("INSERT OR IGNORE INTO sequence (key, value) VALUES ('last_sequence', 0)")
        conn.commit()

# Inicializar o banco de dados
init_db()

def log_event(message):
    """Registra um evento no banco de dados e imprime no console."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (message) VALUES (?)", (message,))
        conn.commit()
    print(message)

@app.route('/')
def index():
    """Serve a interface inicial."""
    return send_from_directory(TEMPLATES_DIR, "index.html")

@app.route('/join', methods=['POST'])
def join_group():
    """Adiciona um processo ao grupo de membros."""
    process_id = request.json.get("process_id")
    with lock, sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO membership (id) VALUES (?)", (process_id,))
            conn.commit()
            log_event(f"JOIN: Processo {process_id} entrou no grupo.")
        except sqlite3.IntegrityError:
            return jsonify({"error": "Processo já está no grupo."}), 400
    return jsonify({"message": f"Processo {process_id} adicionado ao grupo."})

@app.route('/leave', methods=['POST'])
def leave_group():
    """Remove um processo do grupo de membros."""
    process_id = request.json.get("process_id")
    with lock, sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM membership WHERE id = ?", (process_id,))
        conn.commit()
        log_event(f"LEAVE: Processo {process_id} saiu do grupo.")
    return jsonify({"message": f"Processo {process_id} removido do grupo."})

@app.route('/send-message', methods=['POST'])
def send_message():
    """Recebe uma mensagem de um membro e associa um número de sequência."""
    data = request.json
    process_id = data.get("process_id")
    message = data.get("message")

    with lock, sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM membership WHERE id = ?", (process_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Processo não é membro do grupo."}), 403

        # Incrementa o número sequencial
        cursor.execute("UPDATE sequence SET value = value + 1 WHERE key = 'last_sequence'")
        cursor.execute("SELECT value FROM sequence WHERE key = 'last_sequence'")
        sequence_number = cursor.fetchone()[0]

        # Registra a mensagem no banco
        cursor.execute("""
            INSERT INTO messages (sequence, sender, content)
            VALUES (?, ?, ?)
        """, (sequence_number, process_id, message))
        conn.commit()

        log_event(f"MSG [{sequence_number}] {process_id}: {message}")
    return jsonify({"sequence": sequence_number, "message": message})

@app.route('/messages', methods=['GET'])
def get_messages():
    """Retorna todas as mensagens ordenadas."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sequence, sender, content
            FROM messages
            ORDER BY sequence
        """)
        messages = [
            f"[{row[0]}] {row[1]}: {row[2]}"
            for row in cursor.fetchall()
        ]
    return jsonify({"messages": messages})

@app.route('/logs', methods=['GET'])
def get_logs():
    """Retorna os logs do sistema."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT message FROM logs ORDER BY id")
        logs = [row[0] for row in cursor.fetchall()]
    return jsonify({"logs": logs})

@app.route('/clear-logs', methods=['POST'])
def clear_logs():
    """Limpa todos os logs do sistema."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM logs")
        conn.commit()
    log_event("LOGS: Todos os logs foram excluídos.")
    return jsonify({"message": "Todos os logs foram excluídos."})

@app.route('/clear-messages', methods=['POST'])
def clear_messages():
    """Limpa todas as mensagens armazenadas no banco."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages")
        conn.commit()
    log_event("CHAT: Todas as mensagens foram excluídas.")
    return jsonify({"message": "Todas as mensagens foram excluídas."})

@app.route('/membership', methods=['GET'])
def get_membership():
    """Retorna os membros ativos do grupo."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM membership")
        membership = [row[0] for row in cursor.fetchall()]
    return jsonify({"membership": membership})

@app.route('/reset-sequence', methods=['POST'])
def reset_sequence():
    """Reinicia o contador de sequência."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE sequence SET value = 0 WHERE key = 'last_sequence'")
        conn.commit()
    log_event("SEQUENCER: Contagem de sequência reiniciada para 0.")
    return jsonify({"message": "Contagem de sequência reiniciada para 0."})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
