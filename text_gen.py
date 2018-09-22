from textgenrnn import textgenrnn
import glob


class TextGen(object):

    def __init__(self):
        self.textgen = textgenrnn()

    def findModel(self, query):
        listFiles = glob.glob('./' + str(query) + '*.hdf5')
        if len(listFiles) is 0:
            return False
        elif len(listFiles) is 1:
            return listFiles[0]
        else:
            return listFiles

    def load(self, modelFile):
        try:
            self.textgen = textgenrnn(modelFile)
            return True
        except FileNotFoundError:
            listFiles = self.findModel(modelFile)
            if listFiles is not False:
                return listFiles
            else:
                return False
        except BaseException:
            return False

    def train(self, inputFile, epochs=None, modelFile=None):
        self.textgen.train_from_file(inputFile, num_epochs=epochs)
        if modelFile is None:
            modelFile = str(inputFile) + '.hdf5'
        self.textgen.save(modelFile)

    def generate(self, modelFile, num, temperature):
        loadResult = self.load(modelFile)
        if loadResult is True:
            self.textgen.generate(num, temperature)
        elif loadResult is False:
            return "Error retrieving the model"
        else:
            return "The following similar models were found " + str(loadResult)
