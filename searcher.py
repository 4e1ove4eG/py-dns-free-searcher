import re
import string
import subprocess
from itertools import combinations_with_replacement
def is_domain_part_valid(part):
    return part[0] != '-' and part[-1] != '-'



def domain_list_generator(domain_names):
    combinations = combinations_with_replacement(string.ascii_lowercase + '-', 3)
    result = []
    # read_last_domain_name()
    found_last_domain_name = False
    last_domain_name = read_last_domain_name()
    print(last_domain_name)
    for combination in combinations:
        if is_domain_part_valid(combination):
            for domain_name in domain_names:
                domain = (''.join(combination) + "." + domain_name)
                if last_domain_name == domain or last_domain_name == False:
                    found_last_domain_name = True
                    continue
                if not found_last_domain_name:
                    continue
                result.append(domain)
    return result

def save_last_domain_name(domainname: str):
    with open("lastdomainname.txt", 'w') as f:
        f.write(domainname)


def read_last_domain_name():
    with open("lastdomainname.txt", 'r') as f:
        last_domain_name = f.read()
        if len(last_domain_name.strip()) > 0:
            return last_domain_name
        return False


def save_domain_name(domain):
    with open('free_domains.lst', 'a+') as f:
        f.write(domain + '\n')

def domain_list_validator(domain_list):
    result = []
    re_expired_domain = re.compile(r'registrar|Expiry Date|Creation Date', flags=re.IGNORECASE)
    #read_last_domain_name()
    for domain in domain_list:
        print(f'checking domain name:{domain}')
        if is_free_domain_name(domain, re_expired_domain):
            print(f'free domain:{domain}!')
        #else:
        #    print("bbb.cc" + domain)
            save_last_domain_name(domain)
            save_domain_name(domain)
            result.append(domain)
    return result


def is_free_domain_name(domainname: str, re_expired_domain):
    d = subprocess.run(['whois', domainname], stdout=subprocess.PIPE)
    output = str(d.stdout)
    return not re_expired_domain.findall(output)

if __name__ == "__main__":
    # execute only if run as a script
    list = ['cc', 'us', 'vc', 'io', 'co', 'me', 'im']
    domain_list = domain_list_generator(list)
    print(domain_list)
    free_domains = domain_list_validator(domain_list)


