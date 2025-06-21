import tkinter as tk

INPUT_WIDTH = 50

def formmated_list2str(lines, new_line = False):
    if not lines:
        return "[]"
    result = "["
    for line in lines:
        result += "'%s', " % line
        if new_line:
            result += '\n'
    result = result[:-2] + "]"
    return result

def _widget_select_all(event):
    
    # select text
    event.widget.event_generate('<<SelectAll>>')
    # event.widget.select_range(0, 'end')
    # move cursor to the end
    # event.widget.icursor('end')
    #stop propagation
    return 'break'

def new_TextBox(frame, text = "", read_only = False, width=100, expand=True, side="top"):
    
    state = tk.NORMAL
    # if read_only:
    #     state = tk.DISABLED
    text_box = tk.Text(frame, width=width, font=("Arial", 12), state=state)
    if read_only:
        text_box.bind("<Key>", lambda e: "break")#make the textbox read-only
    if text:
        text_box.insert( "1.0", text)
    text_box.bind('<Control-a>', _widget_select_all)
    text_box.pack(side="top", fill="both", expand=expand)
    return text_box

class FastFormatter:

    def __init__(self, func_dict, title="Fast Formatter"):
        self.func_dict = func_dict
        root = tk.Tk()
        self.root = root
        root.title(title)

        # Create frames for side-by-side placement
        input_frame = tk.Frame(root, width=INPUT_WIDTH)
        output_frame = tk.Frame(root, width=(100-INPUT_WIDTH))

        # Create input box with label and initial text
        input_label = tk.Label(input_frame, text="Input:")
        input_label.pack(side="top", fill="x")
        
        control_bar_in = tk.Frame(input_frame)
        tk.Button(control_bar_in, text="Clear", command=self.button_clear).pack(side="left", padx=5, pady=5)
        control_bar_in.pack(side="top", fill="x")# pack control_bar_out

        self.input_box = new_TextBox(input_frame, width=INPUT_WIDTH, expand=True, side="top")
        self.input_box.bind('<Control-r>', self.button_apply_formatted)
        # Create output box with label and initial text, set state to readonly
        output_label = tk.Label(output_frame, text="Output:")
        output_label.pack(side="top", fill="x")

        #   --control_bar_out--
        control_bar_out = tk.Frame(output_frame)
        #---Dropdown---
        if not func_dict:
            raise Exception("the 'func_dict' is empty")
        # Dropdown menu options
        options = list(func_dict.keys())
        if not func_dict:
            raise Exception("the 'func_dict' is empty or invalid")
        # datatype of menu text 
        drop_val = tk.StringVar()
        self.drop_val = drop_val
        # initial menu text 
        drop_val.set(options[0])

        # Create Dropdown menu 
        self.drop = tk.OptionMenu(control_bar_out, drop_val, *options) 
        self.drop.pack(side="left", padx=5, pady=5)
        #  Buttons
        tk.Button(control_bar_out, text="Formatted", command=self.button_apply_formatted).pack(side="left", padx=5, pady=5)
        tk.Button(control_bar_out, text="List", command=self.button_apply_list).pack(side="left", padx=5, pady=5)
        tk.Button(control_bar_out, text="Copy", command=self.button_copy).pack(side="left", padx=5, pady=5)
        # pack control_bar_out
        control_bar_out.pack(side="top", fill="x")

        # output_box = tk.Text(output_frame, width=(100-INPUT_WIDTH), font=("Arial", 12), state="disabled")
        self.output_box = new_TextBox(output_frame, read_only=True, width=(100-INPUT_WIDTH), expand=True)

        # Place the frames side-by-side
        input_frame.pack(side="left", fill="both", expand=True)
        output_frame.pack(side="right", fill="both", expand=True)

        root.mainloop()

    def button_copy(self):
        # Get the output text and copy it to clipboard
        output_text = self.output_box.get(1.0, tk.END).strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(output_text)
        
    def __apply_filter(filter_fun, val):
        tmp = filter_fun(val)
        if type(tmp) == bool and tmp:
            tmp = val
        return tmp

    def get_result_list(self):
        input_text = self.input_box.get(1.0, tk.END)
        output_text = str()
        filter_fun = self.func_dict[self.drop_val.get()]
        
        result_list = list()
        dup_dict = dict()
        input_list = [i.strip() for i in input_text.split("\n") if i.isprintable()]
        for i in input_list:
            tmp = filter_fun(i)
            if type(tmp) == bool and tmp:
                tmp = i
            
            if tmp and tmp not in dup_dict:
                dup_dict[tmp] = True
                result_list.append(tmp)
        return result_list

    def button_apply(self, event=None):
        input_text = self.input_box.get(1.0, tk.END)
        output_text = str()
        filter_fun = self.func_dict[self.drop_val.get()]
        
        result_list = list()
        dup_dict = dict()
        input_list = [i.strip() for i in input_text.split("\n") if i.isprintable()]
        for i in input_list:
            tmp = filter_fun(i)
            if type(tmp) == bool and tmp:
                tmp = i
            
            if tmp and tmp not in dup_dict:
                dup_dict[tmp] = True
                result_list.append(tmp)
            
        # output_text = str(result_list).replace(", ", ",\n")
        # output_text = str(result_list)
        output_text = "\n".join(result_list)
    
        #write to output_box
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert( "1.0", output_text)

    def button_apply_list(self, event=None):
        result_list = self.get_result_list()
        output_text = "\n".join(result_list)
        #write to output_box
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert( "1.0", output_text)
    
    def button_apply_formatted(self, event=None):
        result_list = self.get_result_list()
        # output_text = str(result_list).replace(", ", ",\n")
        output_text = str(result_list)
        #write to output_box
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert( "1.0", output_text)

    def button_clear(self):
        self.input_box.delete('1.0', tk.END)

