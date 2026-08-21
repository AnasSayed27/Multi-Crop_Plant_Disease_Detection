import sqlite3
import os
import time
import hmac
import hashlib
import binascii
from typing import Optional, Dict, List, Any
import jwt

# Database path & Environment-driven JWT Configuration
DB_PATH = os.getenv("DB_PATH", "database.db")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.getenv("SECRET_KEY", "multi_crop_plant_disease_secret_key_2026_super_secure_32bytes"))
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
TOKEN_EXPIRATION_SECONDS = int(os.getenv("TOKEN_EXPIRATION_SECONDS", str(86400 * 7)))  # 7 days

# Try importing passlib / bcrypt, fallback to hashlib.pbkdf2_hmac if missing or failing
BCRYPT_AVAILABLE = False
try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # Quick sanity check test
    test_hash = pwd_context.hash("test")
    if pwd_context.verify("test", test_hash):
        BCRYPT_AVAILABLE = True
except Exception:
    BCRYPT_AVAILABLE = False


def hash_password(password: str) -> str:
    """Hashes a password using bcrypt if available, else hashlib.pbkdf2_hmac."""
    if BCRYPT_AVAILABLE:
        return pwd_context.hash(password)
    else:
        # PBKDF2 HMAC SHA256 with 100,000 iterations
        salt = hashlib.sha256(os.urandom(16)).hexdigest()[:16]
        key = hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode('utf-8'), 
            salt.encode('utf-8'), 
            100000
        )
        return f"pbkdf2_sha256${salt}${binascii.hexlify(key).decode('ascii')}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against its hash using constant-time comparison."""
    if BCRYPT_AVAILABLE and not hashed_password.startswith("pbkdf2_sha256$"):
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False
    
    if hashed_password.startswith("pbkdf2_sha256$"):
        parts = hashed_password.split("$")
        if len(parts) != 3:
            return False
        _, salt, expected_key = parts
        key = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        computed_key = binascii.hexlify(key).decode('ascii')
        return hmac.compare_digest(computed_key, expected_key)
    
    return False


def create_access_token(data: dict) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()
    to_encode.update({"exp": int(time.time()) + TOKEN_EXPIRATION_SECONDS})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decodes and validates a JWT access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None


def get_db():
    """Returns a SQLite database connection with row factory, foreign keys, and WAL mode."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA busy_timeout = 5000;")
    return conn


def init_db():
    """Initializes database schema and indexes for users and predictions."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create predictions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        crop TEXT NOT NULL,
        disease TEXT NOT NULL,
        confidence REAL NOT NULL,
        image_path TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    """)
    
    # Create query performance indexes
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_predictions_user_created 
    ON predictions (user_id, created_at DESC)
    """)
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_users_email 
    ON users (email)
    """)
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_users_username 
    ON users (username)
    """)
    
    conn.commit()
    conn.close()


def register_user(username: str, email: str, password: str) -> Dict[str, Any]:
    """Registers a new user in SQLite with normalized email."""
    username = username.strip()
    email = email.strip().lower()
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if username or email exists
    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
    if cursor.fetchone():
        conn.close()
        raise ValueError("Username or email already exists")
    
    hashed = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, hashed)
        )
        user_id = cursor.lastrowid
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise ValueError("Username or email already exists")
    finally:
        conn.close()
    
    return {"id": user_id, "username": username, "email": email}


def authenticate_user(username_or_email: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticates a user by username or normalized email and password."""
    identifier = username_or_email.strip()
    normalized_email = identifier.lower()
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, email, password_hash FROM users WHERE username = ? OR email = ?",
        (identifier, normalized_email)
    )
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return None
    
    if verify_password(password, user["password_hash"]):
        return {"id": user["id"], "username": user["username"], "email": user["email"]}
    return None


def get_user_by_id(user_id: Any) -> Optional[Dict[str, Any]]:
    """Fetches user details by user ID."""
    conn = get_db()
    cursor = conn.cursor()
    try:
        uid = int(user_id)
    except (ValueError, TypeError):
        conn.close()
        return None
    cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (uid,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return dict(user)
    return None


def save_prediction(user_id: int, crop: str, disease: str, confidence: float, image_path: str) -> int:
    """Saves a prediction record in the database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO predictions (user_id, crop, disease, confidence, image_path) VALUES (?, ?, ?, ?, ?)",
        (user_id, crop, disease, confidence, image_path)
    )
    prediction_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return prediction_id


def get_prediction_by_id(prediction_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves a single prediction record by ID."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, user_id, crop, disease, confidence, image_path, created_at
        FROM predictions
        WHERE id = ?
        """,
        (prediction_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def get_user_history(user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves user prediction history."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, crop, disease, confidence, image_path, created_at
        FROM predictions
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_user_stats(user_id: int) -> Dict[str, Any]:
    """Calculates summary statistics for a given user."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM predictions WHERE user_id = ?", (user_id,))
    total_scans = cursor.fetchone()["total"]
    
    if total_scans == 0:
        conn.close()
        return {
            "total_scans": 0,
            "avg_confidence": 0.0,
            "top_disease": "None",
            "crop_counts": {},
            "disease_counts": {}
        }
    
    cursor.execute("SELECT AVG(confidence) as avg_conf FROM predictions WHERE user_id = ?", (user_id,))
    avg_conf = cursor.fetchone()["avg_conf"] or 0.0
    
    cursor.execute("""
        SELECT disease, COUNT(*) as count 
        FROM predictions 
        WHERE user_id = ? 
        GROUP BY disease 
        ORDER BY count DESC 
        LIMIT 1
    """, (user_id,))
    top_disease_row = cursor.fetchone()
    top_disease = top_disease_row["disease"] if top_disease_row else "None"
    
    cursor.execute("""
        SELECT crop, COUNT(*) as count 
        FROM predictions 
        WHERE user_id = ? 
        GROUP BY crop
    """, (user_id,))
    crop_counts = {row["crop"]: row["count"] for row in cursor.fetchall()}
    
    cursor.execute("""
        SELECT disease, COUNT(*) as count 
        FROM predictions 
        WHERE user_id = ? 
        GROUP BY disease
    """, (user_id,))
    disease_counts = {row["disease"]: row["count"] for row in cursor.fetchall()}
    
    conn.close()
    
    return {
        "total_scans": total_scans,
        "avg_confidence": round(avg_conf, 2),
        "top_disease": top_disease,
        "crop_counts": crop_counts,
        "disease_counts": disease_counts
    }

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
