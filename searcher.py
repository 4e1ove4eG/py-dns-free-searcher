import re
import string
import subprocess
from itertools import combinations_with_replacement

# TODO обработка whois таймаут
# TODO: вынести в отдельный модуль и имплементировать класс сохранения и извлечения строки из файла
class StringPersistence:
    string = ""

    def get(self):
        return self.string

    def set(self, value: str):
        self.string = value


# TODO: перененести is_domain_part_valid и domain_list_generator в отдельный модуль генерации имен

def is_domain_part_valid(part):
    return part[0] != '-' and part[-1] != '-'


# TODO: добавить функционал востановления с меcта последней остановки и сохранения текущего состояния
def domain_list_generator(domain_name: str, start: str = None):
    combinations = combinations_with_replacement(string.ascii_lowercase + '-', 3)
    result = []
    for combination in combinations:
#        if
        if is_domain_part_valid(combination):
            result.append(''.join(combination) + "." + domain_name)
    # TODO: заменить на yield и рассказать про генераторы
    return result


# TODO: перененести domain_list_validator и is_free_domain_name в отдельный модуль проверки DNS

def domain_list_validator(dns_list, on_each_iteration_callback):
    result = []
    re_expired_domain = re.compile(r'registrar|Expiry Date|Creation Date', flags=re.IGNORECASE)
    for domain in dns_list:
        if is_free_domain_name(domain, re_expired_domain):
            print(domain)
            result.append(domain)
        on_each_iteration_callback(domain)
    return result


def load_string_from_file():
    filename = "last_domain.txt"
    with open(filename, 'r') as file:
        data = file.read()
    return data


def load_string_from_file(string: str):
    print(string)
    filename = "last_domain.txt"
    with open(filename, "w") as text_file:
        print(f"{string}", file=text_file)
    return None


def is_free_domain_name(domainname: str, re_expired_domain):
    d = subprocess.run(['whois', domainname], stdout=subprocess.PIPE)
    output = str(d.stdout)
    return not re_expired_domain.findall(output)


if __name__ == "__main__":
    # execute only if run as a script
    start = load_string_from_file()
    print("Start from previous state: " + start)
    domain_list = domain_list_generator('io', start)
    free_domains = domain_list_validator(domain_list, save_string_to_file)
    print(domain_list)
