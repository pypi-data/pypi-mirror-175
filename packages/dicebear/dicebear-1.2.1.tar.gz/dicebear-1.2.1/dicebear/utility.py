from . import DStyle, DOptions, DAvatar, ascii_lowercase, digits
from random import choices
import typing


def bulk_create(style: DStyle = DStyle.random(), amount: typing.Annotated[int, "Min: 1, Max: 1000"] = 2, *, options: DOptions = None, custom: dict = None) -> typing.List[DAvatar]:
    """
    Creates a list of :py:class:`DAvatar` objects. Easy way to make multiple of the same style (but different randomly generated seeds) at once.

    :param style: class `DStyle` :: the style to apply to all avatars
    :type style: dicebear.DStyle
    :param amount: class `int` :: the amount of DAvatars to create. Default: 2, Min: 1, Max: 1000
    :type amount: int
    :param options: class `DOptions` :: options for the avatar
    :type options: dicebear.DOptions
    :param custom: class `dict` :: customisations for the specified style
    :type custom: dict
    :return: list[DAvatar] :: a list with DAvatar objects
    """
    if amount > 1000 or amount < 1: raise ValueError("argument `amount` must be between 1 and 1000")
    if style is None: style = DStyle.random()
    if custom is None: custom = {}
    if options is None: options = DOptions.empty
    result = []
    for _ in range(amount):
        result.append(DAvatar(style, "".join(choices(ascii_lowercase + digits, k=20)), options=options, custom=custom))
    return result
