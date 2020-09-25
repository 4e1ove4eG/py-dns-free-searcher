import re
import string
import subprocess
from itertools import combinations_with_replacement
def is_domain_part_valid(part):
    return part[0] != '-' and part[-1] != '-'



def domain_list_generator(domain_name):
    combinations = combinations_with_replacement(string.ascii_lowercase + '-', 3)
    result = []
    for combination in combinations:
        if is_domain_part_valid(combination):
            result.append(''.join(combination) + "." + domain_name)
    return result


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


