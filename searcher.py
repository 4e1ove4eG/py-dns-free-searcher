import re
import string
import subprocess
from itertools import combinations_with_replacement


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

# TODO: добавить функционал востановления с места последней остановки и сохранения текущего состояния
def domain_list_generator(domain_name: str, string_persistence: StringPersistence = None):
    combinations = combinations_with_replacement(string.ascii_lowercase + '-', 3)
    result = []
    for combination in combinations:
        if is_domain_part_valid(combination):
            result.append(''.join(combination) + "." + domain_name)
    # TODO: заменить на yield и рассказать про генераторы
    return result


# TODO: перененести domain_list_validator и is_free_domain_name в отдельный модуль проверки DNS

def domain_list_validator(domain_list):
    result = []
    re_expired_domain = re.compile(r'registrar|Expiry Date|Creation Date', flags=re.IGNORECASE)
    for domain in domain_list:
        if is_free_domain_name(domain, re_expired_domain):
            print(domain)
            result.append(domain)
    return result


def is_free_domain_name(domainname: str, re_expired_domain):
    d = subprocess.run(['whois', domainname], stdout=subprocess.PIPE)
    output = str(d.stdout)
    return not re_expired_domain.findall(output)


if __name__ == "__main__":
    # execute only if run as a script
    domain_list = domain_list_generator('io')
    free_domains = domain_list_validator(domain_list)
    print(domain_list)
