"""Tożsamość użytkownika i role (etap 2).

Tryby (AUTH_MODE):
- local: komputer AJ, bez logowania; jeden użytkownik lokalny z rolą operatora.
- cloudflare: Cloudflare Access sprawdza osobę przy wejściu, a backend dodatkowo
  weryfikuje podpis tokenu (nagłówek Cf-Access-Jwt-Assertion albo ciasteczko
  CF_Authorization). Sam adres e-mail w nagłówku nie wystarcza.

Rola operatora: adres e-mail na liście OPERATOR_EMAILS. Pozostali to testerzy.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache

import jwt
from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.deps import get_db
from app.core.local_test import PLACEHOLDER_USER_ID
from app.models.db_models import Analysis, User

ROLE_OPERATOR = "operator"
ROLE_TESTER = "tester"


@dataclass
class CurrentUser:
    user: User
    role: str

    @property
    def is_operator(self) -> bool:
        return self.role == ROLE_OPERATOR


@lru_cache(maxsize=4)
def _jwks_client(team_domain: str) -> jwt.PyJWKClient:
    return jwt.PyJWKClient(f"https://{team_domain}/cdn-cgi/access/certs", cache_keys=True)


def verify_access_token(token: str) -> dict:
    """Zwraca dane tokenu Cloudflare Access albo zgłasza 401."""
    team, aud = settings.cf_access_team_domain, settings.cf_access_aud
    if not team or not aud:
        raise HTTPException(status_code=500, detail="Brak konfiguracji Cloudflare Access (CF_ACCESS_TEAM_DOMAIN, CF_ACCESS_AUD).")
    try:
        key = _jwks_client(team).get_signing_key_from_jwt(token).key
        claims = jwt.decode(token, key, algorithms=["RS256"], audience=aud, issuer=f"https://{team}")
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="Nieprawidłowy lub wygasły token logowania.") from exc
    if not claims.get("email") or not claims.get("sub"):
        raise HTTPException(status_code=401, detail="Token logowania nie zawiera adresu e-mail.")
    return claims


def role_for(email: str) -> str:
    return ROLE_OPERATOR if email.lower() in settings.operator_emails else ROLE_TESTER


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> CurrentUser:
    if settings.auth_mode == "local":
        user = await db.get(User, PLACEHOLDER_USER_ID)
        if user is None:
            user = User(id=PLACEHOLDER_USER_ID, sub="obsil-local-test", email="local-test@localhost", is_active=True)
            db.add(user)
            await db.commit()
        return CurrentUser(user, ROLE_OPERATOR)
    if settings.auth_mode != "cloudflare":
        raise HTTPException(status_code=500, detail="Nieznany AUTH_MODE.")

    token = request.headers.get("cf-access-jwt-assertion") or request.cookies.get("CF_Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Brak logowania.")
    claims = verify_access_token(token)
    email = claims["email"].lower()
    user = (await db.execute(select(User).where(User.sub == claims["sub"]))).scalar_one_or_none()
    if user is None:
        user = User(sub=claims["sub"], email=email, is_active=True)
        db.add(user)
    user.email = email
    user.last_login = datetime.now(timezone.utc)
    # Zapis od razu: endpoint może używać innej sesji, a analiza wskazuje na użytkownika.
    await db.commit()
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Konto zablokowane.")
    return CurrentUser(user, role_for(email))


def require_operator(current: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if not current.is_operator:
        raise HTTPException(status_code=403, detail="Operacja dostępna tylko dla operatora.")
    return current


async def get_owned_analysis(analysis_id, current: CurrentUser, db: AsyncSession) -> Analysis:
    """Analiza widoczna dla autora i operatora; dla innych jak nieistniejąca (404)."""
    analysis = await db.get(Analysis, analysis_id)
    if analysis is None or (not current.is_operator and analysis.user_id != current.user.id):
        raise HTTPException(status_code=404, detail="Nie znaleziono analizy.")
    return analysis
