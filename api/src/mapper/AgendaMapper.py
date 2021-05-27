from python_framework import Mapper, MapperMethod

from model import Agenda
from dto.agenda import AgendaDto

@Mapper()
class AgendaMapper:

    @MapperMethod(requestClass=[[AgendaDto.AgendaRequestDto]], responseClass=[[Agenda.Agenda]])
    def fromRequestDtoListToModelList(self, dtoList, modelList) :
        for model in modelList :
            self.mapper.agenda.mapModelWeekDay(model)
        return modelList

    @MapperMethod(requestClass=[[Agenda.Agenda]], responseClass=[[AgendaDto.AgendaResponseDto]])
    def fromModelListToResponseDtoList(self, modelList, dtoList) :
        return dtoList

    @MapperMethod(requestClass=[AgendaDto.AgendaRequestDto], responseClass=[Agenda.Agenda])
    def fromRequestDtoToModel(self, dto, model) :
        self.mapper.agenda.mapModelWeekDay(model)
        return model

    @MapperMethod(requestClass=[Agenda.Agenda], responseClass=[AgendaDto.AgendaResponseDto])
    def fromModelToResponseDto(self, model, dto) :
        return dto

    @MapperMethod()
    def mapModelWeekDay(self, model) :
        model.weekDay = self.service.agenda.getWeekDayByModel(model)
