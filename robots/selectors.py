from robots.models import Robot


def is_robot_exists(*, serial: str) -> bool:
    return Robot.objects.filter(serial=serial).exists()
