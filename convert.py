#!/usr/bin/env python3
import re, sys

def wildcard_to_regex(pattern: str) -> str:
    escaped = re.escape(pattern)
    escaped = escaped.replace(r'\*', r'[^/]*?')
    return f'^https?://{escaped}(/.*)?$'

def convert(input_file, whitelist_out, blacklist_out):
    rule_re = re.compile(r'^(@@)?\|\|(.+?)(\^?)(\$.*)?$')
    whitelist, blacklist = [], []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            raw = line.strip()
            if not raw or raw.startswith('!') or raw.startswith('#'):
                continue
            m = rule_re.match(raw)
            if not m:
                continue
            is_white = m.group(1) == '@@'
            domain_part = m.group(2).lower()
            if '*' in domain_part:
                rule = f'URL-REGEX,{wildcard_to_regex(domain_part)}'
            else:
                rule = f'DOMAIN-SUFFIX,{domain_part}'
            (whitelist if is_white else blacklist).append(rule)

    with open(whitelist_out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(whitelist))
    with open(blacklist_out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(blacklist))

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('用法: python convert.py <输入> <白名单输出> <黑名单输出>')
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2], sys.argv[3])