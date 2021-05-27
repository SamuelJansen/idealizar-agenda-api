from python_framework import Controller, ControllerMethod, HttpStatus

from dto.agenda import AgendaDto

@Controller(url = '/agenda/ai', tag='AgendaAi', description='AgendaAi controller')
class AgendaAiController:

    @ControllerMethod(url = '/',
        requestHeaderClass = [AgendaDto.AgendaHeaderRequestDto],
        requestParamClass = [AgendaDto.AgendaParamRequestDto],
        responseClass = [[AgendaDto.AgendaResponseDto]]
    )
    def get(self, headers={}, params={}):
        return self.service.agenda.findNextEvent(headers, params), HttpStatus.OK
