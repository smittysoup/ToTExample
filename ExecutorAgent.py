'''
1.  The agent recieves a spec from the designer.  
2. The agent should decide what type of code needs to be written.  
3. The agent should write the code.
4. Depending on what type of code was chosen, run code through a validator and a linter.
5. Start with only HTML.  The agent should write HTML code.
6.  Along with the code the agent should use puppeteer to write a test for the code.
7.  the agent should write a python subprocess that runs the test.
8.  The agent should run the test.
'''

# Importing required modules and classes
import html5lib
import subprocess


def html_linter(code):
    parser = html5lib.HTMLParser(strict=True)
    return parser.parse(code)

def print_tree(element, indent=0):
    print("  " * indent + repr(element.tag))
    for child in element:
        print_tree(child, indent + 1)
    return None
        
def serialize_tree(tree):
    walker = html5lib.getTreeWalker("etree")
    serializer = html5lib.serializer.HTMLSerializer()
    return "".join(serializer.serialize(walker(tree)))

def save_code_to_file(html_code, filename='index.html'):
    try:
        with open(filename, 'w') as f:
            f.write(html_code)
        print(f'Code saved successfully to {filename}!')
    except Exception as e:
        print(f'Error occurred: {e}')
    return None
        
def read_code_from_file(filename='page1.html'):
    try:
        with open(filename, 'r') as f:
            read_code = f.read()
        print(f'Code read successfully from {filename}!')
        return read_code
    except Exception as e:
        print(f'Error occurred: {e}')
        return None
        
def check_page_with_puppeteer(page_path):
    result = subprocess.run(["node", "puppeteer_script.js", page_path], capture_output=True, text=True)
    stderr = result.stderr  # This is a string containing the error output.
    return stderr

def lint(filepath):
    code = read_code_from_file(filepath)
    dtree = html_linter(code)
    code = serialize_tree(dtree)
    save_code_to_file(code,filepath)
    return code

if __name__ == '__main__':
    # variables for testing
    code = '''
    <!DOCTYPE html>
<html>
    <head>
        <title>Webpage with Left Navigation Menu</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="A modern, minimalistic webpage with a left navigation menu optimized for mobile devices and SEO.">
        <style>
            body {
                font-family: sans-serif;
            }
            #nav {
                width: 200px;
                float: left;
            }
            #main {
                margin-left: 200px;
            }
            @media (max-width: 600px) {
                #nav {
                    width: 100%;
                    float: none;
                }
                #main {
                    margin-left: 0;
                }
            }
        </style>
    </head>
    <body>
        <div id="nav">
            <ul>
                <li><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Contact</a></li>
            </ul>
        </div>
        <div id="main">
            <h1>Welcome!</h1>
            <p>This is a modern, minimalistic webpage with a left navigation menu optimized for mobile devices and SEO.</p>
        </div>
    </body>
</html>
'''
    dtree = html_linter(code)
    print(serialize_tree(dtree))

