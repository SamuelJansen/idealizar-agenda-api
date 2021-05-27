from python_helper import Constant as c
from python_helper import ObjectHelper, StringHelper, DateTimeHelper
from python_framework import SqlAlchemyProxy as sap
from python_framework import ConverterStatic
from model.ModelAssociation import AGENDA, MODEL

from enumeration.util.WeekDay import WeekDay
from enumeration.agenda.AgendaType import AgendaType
from enumeration.agenda.AgendaStatus import AgendaStatus

GIANT_STRING_SIZE = 16384
LARGE_STRING_SIZE = 1024
STRING_SIZE = 512
MEDIUM_STRING_SIZE = 128
LITTLE_STRING_SIZE = 64

DEFAULT_STATUS = AgendaStatus.INCOMMING
DEFAULT_TYPE = AgendaType.UNIQUE

class Agenda(MODEL):
    __tablename__ = AGENDA

    id = sap.Column(sap.Integer(), sap.Sequence(f'{__tablename__}{sap.ID}{sap.SEQ}'), primary_key=True)
    boss = sap.Column(sap.String(MEDIUM_STRING_SIZE))
    scope = sap.Column(sap.String(MEDIUM_STRING_SIZE))
    hoster = sap.Column(sap.String(MEDIUM_STRING_SIZE))
    beginAtDate = sap.Column(sap.Date) ###- sap.Column(sap.DateTime, default=datetime.datetime.utcnow)
    endAtDate = sap.Column(sap.Date)
    beginAtTime = sap.Column(sap.Time)
    endAtTime = sap.Column(sap.Time)
    notes = sap.Column(sap.String(GIANT_STRING_SIZE))
    status = sap.Column(sap.String(LITTLE_STRING_SIZE), default=DEFAULT_STATUS)
    type = sap.Column(sap.String(LITTLE_STRING_SIZE), default=DEFAULT_TYPE)
    url = sap.Column(sap.String(LARGE_STRING_SIZE))
    weekDay = sap.Column(sap.Integer())

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
        status = None,
        type = None,
        url = None,
        weekDay = None
    ):
        self.id = id
        self.boss = boss
        self.scope = scope
        self.hoster = hoster
        self.beginAtDate = DateTimeHelper.forcedlyGetDate(beginAtDate)
        self.endAtDate = DateTimeHelper.forcedlyGetDate(endAtDate)
        self.beginAtTime = DateTimeHelper.forcedlyGetTime(beginAtTime)
        self.endAtTime = DateTimeHelper.forcedlyGetTime(endAtTime)
        self.notes = notes
        self.status = AgendaStatus.map(ConverterStatic.getValueOrDefault(status, DEFAULT_STATUS))
        self.type = AgendaType.map(ConverterStatic.getValueOrDefault(type, DEFAULT_TYPE))
        self.url = url
        self.weekDay = WeekDay.map(weekDay)

    def __repr__(self):
        return f'{self.__tablename__}(id: {self.id}, boss: {self.boss}, scope: {self.scope}, hoster: {self.hoster}, beginAt: {DateTimeHelper.of(date=self.beginAtDate, time=self.beginAtTime)}, endAt: {DateTimeHelper.of(date=self.endAtDate, time=self.endAtTime)}, notes: {self.notes}, status: {self.status}, type: {self.type}, url: {self.url})'
