from python_helper import ObjectHelper
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

from dto.agenda import AgendaDto

@Validator()
class AgendaValidator:

    @ValidatorMethod()
    def validateModelIsFound(self, model) :
        if ObjectHelper.isNone(model) :
            raise GlobalException(message='There are no calls scheduled for this moment', status=HttpStatus.NOT_FOUND)
