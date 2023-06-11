import subprocess


def get_username(account_name):
    pipe = subprocess.run(['awk',
                           '-F',
                           ' ',
                           "/" + account_name + "/ { print $(NF-2); exit; }",
                           '/home/zan/.authinfo'],
                          capture_output=True,
                          text=True)
    username = pipe.stdout.strip('\n')
    return username


def get_password(account_name):
    pipe = subprocess.run(['awk',
                           '-F',
                           ' ',
                           "/" + account_name + "/ { print $NF; exit; }",
                           '/home/zan/.authinfo'],
                          capture_output=True,
                          text=True)
    password = pipe.stdout.strip('\n')
    return password


def get_work_username():
    pipe = subprocess.run(['awk',
                           '-F',
                           ' ',
                           "/work/ { print $(NF-6); exit; }",
                           '/home/zan/.authinfo'],
                          capture_output=True,
                          text=True)
    username = pipe.stdout.strip('\n')
    return username


def get_client_id():
    pipe = subprocess.run(['awk',
                           '-F',
                           ' ',
                           "/work/ { print $(NF-4); exit; }",
                           '/home/zan/.authinfo'],
                          capture_output=True,
                          text=True)
    client_id = pipe.stdout.strip('\n')
    return client_id


def get_client_secret():
    pipe = subprocess.run(['awk',
                           '-F',
                           ' ',
                           "/work/ { print $(NF-2); exit; }",
                           '/home/zan/.authinfo'],
                          capture_output=True,
                          text=True)
    client_secret = pipe.stdout.strip('\n')
    return client_secret


def get_refresh_token():
    pipe = subprocess.run(['awk',
                           '-F',
                           ' ',
                           "/work/ { print $NF; exit; }",
                           '/home/zan/.authinfo'],
                          capture_output=True,
                          text=True)
    refresh_token = pipe.stdout.strip('\n')
    return refresh_token
