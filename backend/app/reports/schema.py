from enum import Enum

from pydantic import BaseModel


class UsageAction(str, Enum):
    used = "used"
    wasted = "wasted"


class LogUsageRequest(BaseModel):
    action: UsageAction
    delete_item: bool = False


class ReportItem(BaseModel):
    name: str
    count: int
    unit: str
