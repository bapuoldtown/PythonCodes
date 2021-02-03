from configparser import ConfigParser

def config(filename='database.ini',section='postgresql'):
    parser=ConfigParser()
    parser.read(filename)

    if parser.has_section('postgresql'):
        print("The mentioned section is present")

        items=parser.items(section)

        for i in items:
            print(type(i))
    else:
        raise TypeError('The section is not present')

print(config())