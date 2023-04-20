import pathlib

import pytest

from im_swagger_spy import http_spy
from im_swagger_spy.syncdb import ReportInfo


@pytest.fixture(params=[
    '.',
    'sw-report',
    'sw-report/subdir'
])
def clean_report_folders(request):
    yield request.param

    report_folder_path = pathlib.Path(request.param)

    report_folder_path.joinpath(f'spy-report-vk_teams.botapi.html').unlink()

    if request.param == '.':
        return
    elif request.param == 'sw-report':
        report_folder_path.rmdir()
    else:
        report_folder_path.rmdir()
        report_folder_path.parent.rmdir()


def test_create_report(clean_report_folders):
    spy = http_spy.SwaggerHttpSpy(
        service_name='vk_teams.botapi',
        targets=['https://myteam.mail.ru/botapi/api.yaml?4624464'],
        api_prefix='/bot/v1',
        report_path=clean_report_folders
    )

    spy.load_schema()

    spy.report()

    spy.build_report()

    report_folder = pathlib.Path(spy.report_path)

    assert report_folder.exists() and report_folder.is_dir()

    report_filename = f'spy-report-{spy.service}.html'

    assert report_folder.joinpath(
        report_filename).exists(), \
        f'Report "{report_filename}" does not exist in {spy.report_path}'


def test_raise_report_on_none_path_value():
    spy = http_spy.SwaggerHttpSpy(
        service_name='vk_teams.botapi',
        targets=['https://myteam.mail.ru/botapi/api.yaml?4624464'],
        api_prefix='/bot/v1',
        report_path=None
    )

    with pytest.raises(ValueError):
        spy.report()


def test_report_regexp_path(swagger, session):

    swagger.register_as_hook(session)

    session.post('https://petstore.swagger.io/v2/pet/1/uploadImage')

    USED_METHODS_MODELS_LIST, SKIPPED_METHODS_MODELS_LIST = swagger.report_models()


def test_report_integrity_error(swagger):

    ReportInfo.create(**{
        'info_type': 'service', 'info_text': "self.service"
    })

    swagger.report()