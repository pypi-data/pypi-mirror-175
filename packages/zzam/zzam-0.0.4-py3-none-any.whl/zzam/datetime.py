import datetime
from datetime import timedelta


def time_to_hours(time: timedelta) -> str:
    """
    Handles the conversion of a given time and returns
    the value as a str which represents that value as a
    human-readable string like HH:mm:ss
    """

    if time.days > 0:
        days_to_seconds: int = time.days * 24 * 60 * 60
        add_seconds: int = days_to_seconds + time.seconds
        return sec_to_hours(add_seconds)

    return str(timedelta(seconds=time.seconds))


def sec_to_hours(seconds: int) -> str:
    """
    Handles the conversion of seconds that represent more
    than 24 hours to a human-readable format like HH:mm:ss
    """

    hours: str = str(seconds // 3600)
    minutes: str = str((seconds % 3600) // 60)
    seconds: str = str((seconds % 3600) % 60)

    if len(minutes) == 1 and len(seconds) == 1:
        return f"{hours}:0{minutes}:0{seconds}"
    elif len(minutes) == 1 and len(seconds) > 1:
        return f"{hours}:0{minutes}:{seconds}"
    elif len(minutes) > 1 and len(seconds) == 1:
        return f"{hours}:{minutes}:0{seconds}"
    else:
        return f"{hours}:{minutes}:{seconds}"


def min_to_hours(minutes: any) -> str:
    """
    Handles converting minutes to hours and
    returning it as a string
    """

    return '{:02d}:{:02d}:{:02d}'.format(*divmod(int(minutes), 60))


def is_weekend(count_friday: bool = False) -> bool:
    """
    :return: True if Friday, Saturday or Sunday
    :return: True if Saturday or Sunday
    """
    localtime = datetime.datetime.now()
    if not count_friday:
        return (
            localtime.isocalendar()[2] == 6
            or localtime.isocalendar()[2] == 7
        )
    return (
        localtime.isocalendar()[2] == 5
        or localtime.isocalendar()[2] == 6
        or localtime.isocalendar()[2] == 7
    )
