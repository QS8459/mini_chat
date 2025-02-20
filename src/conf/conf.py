import logging

log = logging.Logger(
    name = "MINI CHAT"
)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(logging.Formatter('%(asctime)s\t%(levelname)s\t%(message)s', datefmt='%Y-%m-%dT%H:%M:%S'))

log.addHandler(streamHandler)
