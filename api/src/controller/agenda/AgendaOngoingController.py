from python_framework import Controller, ControllerMethod, HttpStatus

from dto.agenda import AgendaDto

@Controller(url = '/agenda', tag='Agenda', description='Agenda controller')
class AgendaOngoingController:

    @ControllerMethod(url = '/present',
        responseClass = AgendaDto.AgendaResponseDto
    )
    def get(self):
        return self.service.agenda.findPresentAgendaAndOpenItIfActiveEnvironmentIsLocal(), HttpStatus.OK
