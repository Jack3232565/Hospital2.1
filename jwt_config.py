
from jwt import encode, decode, DecodeError, ExpiredSignatureError, InvalidTokenError

def solicita_token(dato: dict) -> str:
    token: str = encode(payload=dato, key='jack323256', algorithm='HS256')
    return token

def valida_token(token: str) -> dict:
    try:
        dato: dict = decode(token, key="jack323256", algorithms=["HS256"])
        return dato
    except ExpiredSignatureError:
        print("El token ha expirado")
        raise
    except DecodeError:
        print("Error decodificando el token: Padding incorrecto o token mal formado")
        raise
    except InvalidTokenError:
        print("Token inválido")
        raise