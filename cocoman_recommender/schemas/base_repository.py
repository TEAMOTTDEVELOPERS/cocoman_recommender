class BaseRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory
