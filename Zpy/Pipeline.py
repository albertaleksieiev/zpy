import re

from Zpy.Utils import findBeginAndEndIndexesOfRegex,match_inside_matches_array

class Pipeline:

    def findStrs(self,line):
        """
        finds string inside string - "some big string 'SUBSTRING'"
        :param line: Line with string
        :return: begin and end index of substring

        >>> [(x['start'],x['end']) for x in Pipeline().findStrs("echo 'cat' | is not a 'cot' ")]
        [(5, 10), (22, 27)]
        """
        return findBeginAndEndIndexesOfRegex(line=line,regex=re.compile(r"(\"|\').*?(\"|\')",re.MULTILINE))

    def split(self,line):
        """
        Split string by |
        :param line: some string with pipes
        :return: splited tokens

        #>>> Pipeline().split("ls | os.listdir(z) | cat 'some \'| magic'  | file.txt' ")
        >>> Pipeline().split("ls|asd|qwe|zxc|qqq")
        ['ls', 'asd', 'qwe', 'zxc', 'qqq']
        >>> Pipeline().split("cat 'asd|.txt' | z + '|no'")
        ["cat 'asd|.txt' ", " z + '|no'"]
        >>> Pipeline().split("")
        ['']
        """

        if len(line) == 0:
            return ['']

        str_matches = self.findStrs(line=line)

        parts = findBeginAndEndIndexesOfRegex(line,regex=r"\|")

        pipeline_matches = list(filter(lambda match : not match_inside_matches_array(match,str_matches),parts))

        # It's just 1 command
        if len(line) > 0 and (len(parts) == 0 or len(pipeline_matches) == 0):
            return [line]

        begin_index = 0
        splits = []
        for match in pipeline_matches:
            splits.append(line[begin_index:match['start']])
            begin_index = match['end']
        if(len(pipeline_matches) > 0):
            splits.append(line[begin_index:].strip())

        return [s.strip() for s in splits]
