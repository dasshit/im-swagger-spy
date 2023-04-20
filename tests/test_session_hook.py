def test_register_session_hook(session, swagger):

    swagger.register_as_hook(session)

    session.get('https://ya.ru/test')
