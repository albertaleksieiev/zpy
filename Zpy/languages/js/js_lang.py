import os
import re
import json
from Zpy.languages.Language import Language
from Zpy.modules.helpful.zjs import zjs
import execjs

class JavascriptLanguage(Language):
    def __init__(self):
        super(JavascriptLanguage, self).__init__()
        self.lang_regex = r"( *?j )"
        self.lang_regex_compiled = re.compile( self.lang_regex)
        self.zjs = zjs(processor=None)
        #self.exec_command = ['fs = require("fs")','request = require("request")']
        self.exec_command=[]
    def prepare(self,line):
        """
        Remove `j` character at begin
        :param line: line to preparing
        :return: striped line without j-symbol at begining
        >>> prepare = JavascriptLanguage().prepare
        >>> prepare("   j [1,2,3,4].map( function(e) { return e*2 } )")
        '[1,2,3,4].map( function(e) { return e*2 } )'
        >>> prepare("j     some string")
        'some string'

        """
        return re.sub(self.lang_regex,"",line,1).strip()
    def isLangPrefix(self, line):
        return self.isLang(line)

    def isLang(self, line):
        """
        JS language contain upper case letter `j` at begin, like '   j [1,2,3,4].map( function(e) { return e*2 } )'
        :param line: command
        :return: True if this is js syntax False otherwise

        >>> isLang = JavascriptLanguage().isLang
        >>> isLang("  j  2 + 3 * 4")
        True
        >>> isLang(" 8 + 5")
        False
        """
        return self.lang_regex_compiled.match(line) is not None


    def complete(self, line):
        return ""

    def get_require_regex(self):
        """
        :return: regex for require statement
        """
        regex = r"(?:(?:var|const|\ *?)\s*(.*?)\s*=\s*)?require\(['\"]([^'\"]+)['\"](?:, ['\"]([^'\"]+a)['\"])?\);?"
        return regex

    def get_require_modules(self,str):
        """
        Find require statement
        :param str:
        :return: None if nothing finded, otherwise return arrays where elements is array with 2 elements, when first item is alias and second required module
        >>> g = JavascriptLanguage().get_require_modules
        >>> g('fs = require("fs");some=require("module")')
        [['fs', 'fs'], ['some', 'module']]
        >>> g('var req = require("request")')
        [['req', 'request']]
        >>> g("varreq=req")
        """

        requirements = []
        matches = re.finditer(self.get_require_regex(), str)
        for match in matches:
            if match.group(1) is not None and match.group(2) is not None:
                requirements.append([match.group(1),match.group(2)])
        if len(requirements) == 0:
            return None
        return requirements

    def evaluate(self, line, processor=None, stdin=""):
        """
        Evaluate js code
        :param line: line for evaluation
         param processor: Zpy processor
        :param stdin: stdin will be passed to lang as Z variable
        :return: evaluation results
        >>> eval = JavascriptLanguage().evaluate
        >>> eval("j setTimeout(function(){ sync_err('ASYNC') },200)")
        Traceback (most recent call last):
           ...
        execjs._exceptions.ProgramError: ASYNC
        >>> eval("j setTimeout(function(){ sync('ASYNC') },200)")
        'ASYNC'
        >>> eval('j 2 + 3')
        5
        """

        # >>> eval("j fs.writeFileSync('/tmp/zpy.tmp', 'Zpy work with js!!!')")
        # >>> eval("j fs.readFileSync('/tmp/zpy.tmp', 'utf8')")
        #'Zpy work with js!!!'
        line = self.prepare(line)

        requirements = self.get_require_modules(line)
        if requirements is not None:
            for requirement in requirements:
                comm = "%s = require('%s')" % (requirement[0],requirement[1])
                if comm not in requirement:
                    self.exec_command.append(comm)
            return "Added new requirements : { %s }" % str(requirements)



        # Add default imports
        default_imports = self.zjs.get_def_imports_dict()
        for name, imp in default_imports.items():
            comm = "%s = %s"%(name,imp)
            if comm not in self.exec_command:
                self.exec_command.append(comm)


        z_variable = [] if stdin=="" else ['var z = %s' % json.dumps(stdin)]

        sync_add_function = """
                   var sync_add = function(val){
                       sync_end.results.push(val)
                   }
               """
        sync_end_function = """
                   var sync_end = function(){
                      process.stdout.write(JSON.stringify(['ok',sync_end.results]));
                      process.stdout.write(  '\\n' );
                      process.exit(0)
                   }
                   sync_end.results = []
               """
        sync_function = """
            var sync = function(val) {
                process.stdout.write(JSON.stringify(['ok',val]));
                process.stdout.write(  '\\n' );
                process.exit(0)
            } """
        sync_err = """
            var sync_err = function(err){
                process.stdout.write(JSON.stringify(['err',  err]));
               process.stdout.write(  '\\n' );
               process.exit(0)
            }
        """


        regex_syncs_functions = r"sync_err.*?\(.*?\) | sync\(.*?\)"

        for _ in (re.finditer(regex_syncs_functions, line)):
            if(len(line)) > 0:
                line =   "(" + line  + """) && Object.assign(function() { } ,{'skip_print':"zkip_"})""" #Set result of evaluation  undefined, remove converting our function to result
            break


        ctx = execjs.compile(";\n".join(self.exec_command \
                                       + z_variable       \
                                       +[sync_function,sync_err] ))
        return ctx.eval(line)
