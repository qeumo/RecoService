from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.token_template = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9" \
                              ".eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIi" \
                              "LCJpYXQiOjE2Njg4NjExNTQsImV4cCI6MTcwM" \
                              "DM5NzE1NCwiYXVkIjoid3d3LmV4YW1wbGUuY2" \
                              "9tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmN" \
                              "vbSIsIkdpdmVuTmFtZSI6IkpvaG5ueSIsIlN1" \
                              "cm5hbWUiOiJSb2NrZXQiLCJFbWFpbCI6Impyb" \
                              "2NrZXRAZXhhbXBsZS5jb20iLCJSb2xlIjpbIk" \
                              "1hbmFnZXIiLCJQcm9qZWN0IEFkbWluaXN0cmF" \
                              "0b3IiXX0.YgQERjBuFj7f3Ofy3q2aQMXA4JCv" \
                              "5q2rKAgkiIri3G8"

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = \
            await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403,
                                    detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403,
                                    detail="Invalid token.")
            return credentials.credentials
        raise HTTPException(status_code=403,
                            detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> bool:
        return self.token_template == token
