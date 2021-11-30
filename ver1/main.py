import cnn_crawler
import Preprocessor
import scoring

if __name__ == '__main__':
    exec(open("cnn_crawler.py").read())
    exec(open("Preprocessor.py").read())
    exec(open("scoring.py").read())

    print("All process is done")
