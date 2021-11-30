import newscrawl
import json_to_frame
import Preprocessor
import scoring

if __name__ == '__main__':
    try:
        exec(open("newscrawl.py").read())
        exec(open("json_to_frame.py").read())
        exec(open("Preprocessor.py").read())
        exec(open("scoring.py").read())
        print("All process is done")

    except:
        print("Error!")
