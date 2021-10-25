from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
import re
from decimal import Decimal

Builder.load_file('./calculator.kv')
Window.size = (320, 568)


# set maximum text input length
class MyTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        if len(self.text) > 9:
            substring = ""
        return super(MyTextInput, self).insert_text(substring, from_undo=from_undo)


class MyRoot(Widget):

    def press_btn(self, instance):
        self.text_input.focus = True

        btn_name = instance.name
        btn_text = instance.text
        if btn_name == 'btn_clr':
            # all clear
            self.text_input.text = ''
        elif btn_name == 'btn_del':
            # backspace
            input_text = self.text_input.text
            cursor_idx = self.text_input.cursor_col
            input_text_temp = input_text[0:cursor_idx]
            input_text_length = len(input_text_temp)
            if input_text_length > 0:
                input_text_length = input_text_length - 1
                input_text_temp = input_text_temp[0:input_text_length]
            else:
                input_text_temp = ''
            self.text_input.text = input_text_temp + input_text[cursor_idx:]
            self.text_input.cursor = (cursor_idx - 1, self.text_input.cursor_row)

            # self.text_input.do_backspace(from_undo=False, mode='bkspc') # works only when readonly = False
        else:
            if btn_name == 'btn_res':
                # result
                if len(self.text_input.text) == 0:
                    # no expression
                    self.text_input.focus = True
                    pass
                else:
                    exp = self.text_input.text.replace(chr(247), '/')
                    exp = exp.replace(chr(215), '*')
                    # evaluate expression
                    exp_list = re.findall(r'[0-9\.]+|[^0-9\.]+', exp)
                    final_exp = ""
                    for i in range(len(exp_list)):
                        item = exp_list[i]
                        if '/' not in item and '*' not in item and '+' not in item and \
                                '-' not in item and '(' not in item and ')' not in item:
                            operand = "Decimal('" + item + "')"
                            final_exp = final_exp + operand
                        else:
                            operator = item
                            final_exp = final_exp + operator
                    try:
                        self.text_input.text = str(eval(final_exp))
                    except:
                        self.text_input.text = self.text_input.text
            else:
                # insert
                if len(self.text_input.text) > 0:
                    input_text = self.text_input.text
                    cursor_idx = self.text_input.cursor_col
                    if cursor_idx == len(input_text):
                        # insert at the end
                        if input_text[len(input_text) - 1] == chr(247) or input_text[len(input_text) - 1] == chr(215) or \
                                input_text[len(input_text) - 1] == '+' or input_text[len(input_text) - 1] == '-':
                            # any operator at the end of the expression
                            if btn_text == chr(247) or btn_text == chr(215) or \
                                    btn_text == '+' or btn_text == '-':
                                # operator button is pressed
                                pass
                            else:
                                self.text_input.text += btn_text
                        else:
                            if btn_name == 'btn_pt':
                                # point button is pressed
                                input_text_list = re.findall(r'[0-9\.]+|[^0-9\.]+', input_text)
                                if '.' in input_text_list[len(input_text_list) - 1]:
                                    # operand is a float
                                    pass
                                else:
                                    self.text_input.text += btn_text
                            else:
                                self.text_input.text += btn_text
                    elif 0 < cursor_idx < len(input_text):
                        # insert at the middle
                        input_text_temp = input_text[0:cursor_idx]
                        if btn_name == 'btn_pt':
                            # point button is pressed
                            input_text_list = re.findall(r'[0-9\.]+|[^0-9\.]+', input_text_temp)
                            if '.' in input_text_list[len(input_text_list) - 1]:
                                # operand is a float
                                pass
                            else:
                                input_text_temp += btn_text
                        else:
                            input_text_temp += btn_text
                        self.text_input.text = input_text_temp + input_text[cursor_idx:]
                        self.text_input.cursor = (cursor_idx + 1, self.text_input.cursor_row)
                    else:
                        # insert at the beginning
                        input_text_temp = ''
                        if btn_name == 'btn_div' or btn_name == 'btn_mul' or btn_name == 'btn_add':
                            # division, multiplication or addition button is pressed
                            pass
                        elif btn_name == 'btn_sub':
                            # subtraction button is pressed
                            if input_text[0] == '-':
                                # if already present
                                pass
                            else:
                                input_text_temp += btn_text
                                self.text_input.text = input_text_temp + input_text
                                self.text_input.cursor = (cursor_idx + 1, self.text_input.cursor_row)
                        elif btn_name == 'btn_pt':
                            # point button is pressed
                            input_text_list = re.findall(r'[0-9\.]+|[^0-9\.]+', input_text)
                            if '.' in input_text_list[0]:
                                # operand is a float
                                pass
                            else:
                                input_text_temp += btn_text
                                self.text_input.text = input_text_temp + input_text
                                self.text_input.cursor = (cursor_idx + 1, self.text_input.cursor_row)
                        else:
                            input_text_temp += btn_text
                            self.text_input.text = input_text_temp + input_text
                            self.text_input.cursor = (cursor_idx + 1, self.text_input.cursor_row)
                else:
                    # fresh insertion
                    if btn_name == 'btn_div' or btn_name == 'btn_mul' or btn_name == 'btn_add':
                        # division, multiplication or addition button is pressed
                        pass
                    elif btn_name == 'btn_sub':
                        # subtraction button is pressed
                        self.text_input.text = btn_text
                    elif btn_name == 'btn_pt':
                        # point button is pressed
                        self.text_input.text = '.'
                    else:
                        self.text_input.text = btn_text

    def release_btn(self):
        self.text_input.focus = True


class Calculator(App):
    def build(self):
        return MyRoot()


calc = Calculator()
calc.run()
