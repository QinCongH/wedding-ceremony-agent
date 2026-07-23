from agent.tools.registry import ToolRegistry


def search_venue(query: str) -> str:
    """搜索婚礼场地"""
    # TODO: 接入真实搜索API
    return f"搜索场地结果: {query}"


ToolRegistry.register("search_venue", search_venue)
