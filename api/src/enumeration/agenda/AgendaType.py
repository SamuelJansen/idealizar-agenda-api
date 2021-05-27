from python_framework import Enum, EnumItem

@Enum()
class AgendaTypeEnumeration :
    UNIQUE = EnumItem()
    WEEKLY = EnumItem()
    DAILY = EnumItem()

AgendaType = AgendaTypeEnumeration()
