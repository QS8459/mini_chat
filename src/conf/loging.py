import logging

log = logging.Logger(
    name="Mini Chat",
)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(logging.Formatter("%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

log.addHandler(console)