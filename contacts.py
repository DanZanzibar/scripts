from csv import DictReader, DictWriter
from os.path import join, exists
from os import remove
from datetime import date


DATA_DIR = '/home/zan/sync-general/bin/customer-contacts/'
FIELDNAMES = (
    'Customer No.',
    'Company',
    'City',
    'State',
    'Address',
    'Sub Type',
    'Bookings YTD',
    'Previous Years Bookings',
    'Last Contact',
    'Days Since Contact',
    'Priority'
)
ACCOUNTS_FILE = 'accounts.csv'
EXPORT_FILE = 'export.csv'
CONTACTS_FILE = 'contacts.csv'

TOP50 = {
    "None": (0, 90),
    "Low": (90, 90),
    "Medium": (90, 185),
    "High": (185, 10000)
}
TARGET = {
    "None": (0, 185),
    "Low": (185, 185),
    "Medium": (185, 365),
    "High": (365, 10000)
}
OTHER = {
    "None": (0, 365),
    "Low": (365, 730),
    "Medium": (730, 10000),
    "High": (10000, 10000)
}

SALES_RANGES = (0, 1000, 10000, 20000)


def read_csv_file(file_name: str) -> list[dict]:
    file_path = join(DATA_DIR, file_name)
    with open(file_path, 'r', newline='') as f:
        reader = DictReader(f)
        dict_list = []

        for row in reader:
            dict_list.append(row)

    return dict_list


def write_csv_file(file_name: str, dict_list: list[dict],
                   fieldnames: tuple[str]) -> None:
    file_path = join(DATA_DIR, file_name)
    with open(file_path, 'w', newline='') as f:
        writer = DictWriter(f, fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(dict_list)


def _strip_dict_whitespace(dictionary: dict[str, str]) -> dict:
    for key, value in dictionary.items():
        dictionary[key] = value.strip()
    return dictionary


def strip_csv_whitespace(file_name: str) -> None:
    dict_list = read_csv_file(file_name)
    fieldnames = [column for column in dict_list[0]]
    for each_dict in dict_list:
        each_dict = _strip_dict_whitespace(each_dict)
    write_csv_file(file_name, dict_list, fieldnames)


def find_account_by_cust_no(account_list: list[dict], cust_no: str) -> dict:
    match = None
    for account in account_list:
        if account['Customer No.'] == cust_no:
            match = account
            break

    return match


def import_from_q360() -> None:
    strip_csv_whitespace(EXPORT_FILE)
    export = read_csv_file(EXPORT_FILE)

    if exists(join(DATA_DIR, ACCOUNTS_FILE)):
        old_accounts = read_csv_file(ACCOUNTS_FILE)
        for account in export:
            cust_no = account['Customer No.']
            old_account = find_account_by_cust_no(old_accounts, cust_no)
            if old_account:
                account['Last Contact'] = old_account['Last Contact']

    write_csv_file(ACCOUNTS_FILE, export, FIELDNAMES)
    remove(join(DATA_DIR, EXPORT_FILE))


def days_since_contact(account: dict) -> int:
    days = 9999
    today = date.today()
    iso_date = account['Last Contact']
    if iso_date:
        last_contact = date.fromisoformat(iso_date)
        tdelta = today - last_contact
        days = tdelta.days

    return days


def _priority(account: dict, config_constant: dict[str, int]) -> str:
    days = account['Days Since Contact']
    account_priority = 'None'

    for priority in config_constant:
        if config_constant[priority][0] <= days < config_constant[priority][1]:
            account_priority = priority
            break

    return account_priority


def determine_priority(account: dict) -> str:
    cust_type = account['Sub Type']
    if cust_type == "TOP 50 - ZOWSLEY":
        priority = _priority(account, TOP50)
    elif cust_type == "2. TARGET (OUTSIDE)":
        priority = _priority(account, TARGET)
    else:
        priority = _priority(account, OTHER)

    return priority


def update_accounts_days_and_priority() -> None:
    accounts = read_csv_file(ACCOUNTS_FILE)
    for account in accounts:
        account['Days Since Contact'] = days_since_contact(account)
        account['Priority'] = determine_priority(account)
    write_csv_file(ACCOUNTS_FILE, accounts, FIELDNAMES)


def pull_activities_from_file() -> dict[str, set[str]]:
    strip_csv_whitespace(CONTACTS_FILE)
    activities = read_csv_file(CONTACTS_FILE)
    contacts = {}

    for activity in activities:
        if (cust_no := activity['Customer No.']) not in contacts:
            contacts[cust_no] = {activity['Date']}
        else:
            contacts[cust_no].add(activity['Date'])

    return contacts


def update_accounts_contacts() -> None:
    accounts = read_csv_file(ACCOUNTS_FILE)
    contacts = pull_activities_from_file()

    for account in accounts:
        cust_no = account['Customer No.']
        if cust_no in contacts:
            account['Last Contact'] = max(contacts[cust_no])

    write_csv_file(ACCOUNTS_FILE, accounts, FIELDNAMES)
    remove(join(DATA_DIR, CONTACTS_FILE))


def cieling_from_string(string: str) -> float:
    num = float(string)
    cieling_value = 0

    for x in range(0, len(SALES_RANGES) - 1):
        if SALES_RANGES[x] < num <= SALES_RANGES[x + 1]:
            cieling_value = SALES_RANGES[x + 1]
            break

    if num > SALES_RANGES[-1]:
        cieling_value = 100000

    return cieling_value


def account_sales_cieling(account: dict, sales_category: str) -> float:
    if sales_category == 'all':
        ytd = account['Bookings YTD']
        prev_year = account['Previous Years Bookings']
        total = float(ytd) + float(prev_year)
        value = cieling_from_string(str(total))
    else:
        value = cieling_from_string(account[sales_category])

    return value


def all_sales_cieling(account: dict) -> float:
    return account_sales_cieling(account, 'all')


def sort_type_helper(account: dict) -> int:
    cust_type = account['Sub Type']
    value = 3
    if cust_type == 'TOP 50 - ZOWSLEY':
        value = 1
    elif cust_type == '2. TARGET (OUTSIDE)':
        value = 2

    return value


def sort_priority_helper(account: dict) -> int:
    priority = account['Priority']
    if priority == 'High':
        value = 1
    elif priority == 'Medium':
        value = 2
    elif priority == 'Low':
        value = 3
    else:
        value = 4

    return value


def sort_days_helper(account: dict) -> int:
    return int(account['Days Since Contact'])


def sort_accounts() -> None:
    accounts = read_csv_file(ACCOUNTS_FILE)

    accounts.sort(key=sort_days_helper, reverse=True)
    accounts.sort(key=all_sales_cieling, reverse=True)
    accounts.sort(key=sort_type_helper)
    accounts.sort(key=sort_priority_helper)

    write_csv_file(ACCOUNTS_FILE, accounts, FIELDNAMES)


def run_as_script() -> None:
    initial_setup = not exists(join(DATA_DIR, ACCOUNTS_FILE))
    import_needed = initial_setup or exists(join(DATA_DIR, EXPORT_FILE))

    if import_needed:
        import_from_q360()

    if exists(join(DATA_DIR, CONTACTS_FILE)):
        update_accounts_contacts()

    update_accounts_days_and_priority()
    sort_accounts()


if __name__ == '__main__':
    run_as_script()
