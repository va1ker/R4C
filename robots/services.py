from robots.models import Robot


def create_robot(model: str, version: str, created: str) -> None:
    Robot.objects.create(serial=model + "-" + version, model=model, version=version, created=created)
