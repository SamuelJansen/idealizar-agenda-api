from python_framework import Controller, ControllerMethod, HttpStatus

from dto.agenda import AgendaDto

@Controller(url = '/agenda', tag='Agenda', description='Agenda controller')
class AgendaIncommingController:

    @ControllerMethod(url = '/incomming',
        responseClass=[[AgendaDto.AgendaResponseDto]]
    )
    def get(self):
        return self.service.agenda.findIncommingAgendaList(), HttpStatus.OK
