import re
def findBeginAndEndIndexesOfRegex(line,regex):
    """
    Find match start and match end by giving regex
    :param line: String
    :param regex: some regexpr
    :return: begin and end of matching

    >>> [(x['start'],x['end']) for x in findBeginAndEndIndexesOfRegex(line="find string stop in this stop sentance",regex=re.compile(r"st.*?p",re.MULTILINE))]
    [(5, 16), (25, 29)]
    >>> findBeginAndEndIndexesOfRegex(line="find string stop in this stop sentance",regex=re.compile(r"nostop",re.MULTILINE))
    []
    """
    matches = re.finditer(regex, line)
    str_matches = []
    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
        str_matches.append({'start': match.start(), 'end': match.end()})
    return str_matches

def match_inside_matches_array(match, matches):
    """
    Do we inside match area
    :param match: one match with start and end fields
    :param matches: array of matching data
    :return: True if inside False othercase
    >>> matches =  [{'start': 0, 'end': 2}, {'start': 6, 'end': 8}, {'start': 11, 'end': 13}]
    >>> match_inside_matches_array({'start':2,'end':5},matches)
    False
    >>> match_inside_matches_array({'start':0,'end':2},matches)
    True

    """
    for m in matches:
        if match['start']>=m['start'] and match['end']<=m['end']:
            return True
    return False


def get_linux_commands():
 return ['adduser', 'arch', 'awk', 'bc', 'cal','cd', 'cat', 'chdir', 'chgrp', 'chkconfig', 'chmod', 'chown', 'chroot', 'cksum', 'clear', 'cmp', 'comm', 'cp', 'cron', 'crontab', 'csplit', 'cut', 'date', 'dc', 'dd', 'df', 'diff', 'diff3', 'dir', 'dircolors', 'dirname', 'du', 'echo', 'ed', 'egrep', 'eject', 'env', 'expand', 'expr', 'factor', 'FALSE', 'fdformat', 'fdisk', 'fgrep', 'find', 'fmt', 'fold', 'format', 'free', 'fsck', 'gawk', 'grep', 'groups', 'gzip', 'head', 'hostname', 'id', 'info', 'install', 'join', 'kill', 'less', 'ln', 'locate', 'logname', 'lpc', 'lpr', 'lprm', 'ls', 'man', 'mkdir', 'mkfifo', 'mknod', 'more', 'mount', 'mv', 'nice', 'nl', 'nohup', 'passwd', 'paste', 'pathchk', 'pr', 'printcap', 'printenv', 'printf', 'ps', 'pwd', 'quota', 'quotacheck', 'quotactl', 'ram', 'rcp', 'rm', 'rmdir', 'rpm', 'rsync', 'screen', 'sdiff', 'sed', 'select', 'seq', 'shutdown', 'sleep', 'sort', 'split', 'su', 'sum', 'symlink', 'sync', 'tac', 'tail', 'tar', 'tee', 'test', 'time', 'touch', 'top', 'traceroute', 'tr', 'TRUE', 'tsort', 'tty', 'umount', 'uname', 'unexpand', 'uniq', 'units', 'unshar', 'useradd', 'usermod', 'users', 'uuencode', 'uudecode', 'vdir', 'watch', 'wc', 'whereis', 'which', 'who', 'whoami', 'xargs', 'yes']