from datetime import datetime, timedelta
import jwt
import bcrypt
from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Password hashing


def hash_password(password: str) -> str:
    # Truncate to 72 bytes (bcrypt limit). Handle multi-byte chars safely.
    encoded = password.encode("utf-8")
    if len(encoded) > 72:
        encoded = encoded[:72]
        # decode ignoring partial characters at the end
        password_to_hash = encoded.decode("utf-8", "ignore")
    else:
        password_to_hash = password

    return bcrypt.hashpw(password_to_hash.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    # Truncate plain password to 72 bytes to match hashing behavior
    encoded = plain.encode("utf-8")
    if len(encoded) > 72:
        encoded = encoded[:72]
        plain_to_verify = encoded.decode("utf-8", "ignore")
    else:
        plain_to_verify = plain

    try:
        return bcrypt.checkpw(plain_to_verify.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """Create a refresh JWT with a longer expiry and explicit type."""
    from core.config import REFRESH_TOKEN_EXPIRE_DAYS

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    # mark token as a refresh token
    to_encode.update({"exp": expire, "type": "refresh"})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_refresh_token(token: str) -> dict:
    """Decode and verify a refresh token, ensuring token type."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise

    if payload.get("type") != "refresh":
        raise ValueError("Not a refresh token")

    return payload