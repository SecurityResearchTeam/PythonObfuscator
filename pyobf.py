import re

class Obfuscator:
    input_str = ""
    words = []
    frequencies = []
    output_lines = []

    def __init__(self, s):
        self.input_str = s
        self.words = []
        self.frequencies = []
        self.output_lines = []

    def add_terminal(self, m):
        if m.group(1) not in self.words:
            self.words.append(m.group(1))
            self.frequencies.append(1)
        else:
            self.frequencies[self.words.index(m.group(1))] += 1
        return ""
        #return hex(len(self.words) - 1)[2:]

    def simple(self):
        '''
        simplistic version of obfuscating the script by using the exec() command
        would be slow if the script is long and sophisticated
        '''
        #get rid of the Windows Line Breaks (might be optional)
        indent_size = 0
        indent_checked = False
        s = self.input_str.replace("\r\n", "\n").split("\n")
        for i in xrange(len(s)):
            #check indentation
            line = s[i].replace("\t", "(>)")
            if line.startswith(" ") and not indent_checked:
                while line.startswith(" "):
                    line = line[1:]
                    indent_size += 1
                indent_checked = True
            if indent_size > 0:
                line = s[i].replace(" " * indent_size, "(>)")
            s[i] = line
            #replace quotes
            s[i] = s[i].replace("'", "\\'")
            s[i] = s[i].replace('"', '\\"')
            #add words
            regex_terminal =  re.search(r"([A-Za-z0-9_.]+)", line)
            while regex_terminal != None:
                line = re.sub(r"([A-Za-z0-9_.]+)", self.add_terminal, line, count=1)
                regex_terminal = re.search(r"([A-Za-z0-9_.]+)", line)

        #sort words
        self.words.sort(key=dict(zip(self.words, self.frequencies)).get)
        self.frequencies = sorted(self.frequencies)
        self.words.reverse()
        self.frequencies.reverse()

        #replace words
        for i in xrange(len(s)):
            line = s[i]
            for word in self.words:
                line = re.sub(r"\b" + word + r"\b", hex(self.words.index(word))[2:], line)
            s[i] = line

            s[i] = s[i].replace("(>)", "\\t")

        self.output_lines = s[:]
        return "\\n".join(s)

    def build_simple(self):
        '''
        return a string of obfuscated python script
        '''
        obf_str = self.simple().replace("\\", "\\\\")
        words_str = "|".join(self.words)

        return """exec('''import re\\nexec((lambda p,y:(lambda o,b,f:re.sub(o,b,f))(r"([0-9a-f]+)",lambda m:p(m,y),"%s"))(lambda a,b:b[int("0x"+a.group(1),16)],"%s".split("|")))''')""" % (obf_str, words_str)
