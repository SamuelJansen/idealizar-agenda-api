from python_framework import Enum, EnumItem

@Enum()
class AgendaStatusEnumeration :
    INCOMMING = EnumItem()
    ONGOING = EnumItem()
    PAST = EnumItem()

AgendaStatus = AgendaStatusEnumeration()
