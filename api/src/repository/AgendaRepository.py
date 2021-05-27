from python_helper import ObjectHelper, DateTimeHelper
from python_framework import SqlAlchemyProxy as sap
from python_framework import Repository

from enumeration.agenda.AgendaType import AgendaType
from enumeration.agenda.AgendaStatus import AgendaStatus

from model import Agenda

@Repository(model = Agenda.Agenda)
class AgendaRepository:

    def findAll(self) :
        return self.repository.findAllAndCommit(self.model)

    def existsById(self, id) :
        return self.repository.existsByIdAndCommit(id, self.model)

    def findById(self, id) :
        if self.existsById(id) :
            return self.repository.findByIdAndCommit(id, self.model)

    def notExistsById(self, id) :
        return not self.existsById(id)

    def save(self, model) :
        return self.repository.saveAndCommit(model)

    def saveAll(self, modelList):
        return self.repository.saveAllAndCommit(modelList)

    def deleteById(self, id):
        self.repository.deleteByIdAndCommit(id, self.model)

    def findAllByIdIn(self, idList) :
        modelList = self.repository.session.query(self.model).filter(self.model.id.in_(idList)).all()
        self.repository.session.commit()
        return modelList

    def findAllNextEventByQuery(self, query) :
        if ObjectHelper.isNotEmpty(query) :
            return self.repository.findAllNextEventByQuery(query, self.model)
        from util import DateTimeUtil
        dateNow, timeNow = DateTimeUtil.getTodayDateAndTodayTime()
        modelList = self.repository.session.query(self.model).filter(
            sap.and_(
                self.model.beginAtDate >= dateNow,
                self.model.beginAtTime >= timeNow
            )
        ).order_by(self.model.beginAtDate.asc()).limit(10).all()
        self.repository.session.commit()
        return modelList

    def findAllByTypeAndNotStatusAndNotPresentAgenda(self, type, status, dateNow, timeNow) :
        modelList = []
        weekDay = DateTimeHelper.getWeekDay(ofDate=dateNow, ofTime=timeNow)
        if ObjectHelper.isNotNone(status) and ObjectHelper.isNotNone(dateNow) and ObjectHelper.isNotNone(timeNow) :
            modelList = self.repository.session.query(self.model).filter(
                sap.and_(
                    sap.and_(
                        self.model.type == type,
                        self.model.status != status
                    ),
                    sap.or_(
                        sap.and_(
                            AgendaType.DAILY == self.model.type,
                            sap.or_(
                                self.model.beginAtTime > timeNow,
                                self.model.endAtTime < timeNow
                            )
                        ),
                        sap.and_(
                            AgendaType.WEEKLY == self.model.type,
                            sap.or_(
                                self.model.weekDay != weekDay,
                                sap.and_(
                                    self.model.weekDay == weekDay,
                                    sap.or_(
                                        self.model.beginAtTime > timeNow,
                                        self.model.endAtTime < timeNow
                                    )
                                )
                            )
                        )
                    )
                )
            ).all()
        self.repository.session.commit()
        return modelList

    def findAllByTypeAndPastDateAndPastTime(self, type, dateNow, timeNow) :
        modelList = []
        if ObjectHelper.isNotNone(type) and ObjectHelper.isNotNone(dateNow) and ObjectHelper.isNotNone(timeNow) :
            modelList = self.repository.session.query(self.model).filter(
                sap.and_(
                    self.model.type == type,
                    sap.or_(
                        self.model.endAtDate < dateNow,
                        sap.and_(
                            self.model.endAtDate == dateNow,
                            self.model.endAtTime <= timeNow
                        )
                    )
                )
            ).all()
        self.repository.session.commit()
        return modelList

    def findPresentAgenda(self, ofDate, ofTime) :
        if ObjectHelper.isNotNone(ofDate) and ObjectHelper.isNotNone(ofTime) :
            model = self.repository.session.query(self.model).filter(
                sap.and_(
                    AgendaStatus.INCOMMING == self.model.status,
                    sap.or_(
                        sap.and_(
                            sap.and_(
                                AgendaType.DAILY == self.model.type,
                                self.model.beginAtDate <= ofDate
                            ),
                            sap.and_(
                                self.model.beginAtTime <= ofTime,
                                self.model.endAtTime >= ofTime
                            )
                        ),
                        sap.or_(
                            sap.and_(
                                sap.and_(
                                    AgendaType.UNIQUE == self.model.type,
                                    self.model.beginAtDate == ofDate,
                                ),
                                sap.and_(
                                    self.model.beginAtTime <= ofTime,
                                    self.model.endAtTime >= ofTime
                                )
                            ),
                            sap.and_(
                                sap.and_(
                                    AgendaType.WEEKLY == self.model.type,
                                    self.model.weekDay == DateTimeHelper.getWeekDay(ofDate=ofDate, ofTime=ofTime)
                                ),
                                sap.and_(
                                    self.model.beginAtTime <= ofTime,
                                    self.model.endAtTime >= ofTime
                                )
                            )
                        )
                    )
                )
            ).first()
        else :
            model = None
        self.repository.session.commit()
        return model

    def thereIsPresentAgenda(self, ofDate, ofTime) :
        exists = False
        if ObjectHelper.isNotNone(ofDate) and ObjectHelper.isNotNone(ofTime) :
            exists = self.repository.session.query(sap.exists().where(
                sap.or_(
                    sap.and_(
                        sap.and_(
                            AgendaType.DAILY == self.model.type,
                            self.model.beginAtDate <= ofDate
                        ),
                        sap.and_(
                            self.model.beginAtTime <= ofTime,
                            self.model.endAtTime >= ofTime
                        )
                    ),
                    sap.or_(
                        sap.and_(
                            sap.and_(
                                AgendaType.UNIQUE == self.model.type,
                                self.model.beginAtDate == ofDate,
                            ),
                            sap.and_(
                                self.model.beginAtTime <= ofTime,
                                self.model.endAtTime >= ofTime
                            )
                        ),
                        sap.and_(
                            sap.and_(
                                AgendaType.WEEKLY == self.model.type,
                                self.model.weekDay == DateTimeHelper.getWeekDay(ofDate=ofDate, ofTime=ofTime)
                            ),
                            sap.and_(
                                self.model.beginAtTime <= ofTime,
                                self.model.endAtTime >= ofTime
                            )
                        )
                    )
                )
            )).one()[0]
        self.repository.session.commit()
        return exists

    def findAllOfDateAndFromTimeAndToTime(self, ofDate, fromTime, toTime) :
        if ObjectHelper.isNotNone(ofDate) and ObjectHelper.isNotNone(fromTime) and ObjectHelper.isNotNone(toTime) :
            modelList = self.repository.session.query(self.model).filter(
                sap.or_(
                    sap.and_(
                        sap.and_(
                            AgendaType.UNIQUE == self.model.type,
                            self.model.beginAtDate == ofDate,
                        ),
                        sap.and_(
                            self.model.beginAtTime >= fromTime,
                            self.model.beginAtTime <= toTime
                        )
                    ),
                    sap.and_(
                        sap.and_(
                            AgendaType.WEEKLY == self.model.type,
                            self.model.weekDay == DateTimeHelper.getWeekDay(ofDate=ofDate, ofTime=fromTime)
                        ),
                        sap.and_(
                            self.model.beginAtTime >= fromTime,
                            self.model.beginAtTime <= toTime
                        )
                    ),
                    sap.and_(
                        AgendaType.DAILY == self.model.type,
                        sap.and_(
                            self.model.beginAtTime >= fromTime,
                            self.model.beginAtTime <= toTime
                        )
                    )
                )
            ).all()
        else :
            modelList = []
        self.repository.session.commit()
        return modelList

    def findAllFromDateAndToDateAndFromTime(self, fromDate, toDate, fromTime) :
        if ObjectHelper.isNotNone(fromDate) and ObjectHelper.isNotNone(toDate) and ObjectHelper.isNotNone(fromTime) :
            filter = sap.and_(
                self.model.beginAtDate == fromDate,
                self.model.beginAtTime >= fromTime
            )
            if fromDate <= toDate :
                filter = sap.or_(
                    filter,
                    sap.and_(
                        sap.and_(
                            self.model.beginAtDate >= DateTimeHelper.plusDays(fromDate, days=1),
                            self.model.beginAtDate <= toDate
                        ),
                        self.model.beginAtTime >= DateTimeHelper.getDefaultTimeBegin()
                    )
                )
            filter = sap.and_(
                AgendaType.UNIQUE == self.model.type,
                filter
            )
            filter = sap.or_(
                filter,
                self.getFilterWeeklyFromDateAndToDateAndFromTime(fromDate, toDate, fromTime)
            )
            filter = sap.or_(
                filter,
                self.getFilterDailyFromDateAndToDateAndFromTime(fromDate, toDate, fromTime)
            )
            modelList = self.repository.session.query(self.model).filter(
                filter
            ).all()
        elif ObjectHelper.isNotNone(fromTime) :
            modelList = self.repository.session.query(self.model).filter(
                sap.and_(
                    sap.and_(
                        AgendaType.WEEKLY == self.model.type,
                        self.model.weekDay == DateTimeHelper.getWeekDay(ofDate=fromDate, ofTime=fromTime)
                    ),
                    self.model.beginAtTime >= fromTime
                )
            ).all()
        else :
            modelList = []
        self.repository.session.commit()
        return modelList

    def getFilterWeeklyFromDateAndToDateAndFromTime(self, fromDate, toDate, fromTime) :
        filter = sap.and_(
            sap.or_(
                self.model.beginAtDate <= fromDate,
                self.model.beginAtDate <= toDate
            ),
            sap.and_(
                self.model.weekDay == DateTimeHelper.getWeekDay(ofDate=fromDate, ofTime=fromTime),
                self.model.beginAtTime >= fromTime
            )
        )
        for day in range(1,7) :
            deltaInDays = DateTimeHelper.plusDays(fromDate, days=day)
            weekDay = DateTimeHelper.getWeekDay(ofDate=deltaInDays, ofTime=fromTime)
            if deltaInDays <= toDate :
                filter = sap.or_(
                    filter,
                    sap.and_(
                        self.model.weekDay == weekDay,
                        sap.or_(
                            self.model.beginAtDate <= fromDate,
                            self.model.beginAtDate <= toDate
                        )
                    )
                )
            else :
                break
        filter = sap.and_(
            AgendaType.WEEKLY == self.model.type,
            filter
        )
        return filter

    def getFilterDailyFromDateAndToDateAndFromTime(self, fromDate, toDate, fromTime) :
        filter = sap.and_(
            self.model.beginAtDate > fromDate,
            self.model.beginAtDate < toDate
        )
        filter = sap.and_(
            self.model.endAtDate > fromDate,
            self.model.endAtDate < toDate
        )
        filter = sap.or_(
            sap.and_(
                sap.or_(
                    self.model.endAtDate == fromDate,
                    self.model.beginAtTime >= fromTime
                ),
                sap.or_(
                    self.model.beginAtDate == toDate,
                    self.model.beginAtTime >= fromTime
                )
            ),
            filter
        )
        filter = sap.or_(
            sap.and_(
                self.model.beginAtDate < fromDate,
                self.model.endAtDate > toDate,
            ),
            filter
        )
        filter = sap.and_(
            AgendaType.DAILY == self.model.type,
            filter
        )
        return filter
