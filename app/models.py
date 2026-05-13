from .config import get_db_connection

def init_db():
    """Initialiser la base de données"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Créer table users
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

def get_all_users():
    """Récupérer tous les utilisateurs"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, email, created_at FROM users ORDER BY id')
    users = cur.fetchall()
    cur.close()
    conn.close()
    
    return [
        {
            'id': user[0],
            'name': user[1],
            'email': user[2],
            'created_at': user[3].isoformat() if user[3] else None
        }
        for user in users
    ]

def create_user(name, email):
    """Créer un nouvel utilisateur"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            'INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id',
            (name, email)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return user_id
    except Exception:
        conn.rollback()
        cur.close()
        conn.close()
        return None
