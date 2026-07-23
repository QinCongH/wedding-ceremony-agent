from agent.tools.registry import ToolRegistry


def check_calendar(date: str) -> str:
    """检查日期是否可用"""
    # TODO: 接入日历API
    return f"日期 {date} 可用"


ToolRegistry.register("check_calendar", check_calendar)
