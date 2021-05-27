import globals
globalsInstance = globals.newGlobalsInstance(__file__
    , settingStatus = True
    , successStatus = True
    , errorStatus = True
    , failureStatus = True
    , debugStatus = True

    , warningStatus = True
    # , wrapperStatus = True
    # , logStatus = True
    # , testStatus = True
)

from python_framework import initialize, runApi
import IdealizaAgendaApi
app = IdealizaAgendaApi.app
api = IdealizaAgendaApi.api
jwt = IdealizaAgendaApi.jwt

@initialize(api, defaultUrl = '/swagger', openInBrowser=False)
def runFlaskApplication(app):
    runApi(debug=False, use_reloader=False)

if __name__ == '__main__' :
    runFlaskApplication(app)
