from python_helper import DateTimeHelper

from enumeration.agenda.AgendaType import AgendaType
from enumeration.agenda.AgendaStatus import AgendaStatus

class AgendaRequestDto:
    def __init__(self,
        boss = None,
        scope = None,
        hoster = None,
        beginAtDate = None,
        endAtDate = None,
        beginAtTime = None,
        endAtTime = None,
        notes = None,
        type = None,
        status = None,
        url = None
    ):
        self.boss = boss
        self.scope = scope
        self.hoster = hoster
        self.beginAtDate = DateTimeHelper.toString(beginAtDate, pattern=DateTimeHelper.DEFAULT_DATE_PATTERN)
        self.endAtDate = DateTimeHelper.toString(endAtDate, pattern=DateTimeHelper.DEFAULT_DATE_PATTERN)
        self.beginAtTime = DateTimeHelper.toString(beginAtTime, pattern=DateTimeHelper.DEFAULT_TIME_PATTERN)
        self.endAtTime = DateTimeHelper.toString(endAtTime, pattern=DateTimeHelper.DEFAULT_TIME_PATTERN)
        self.notes = notes
        self.type = AgendaType.map(type)
        self.status = AgendaStatus.map(status)
        self.url = url

class AgendaResponseDto:
    def __init__(self,
        id = None,
        boss = None,
        scope = None,
        hoster = None,
        beginAtDate = None,
        endAtDate = None,
        beginAtTime = None,
        endAtTime = None,
        notes = None,
        type = None,
        status = None,
        url = None
    ):
        self.id = id
        self.boss = boss
        self.scope = scope
        self.hoster = hoster
        self.beginAtDate = DateTimeHelper.toString(beginAtDate, pattern=DateTimeHelper.DEFAULT_DATE_PATTERN)
        self.endAtDate = DateTimeHelper.toString(endAtDate, pattern=DateTimeHelper.DEFAULT_DATE_PATTERN)
        self.beginAtTime = DateTimeHelper.toString(beginAtTime, pattern=DateTimeHelper.DEFAULT_TIME_PATTERN)
        self.endAtTime = DateTimeHelper.toString(endAtTime, pattern=DateTimeHelper.DEFAULT_TIME_PATTERN)
        self.notes = notes
        self.type = AgendaType.map(type)
        self.status = AgendaStatus.map(status)
        self.url = url

class AgendaHeaderRequestDto :
    def __init__(self,
        id = None
    ) :
        self.id = id

class AgendaParamRequestDto :
    def __init__(self,
        boss = None,
        scope = None,
        hoster = None,
        beginAtDate = None,
        beginAtTime = None,
        status = None
    ) :
        self.boss = boss
        self.scope = scope
        self.hoster = hoster
        self.beginAtDate = beginAtDate
        self.beginAtTime = beginAtTime
        self.status = status
