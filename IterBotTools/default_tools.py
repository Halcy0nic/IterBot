"""Default tools registry for IterBot."""

from .time_tool import TimeTool


def get_default_tools():
    """Returns the default tool registry for IterBot agents."""
    return {
        "get_current_time": TimeTool.get_current_time,
        "get_current_date": TimeTool.get_current_date,
        "get_current_datetime": TimeTool.get_current_datetime,
        "get_epoch_time": TimeTool.get_epoch_time
    }
