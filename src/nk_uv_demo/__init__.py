from importlib.metadata import version

__version__ = version("nk-uv-demo")


def main() -> None:  # noqa: D103
    print("Hello from nk-uv-demo!\nVersion:", __version__)
