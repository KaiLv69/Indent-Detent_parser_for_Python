def pre_process_code(raw_text):
    space4 = "    "
    text = raw_text.replace("\t", space4)
    stack = [0]  # count indents
    list = text.split('\n')
    for idx in range(len(list)):
        l1 = len(list[idx])
        list[idx] = str.lstrip(list[idx])
        indent = (l1 - len(list[idx])) // 4
        rem = l1 - len(list[idx]) - indent * 4
        indent_t = indent

        if indent_t > stack[-1]:
            while indent_t > stack[-1]:
                list[idx] = "INDENT " + list[idx]
                indent_t = indent_t - 1
            stack.append(indent)
        elif indent_t < stack[-1]:
            while indent_t < stack[-1]:
                list[idx] = 'DEDENT' + list[idx]
                indent_t = indent_t + 1
            while indent < stack[-1]:
                stack.pop()

        list[idx] = " " * rem + list[idx]

    text = "NEW_LINE".join(list)
    return text


def post_process_code(code):
    # replace recreate lines with \n and appropriate indent / dedent
    # removing indent/ dedent tokens
    assert isinstance(code, str) or isinstance(code, list)
    if isinstance(code, list):
        code = " ".join(code)
    lines = code.split("NEW_LINE")
    tabs = ""
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("INDENT "):
            number_indent = line.count("INDENT ")
            tabs += "    " * number_indent
            line = line.replace("INDENT " * number_indent, tabs)
        elif line.startswith("DEDENT"):
            number_dedent = line.count("DEDENT")
            tabs = tabs[4 * number_dedent:]
            line = line.replace("DEDENT", "")
            line = line.strip()
            line = tabs + line
        elif line == "DEDENT":
            line = ""
        else:
            line = tabs + line
        lines[i] = line
    untok_s = "\n".join(lines)
    return untok_s


if __name__ == '__main__':
    code = '''import torch


class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.basic_layer_1 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels=1, out_channels=64, kernel_size=4, stride=2, padding=0),
            torch.nn.BatchNorm2d(num_features=64),
            torch.nn.Tanh()
        )

        self.basic_layer_2 = torch.nn.Sequential(
            torch.nn.Conv2d(
                in_channels=64,
                out_channels=128, 
                kernel_size=4, 
                stride=2, 
                padding=0
            ),
            torch.nn.BatchNorm2d(num_features=128),
            torch.nn.Tanh()
        )

        self.basic_layer_3 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels=128, out_channels=3, kernel_size=4, stride=2, padding=0),
            torch.nn.BatchNorm2d(num_features=3),
            torch.nn.Tanh()
        )

        self.linear_layer = torch.nn.Linear(in_features=2700, out_features=10)

    def forward(self, x):
        x = self.basic_layer_1(x)
        x = self.basic_layer_2(x)
        x = self.basic_layer_3(x)
        x = x.view(-1, 2700)
        x = self.linear_layer(x)

        return x'''
    c = pre_process_code(code)
    print(c)
    print(post_process_code(c))
