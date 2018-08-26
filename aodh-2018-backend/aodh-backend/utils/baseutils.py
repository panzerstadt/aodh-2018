import json, os, random


db_file = "./db/db.json"


# ---------
# BAD HACKS
# ---------
# todo: holy shit this is some real crappy hack
def get_filepath(filepath_with_extension, debug=False):
    test = filepath_with_extension[0]
    if not test == '/':
        filepath_with_extension = '/' + filepath_with_extension
    if test == '.':
        filepath_with_extension = filepath_with_extension[2:]
    if debug: print('starting filepath', filepath_with_extension)

    try:
        with open(filepath_with_extension): pass
        return filepath_with_extension
    except FileNotFoundError:
        try:
            fp0 = '.' + filepath_with_extension
            if debug: print('fp0', fp0)
            with open(fp0): pass
            return fp0
        except FileNotFoundError:
            try:
                fp1 = '..' + filepath_with_extension
                if debug: print('fp1', fp1)
                with open(fp1): pass
                return fp1
            except FileNotFoundError:
                try:
                    fp2 = '../..' + filepath_with_extension
                    if debug: print('fp2', fp2)
                    with open(fp2): pass
                    return fp2
                except FileNotFoundError:
                    try:
                        fp3 = '../../..' + filepath_with_extension
                        if debug: print('fp3', fp3)
                        with open(fp3): pass
                        return fp3
                    except:
                        print('current workingdir: ', os.getcwd())
                        raise SystemError("file not found by traversing backwards 3 folders")


def get_directory(directory, debug=False):
    d = lambda x: os.path.isdir(x)
    if debug: print(directory)
    if d(directory):
        return directory
    else:
        dir0 = '.' + directory
        if d(dir0):
            print('returning: ', dir0)
            return dir0
        else:
            dir1 = '..' + directory
            if d(dir1):
                print('returning: ', dir1)
                return dir1
            else:
                dir2 = '../..' + directory
                if d(dir2):
                    print('returning: ', dir2)
                    return dir2
                else:
                    dir3 = '../../..' + directory
                    if d(dir3):
                        print('returning: ', dir3)
                        return dir3
                    else:
                        raise SystemError("directory not found by traversing 3 folders backwards")


def print_list_of_dicts(input_list):
    [print(json.dumps(c, indent=4, ensure_ascii=False)) for c in input_list]


def unhashtagify(text):
    # unhashtagify
    if '#' in text[0]:
        text = text[1:]
        return text
    return text


# remap to range
def remap(x, inMin, inMax, outMin, outMax):

    # range check
    if inMin == inMax:
        print("Warning: Zero input range")
        return None

    if outMin == outMax:
        print("Warning: Zero output range")
        return None

    # check reversed input range
    reverseInput = False
    oldMin = min(inMin, inMax)
    oldMax = max(inMin, inMax)
    if not oldMin == inMin:
        reverseInput = True

    # check reversed output range
    reverseOutput = False
    newMin = min(outMin, outMax)
    newMax = max(outMin, outMax)
    if not newMin == outMin:
        reverseOutput = True

    portion = (x - oldMin) * (newMax - newMin) / (oldMax - oldMin)
    if reverseInput:
        portion = (oldMax - x) * (newMax - newMin) / (oldMax - oldMin)

    result = portion + newMin
    if reverseOutput:
        result = newMax - portion

    return result


def bullshitify(output_dict, max_range=0.05):
    """
    bullshitifies the coordinates of the output if they are similar
    :param output_json:
    :return:
    """
    unique_dict = {
        "lat": [],
        "lng": []
    }
    for tw in output_dict:
        print(tw)
        u_lat = unique_dict['lat']
        u_lng = unique_dict['lng']

        if not tw['lat'] in u_lat:
            u_lat.append(tw['lat'])
        else:
            print('{} -> '.format(tw['lat']), end='')
            tw['lat'] = tw['lat'] + random.uniform(-max_range, max_range)
            print('{}'.format(tw['lat']))
        if not tw['lng'] in u_lng:
            u_lng.append(tw['lng'])
        else:
            tw['lng'] = tw['lng'] + random.uniform(-max_range, max_range)

    return output_dict


if __name__ == '__main__':
    t = [1,2,3,4,5]
    print(t)

    if 6 in t:
        print('yay')

