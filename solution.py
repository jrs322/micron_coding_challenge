
class parsed_module:
    id = ""
    inputs = []
    output = []
    parameters = []
    sub_modules = []
    contents = ""
    def __init__(self, contents):
        self.id = ''
        self.inputs = [] #for multiple input types
        self.outputs = [] #for multiple output types
        self.wire = []
        self.sub_modules = []
        self. contents = contents
    def add_id(self, id):
        self.id = id
    def add_input(self, input):
        self.inputs.append(input)
    def add_output(self, output):
        self.outputs.append(output)
    def add_sub_modules(self, sub_module):
        self.sub_modules.append(sub_module)
    def add_content_line(self, contents):
        self.contents = contents #store this for later retrieval
    def add_wire(self, wire):
        self.wire.append(wire)


def main_parser(parse_file):
    #Parameters : str
    #list of class module
    start_index = 0;
    last_index = 0;
    my_modules = []
    sliced_string = ''
    corrected_lines = [] #once the new lines are removed each line
    # will be based on use of ; and endmodule in verilog
    f = open(parse_file, "r")
    lines = f.readlines()
    f.close()
    f = open(parse_file, "w")
    for line in lines: #This gets rid lines with comments while not getting rid of endmodule
        if '//' not in line or 'endmodule' in line:
            f.write(line)
    f.close()
    with open(parse_file, "r") as file:
        contents = file.read().replace('\n', '')
        while start_index < len(contents): #break down the contents by modules
            start_index = contents.find('module ', start_index)
            last_index = contents.find('endmodule', start_index)
            if start_index == -1:
                break
            #add the string between indecies to the contents of a parsed_module
            sliced_string = contents[start_index:(last_index+9)]
            obj = parsed_module(sliced_string)
            my_modules.append(obj)
            start_index = last_index + 9 #length of endmodule
        #now we will shift through my_modules.contents from ; to ; to add inputs,outputs, and  sub_modules
        for n in my_modules: #lets me sort through these content containers easily
            obj = my_modules[n]
            str = obj.contents
            str.replace(";", "; \n")
            for line in str:
                if "input" in line:
                    obj.add_input(line)
                elif "output" in line:
                    obj.add_ouput(line)
                elif "wire" in line:
                    obj.add_wire(line)
                elif "module" in line and "endmodule" not in line: #need to get module name for next part
                    module_name = line[line.find("module", 0)+7:line.find("(",0)]
                    obj.add_id(module_name)
                elif "module" not in line and "(" in line or ");" in line: #assume any line with ( or ); is sub_module
                    obj.add_sub_modules(line)
                else
                    print("blank line or endmodule")
        return my_modules

def module_counter(my_modules, module_name):
    index = 0;
    sub_mod = []
    all_ids = []
    count = []
    for i in my_modules:
        name = my_modules[i].id
        all_ids.append(name)
        if name == module_name:
            index = i
    selected_mod = my_modules[index]
    sub_mod = selected_mod.sub_modules
