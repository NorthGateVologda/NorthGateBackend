from apps.api.models import Username


def is_exists_username(username: str) -> bool:
    return Username.objects.filter(username=username).exists()

def save_username(username: str) -> None:
    Username.objects.create(username=username)