import requests
from .models import User, SocialAccount


def get_or_create_social_user(provider: str, access_token: str) -> tuple[User, bool]:
    handlers = {
        'google': _handle_google,
        'kakao': _handle_kakao,
        'github': _handle_github,
    }
    if provider not in handlers:
        raise ValueError(f"Unsupported provider: {provider}")
    return handlers[provider](access_token)


def _handle_google(access_token: str) -> tuple[User, bool]:
    resp = requests.get(
        'https://www.googleapis.com/oauth2/v3/userinfo',
        headers={'Authorization': f'Bearer {access_token}'},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    return _get_or_create_user(
        provider='google',
        social_id=data['sub'],
        email=data.get('email', ''),
        name=data.get('name', ''),
        profile_image=data.get('picture', ''),
    )


def _handle_kakao(access_token: str) -> tuple[User, bool]:
    resp = requests.get(
        'https://kapi.kakao.com/v2/user/me',
        headers={'Authorization': f'Bearer {access_token}'},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    kakao_account = data.get('kakao_account', {})
    profile = kakao_account.get('profile', {})
    return _get_or_create_user(
        provider='kakao',
        social_id=str(data['id']),
        email=kakao_account.get('email', ''),
        name=profile.get('nickname', ''),
        profile_image=profile.get('profile_image_url', ''),
    )


def _handle_github(access_token: str) -> tuple[User, bool]:
    headers = {'Authorization': f'token {access_token}', 'Accept': 'application/json'}
    resp = requests.get('https://api.github.com/user', headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    email = data.get('email') or ''
    if not email:
        email_resp = requests.get('https://api.github.com/user/emails', headers=headers, timeout=10)
        if email_resp.ok:
            emails = email_resp.json()
            primary = next((e['email'] for e in emails if e.get('primary')), None)
            email = primary or f"{data['login']}@github.com"

    return _get_or_create_user(
        provider='github',
        social_id=str(data['id']),
        email=email,
        name=data.get('name') or data.get('login', ''),
        profile_image=data.get('avatar_url', ''),
    )


def _get_or_create_user(
    provider: str, social_id: str, email: str, name: str, profile_image: str
) -> tuple[User, bool]:
    try:
        social = SocialAccount.objects.select_related('user').get(provider=provider, social_id=social_id)
        return social.user, False
    except SocialAccount.DoesNotExist:
        pass

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': email,
            'name': name,
            'profile_image': profile_image,
        },
    )
    SocialAccount.objects.create(user=user, provider=provider, social_id=social_id)
    return user, created
