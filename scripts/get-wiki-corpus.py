import q
import argparse
import json
import wikipedia
import codecs
@q
def main():
    #q.d()

    parser = argparse.ArgumentParser(description='Downloading wikipedia category page')
    parser.add_argument("-file", type = str, help='Path to json with pagenames')

    wikipedia.set_lang("ru")

    args = parser.parse_args()
    file = open(args.file, 'r')
    categories = json.load(file)
    textCorpus = ''
    punctuation = ['.', ',', '=', '==', '===']

    corpus = codecs.open('resources/textCorpus.txt', 'w', errors='ignore')
    for i in range(0, categories[u'*'][0][u'a'][u'*'].__len__()):
        category_name = ''
        page = ''
        try:
            category_name = categories[u'*'][0][u'a'][u'*'][i][u'title']
        except Exception:
            continue
        if category_name != '':
            try:
                page = wikipedia.page(category_name).content
            except Exception:
                continue
            if(page != ''):
                page = ' '.join([word for word in page.split() if word not in punctuation])
                page = page.replace(',', '')
                page = page.encode('utf8')
                corpus.write(page)
                print(category_name)

    corpus.close()
    return




if __name__ == "__main__":
    main()