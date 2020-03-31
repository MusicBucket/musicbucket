from emoji import emojize


class EmojiMixin:
    EMOJI = NotImplementedError

    @classmethod
    def get_emoji(cls):
        return emojize(cls.EMOJI, use_aliases=True)
