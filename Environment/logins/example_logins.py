from bs4 import BeautifulSoup


def wp_login(session):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'}

    html_data = session.get("http://localhost:8000/wp-login.php", headers=headers)

    form_soup = BeautifulSoup(html_data.content, 'html.parser')
    form = form_soup.find('form', {'id': 'loginform'})
    inputs = {}
    for current_input in form.find_all('input'):
        input_name = current_input.attrs.get("name")
        if input_name not in {"log", "pwd"}:
            inputs[input_name] = current_input.attrs.get("value")

    url = "http://localhost:8000/wp-login.php"
    inputs["log"] = "a"
    inputs["pwd"] = "password"

    session.post(url, data=inputs, headers=headers)
    return session


def mediawiki_login(session):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'}

    html_data = session.get("http://localhost:8000/index.php?title=Special:UserLogin", headers=headers)

    form_soup = BeautifulSoup(html_data.content, 'html.parser')
    form = form_soup.find('form', {'name': 'userlogin'})
    inputs = {}
    for current_input in form.find_all('input'):
        input_name = current_input.attrs.get("name")
        if input_name not in {"wpName", "wpPassword"}:
            inputs[input_name] = current_input.attrs.get("value")

    url = "http://localhost:8000/index.php/Special:UserLogin"
    inputs["wpName"] = "server"
    inputs["wpPassword"] = "Qazwsxedcr12@"

    # print(inputs)
    session.post(url, data=inputs, headers=headers)
    return session


def kanboard_login(session):

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'}

    html_data = session.get("http://localhost:8008/?controller=AuthController&action=login", headers=headers)

    form_soup = BeautifulSoup(html_data.content, 'html.parser')

    csrf_token = form_soup.find('input', {'name': 'csrf_token'})['value']

    url = "http://localhost:8008/?controller=AuthController&action=check"
    data = {
        "username": "admin",
        "password": "admin",
        "csrf_token": csrf_token

    }
    # print(data)
    session.post(url, data=data, headers=headers)
    return session


def dolibar_login(session):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'}

    html_data = session.get("http://localhost:8000/index.php", headers=headers)

    form_soup = BeautifulSoup(html_data.content, 'html.parser')

    token = form_soup.find('input', {'name': 'token'})['value']
    actionlogin = form_soup.find('input', {'name': 'actionlogin'})['value']
    loginfunction = form_soup.find('input', {'name': 'loginfunction'})['value']
    tz = form_soup.find('input', {'name': 'tz'})['value']
    tz_string = form_soup.find('input', {'name': 'tz_string'})['value']
    dst_observed = form_soup.find('input', {'name': 'dst_observed'})['value']
    dst_first = form_soup.find('input', {'name': 'dst_first'})['value']
    dst_second = form_soup.find('input', {'name': 'dst_second'})['value']
    screenwidth = form_soup.find('input', {'name': 'screenwidth'})['value']
    screenheight = form_soup.find('input', {'name': 'screenheight'})['value']
    dol_hide_topmenu = form_soup.find('input', {'name': 'dol_hide_topmenu'})['value']
    dol_hide_leftmenu = form_soup.find('input', {'name': 'dol_hide_leftmenu'})['value']
    dol_optimize_smallscreen = form_soup.find('input', {'name': 'dol_optimize_smallscreen'})['value']
    dol_no_mouse_hover = form_soup.find('input', {'name': 'dol_no_mouse_hover'})['value']
    dol_use_jmobile = form_soup.find('input', {'name': 'dol_use_jmobile'})['value']

    url = "http://localhost:8000/index.php?mainmenu=home"
    data = {
        "username": "server",
        "password": "Qazwsxedcr12@",
        "token": token,
        "actionlogin": actionlogin,
        "loginfunction": loginfunction,
        "tz": tz,
        "tz_string": tz_string,
        "dst_observed": dst_observed,
        "dst_first": dst_first,
        "dst_second": dst_second,
        "screenwidth": screenwidth,
        "screenheight": screenheight,
        "dol_hide_topmenu": dol_hide_topmenu,
        "dol_hide_leftmenu": dol_hide_leftmenu,
        "dol_optimize_smallscreen": dol_optimize_smallscreen,
        "dol_no_mouse_hover": dol_no_mouse_hover,
        "dol_use_jmobile": dol_use_jmobile

    }
    session.post(url, data=data, headers=headers)
    return session


def b2_login(self):
    html_data = self.session.get(
        "http://localhost:8888/b2evolution/index.php?disp=login&redirect_to=%2Fb2evolution%2Findex.php%3Fblog%3D1&return_to=%2Fb2evolution%2Findex.php%3Fblog%3D1&source=menu%20link")
    form_soup = BeautifulSoup(html_data.content, 'html.parser')
    crumb_loginform = form_soup.find('input', {'name': 'crumb_loginform'})['value']
    source = form_soup.find('input', {'name': 'source'})['value']
    redirect_to = form_soup.find('input', {'name': 'redirect_to'})['value']
    return_to = form_soup.find('input', {'name': 'return_to'})['value']
    # validate_required = form_soup.find('input', {'name':'validate_required'})['value']
    pepper = form_soup.find('input', {'name': 'pepper'})['value']

    url = "http://localhost:8888/b2evolution/index.php?disp=login&redirect_to=%2Fb2evolution%2Findex.php%3Fblog%3D1&return_to=%2Fb2evolution%2Findex.php%3Fblog%3D1&source=menu%20link"
    data = {
        "x": "admin",
        "q": "WVV695xvHZ5xsq",
        "crumb_loginform": crumb_loginform,
        "source": source,
        "redirect_to": redirect_to,
        "return_to": return_to,
        # "validate_required":validate_required,
        "pepper": pepper
    }
    r = self.session.post(url, data=data)


def spark_login(session):

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'}

    url = "http://localhost:8888/hotel_management_system/ajax.php"
    data = {
        "username": "a",
        "password": "a",
        "login": ''

    }

    session.post(url, data=data, headers=headers)
    return session


def elearning_login(session):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'}

    url = "http://localhost:8888/vcs/register.php"
    data = {
        "log_email": "cblake@mail.com",
        "log_password": "cblake123",
        "login_button": 'Login'

    }
    session.post(url, data=data, headers=headers)
    return session