# This file is licensed under the MPL-2.0 license.
# Copyright (c) 2023 Tianyi Network  https://luotianyi.dev
# You can get a copy of license from https://www.mozilla.org/en-US/MPL/2.0/

import os
import json
from urllib.request import Request, urlopen

UPSTREAM_API_URL    = os.environ.get("UPSTREAM_API_URL",   "http://127.0.0.1/api/v1/servers/localhost/zones")
UPSTREAM_API_KEY    = os.environ.get("UPSTREAM_API_KEY",   "password")
NAMED_BANNER_TEXT   = os.environ.get("NAMED_BANNER_TEXT",  "BIND9")
NAMED_CLUSTER_CIDR  = os.environ.get("NAMED_CLUSTER_CIDR", "10.0.0.0/24")
NAMED_UPSTREAM_IP   = os.environ.get("NAMED_UPSTREAM_IP",  "10.0.0.1")
NAMED_RNDC_KEY      = os.environ.get("NAMED_RNDC_KEY",     "YchZCzo4QMF+J9m/I/lPmgaMhZ9H7Y55wFFDDqKOD7s=")
NAMED_CONF_MAIN     = "/etc/bind/named.conf"
NAMED_CONF_UPSTREAM = "/etc/bind/upstream.conf"
NAMED_CONF_DOMAINS  = "/etc/bind/domains.conf"
NAMED_CONF_RNDC     = "/etc/bind/rndc.conf"

def show_variables():
    print("UPSTREAM_API_URL:",   UPSTREAM_API_URL)
    print("UPSTREAM_API_KEY:",   "*" * len(UPSTREAM_API_KEY))
    print("NAMED_BANNER_TEXT:",  NAMED_BANNER_TEXT)
    print("NAMED_CLUSTER_CIDR:", NAMED_CLUSTER_CIDR)
    print("NAMED_UPSTREAM_IP:",  NAMED_UPSTREAM_IP)
    print("NAMED_RNDC_KEY:",     "*" * len(NAMED_RNDC_KEY))

def fetch_domains() -> list[str]:
    request  = Request(UPSTREAM_API_URL, headers={"X-API-Key": UPSTREAM_API_KEY})
    response = json.loads(urlopen(request).read())
    domains  = [entry["name"][:-1] for entry in response]
    return domains

def apply_conf_template(filename: str):
    variables = {
        "NAMED_BANNER_TEXT":  NAMED_BANNER_TEXT,
        "NAMED_CLUSTER_CIDR": NAMED_CLUSTER_CIDR,
        "NAMED_UPSTREAM_IP":  NAMED_UPSTREAM_IP,
        "NAMED_RNDC_KEY":     NAMED_RNDC_KEY,
    }
    print("Generating:", filename)
    with open(filename) as f:
        content = f.read()
        for key, value in variables.items():
            content = content.replace(f"%{key}%", value)
    with open(filename, "w+") as f:
        f.write(content)

def generate_domain_conf(domains: list[str]):
    indent = max([len(d) for d in domains]) + 8
    content = []
    with open (NAMED_CONF_DOMAINS, "w+") as f:
        for domain in domains:
            domain_conf = f'"{domain}"'
            zone_conf   = f'"{domain}.zone"'
            print("Adding domain:", domain)
            content.append(
                'zone %DOMAIN% { file %ZONE%; include "%UPSREAM_CONF%"; };'
                    .replace("%DOMAIN%", f"{domain_conf:<{indent}}")
                    .replace("%ZONE%",   f'{zone_conf:<{indent}}')
                    .replace("%UPSREAM_CONF%", NAMED_CONF_UPSTREAM)
            )
        f.write("\n".join(content))

def main():
    show_variables()
    apply_conf_template(NAMED_CONF_MAIN)
    apply_conf_template(NAMED_CONF_UPSTREAM)
    apply_conf_template(NAMED_CONF_RNDC)
    domains = fetch_domains()
    generate_domain_conf(domains)

if __name__ == "__main__":
    main()
