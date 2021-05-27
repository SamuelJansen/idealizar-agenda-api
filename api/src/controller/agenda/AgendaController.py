from python_framework import Controller, ControllerMethod, HttpStatus

from dto.agenda import AgendaDto

@Controller(url = '/agenda', tag='Agenda', description='Agenda controller')
class AgendaController:

    @ControllerMethod(
        requestClass = AgendaDto.AgendaRequestDto,
        responseClass = AgendaDto.AgendaResponseDto
    )
    def post(self, agendaDto):
        return self.service.agenda.create(agendaDto), HttpStatus.CREATED


@Controller(url = '/agenda/batch', tag='Agenda', description='Agenda controller')
class AgendaBatchController:

    @ControllerMethod(url = '/<string:fromDate>/<string:toDate>',
        responseClass=[[AgendaDto.AgendaResponseDto]]
    )
    def get(self, fromDate=None, toDate=None):
        return self.service.agenda.findAll(fromDate, toDate), HttpStatus.OK

    @ControllerMethod(
        requestClass = [[AgendaDto.AgendaRequestDto]],
        responseClass = [[AgendaDto.AgendaResponseDto]]
    )
    def post(self, dtoList):
        return self.service.agenda.createAll(dtoList), HttpStatus.CREATED
