from typing import Optional
import time

from db import cur, conn
from models import User
from sessions import Session
import utils

session = Session()


def login(username: str, password: str):
    current_user: Optional[User] = session.check_session()
    if current_user:
        return utils.BadRequest('You are already logged in', status_code=401)

    get_user_by_username = '''SELECT * FROM users WHERE username = %s;'''
    cur.execute(get_user_by_username, (username,))
    user_data = cur.fetchone()
    if not user_data:
        return utils.BadRequest('Username not found in the database')

    _user = User(username=user_data[1], password=user_data[2], role=user_data[3], status=user_data[4],
                 login_try_count=user_data[5])

    if password != _user.password:
        update_count_query = '''UPDATE users SET login_try_count = login_try_count + 1 WHERE username = %s;'''
        cur.execute(update_count_query, (_user.username,))
        conn.commit()
        if _user.login_try_count > 2:
            update_status_query = """update users set status = 'blocked' where username = %s"""
            cur.execute(update_status_query, (username,))
            conn.commit()
            time.sleep(30)
            return utils.BadRequest("Your account has been blocked for 3 wrong attempts")
        else:
            pass
        return utils.BadRequest('Incorrect password')
    else:
        update_status_query = '''UPDATE users SET status = 'active' WHERE username = %s;'''
        cur.execute(update_status_query, (_user.username,))
        conn.commit()

    session.add_session(_user)
    return utils.ResponseData('User successfully logged in')


while True:
    choice = input('Enter your choice: ')
    if choice == '1':
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        message = login(username, password)
        print(message)
    else:
        break
