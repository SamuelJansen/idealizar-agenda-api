from python_helper import Constant as c
from python_helper import ObjectHelper, StringHelper, SettingHelper, DateTimeHelper
from python_framework import Service, ServiceMethod, WebBrowser

from domain import AgendaConstants
from enumeration.agenda.AgendaType import AgendaType
from enumeration.agenda.AgendaStatus import AgendaStatus

from model import Agenda
from dto.agenda import AgendaDto

from util import DateTimeUtil

@Service()
class AgendaService:

    @ServiceMethod(requestClass = [AgendaDto.AgendaHeaderRequestDto, AgendaDto.AgendaParamRequestDto])
    def findNextEvent(self, headers, params) :
        query = {} if ObjectHelper.isNone(params) else {k:v for k, v in params.__dict__.items() if ObjectHelper.isNotNone(v)}
        # if 'dateTime' in query :
        #     dateTime = query.pop('dateTime')
        #     if ObjectHelper.isNotNone(dateTime) :
        #         try :
        #             query['beginAtDate'] = DateTimeHelper.dateOf(dateTime)
        #         except : pass
        #         try :
        #             query['beginAtTime'] = DateTimeHelper.timeOf(dateTime)
        #         except : pass
        modelList = self.repository.agenda.findAllNextEventByQuery(query)
        return self.mapper.agenda.fromModelListToResponseDtoList(modelList)

    @ServiceMethod(requestClass = AgendaDto.AgendaRequestDto)
    def create(self, dto):
        model = self.mapper.agenda.fromRequestDtoToModel(dto)
        self.repository.agenda.save(model)
        return self.mapper.agenda.fromModelToResponseDto(model)

    @ServiceMethod(requestClass = [[AgendaDto.AgendaRequestDto]])
    def createAll(self, dtoList):
        modelList = self.mapper.agenda.fromRequestDtoListToModelList(dtoList)
        self.repository.agenda.saveAll(modelList)
        return self.mapper.agenda.fromModelListToResponseDtoList(modelList)

    @ServiceMethod(requestClass=[str, str])
    def findAll(self, givenFromDate, givenToDate):
        if ObjectHelper.isNone(givenFromDate) or StringHelper.isBlank(givenFromDate.strip()) :
            fromDate, toDate, fromTime = DateTimeUtil.getDateMonthBeginAndToDateAndTimeMonthBegin()
        elif ObjectHelper.isNone(givenToDate) or StringHelper.isBlank(givenToDate.strip()) :
            toDate = DateTimeHelper.dateNow()
        else :
            fromDate = DateTimeHelper.forcedlyGetDate(givenFromDate)
            toDate = DateTimeHelper.forcedlyGetDate(givenToDate)
            fromTime = DateTimeHelper.timeNow() if DateTimeHelper.dateNow() == fromDate else DateTimeHelper.getDefaultTimeBegin()
        modelList = self.repository.agenda.findAllFromDateAndToDateAndFromTime(fromDate, toDate, fromTime)
        return self.mapper.agenda.fromModelListToResponseDtoList(modelList)

    @ServiceMethod()
    def findPresentAgendaAndOpenItIfActiveEnvironmentIsLocal(self):
        todayDate, todayTime = DateTimeUtil.getTodayDateAndTodayTime()
        model = self.repository.agenda.findPresentAgenda(todayDate, todayTime)
        self.validator.agenda.validateModelIsFound(model)
        if SettingHelper.activeEnvironmentIsLocal() :
            WebBrowser.openUrlInChrome(model.url)
        model.status = AgendaStatus.AgendaStatus.OPEN
        self.repository.agenda.save(model)
        return self.mapper.agenda.fromModelToResponseDto(model)

    @ServiceMethod()
    def thereIsNoPresentAgenda(self) :
        todayDate, todayTime = DateTimeUtil.getTodayDateAndTodayTime()
        return not self.repository.agenda.thereIsPresentAgenda(todayDate, todayTime)

    @ServiceMethod()
    def updateCurrentStatusOfAgendaList(self) :
        dateTimeNow = DateTimeHelper.dateTimeNow()
        dateNow = DateTimeHelper.dateOf(dateTime=dateTimeNow)
        timeNow = DateTimeHelper.timeOf(dateTime=dateTimeNow)
        uniqueModelList = self.repository.agenda.findAllByTypeAndPastDateAndPastTime(
            AgendaType.UNIQUE,
            dateNow,
            timeNow
        )
        for model in uniqueModelList :
            model.status = AgendaStatus.AgendaStatus.PAST
        dailyModelList = self.repository.agenda.findAllByTypeAndNotStatusAndNotPresentAgenda(
            AgendaType.DAILY,
            AgendaStatus.INCOMMING,
            dateNow,
            timeNow
        )
        for model in dailyModelList :
            model.status = AgendaStatus.AgendaStatus.INCOMMING
        weeklyModelList = self.repository.agenda.findAllByTypeAndNotStatusAndNotPresentAgenda(
            AgendaType.WEEKLY,
            AgendaStatus.INCOMMING,
            dateNow,
            timeNow
        )
        for model in weeklyModelList :
            model.status = AgendaStatus.AgendaStatus.INCOMMING
        self.repository.agenda.saveAll([*uniqueModelList, *dailyModelList, *weeklyModelList])

    @ServiceMethod()
    def findIncommingAgendaList(self):
        today, fromTime, toTime = DateTimeUtil.getTodayDateAndFromTimeNowMinusMinutesAndTodayEnd(marginInMinutes=AgendaConstants.DEFAULT_MARGIN_IN_MINUTES)
        modelList = self.repository.agenda.findAllOfDateAndFromTimeAndToTime(today, fromTime, toTime)
        return self.mapper.agenda.fromModelListToResponseDtoList(modelList)

    @ServiceMethod(requestClass = Agenda.Agenda)
    def getWeekDayByModel(self, model):
        return DateTimeHelper.getWeekDay(ofDate=model.beginAtDate, ofTime=model.beginAtTime)
