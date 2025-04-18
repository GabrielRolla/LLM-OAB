from PyPDF2 import PdfReader
from testParserFunctions import pdfTextExtractor, buildQuestionAndCommentDictionaryArray
from lawsExtractionFunctions import processOabQuestions, createLegalPrincipalsColumn
import pandas as pd

OAB38 = "../rawTests/OAB-38-resolution.pdf"
OAB39 = "../rawTests/OAB-39-resolution.pdf"
OAB40 = "../rawTests/OAB-40-resolution.pdf"
OAB41 = "../rawTests/OAB-41-resolution.pdf"

oabTests = [OAB38, OAB39, OAB40, OAB41]

for testPath in oabTests:
    filePath = testPath
    pdf = PdfReader(filePath)
    oabNumber = filePath.split('/')[2].split('-')[1]

    pdfTextExtractor(pdf, f"extractedText/oab{oabNumber}extractedText.txt")
    questionAndAnswerList = buildQuestionAndCommentDictionaryArray(f"extractedText/oab{oabNumber}extractedText.txt")

    questionsList = []
    commentList = []
    legalPrinciples = []
    for questionAndAnswer in questionAndAnswerList:
        questionsList.append(questionAndAnswer["question"])
        commentList.append(questionAndAnswer['comment'])
        legalPrinciples.append('Não preenchido')


    df = pd.DataFrame({"question":questionsList, "comment":commentList, "legalPrinciples": legalPrinciples})
    df.to_csv(f'../parsedTests/OAB-{oabNumber}.csv', index=False)
    df.to_excel(f'../parsedTests/OAB-{oabNumber}.xlsx', index=False, engine="openpyxl")

OAB38CSV = "../parsedTests/OAB-38.csv"
OAB39CSV = "../parsedTests/OAB-39.csv"
OAB40CSV = "../parsedTests/OAB-40.csv"
OAB41CSV = "../parsedTests/OAB-41.csv"

oabCsvPathList = [OAB38CSV, OAB39CSV, OAB40CSV, OAB41CSV]

for oabCsvPath in oabCsvPathList:
    oabCsv = pd.read_csv(oabCsvPath)
    newCsvName =   oabCsvPath.split('/')[2].split('.')[0]
    
    allExtractedLawsResponse = processOabQuestions(oabCsv, 'gemini-2.0-flash')
    oabCsvLegalPrincipals = createLegalPrincipalsColumn(oabCsv, allExtractedLawsResponse)
    oabCsvLegalPrincipals.to_csv(f'../parsedTests/{newCsvName}.csv', index=False)
    oabCsvLegalPrincipals.to_excel(f'../parsedTests/{newCsvName}.xlsx', index=False, engine="openpyxl")
    print(f'Csv {newCsvName} Gerado')

##Gabaritos
OAB38ANSWERS = ['B', 'D', 'B', 'C', 'D', 'B', 'A', 'C', 'A', 'A', 'A', 'D', 'C', 'A', 'C', 'C', 'C', 'C', 'D', 'B', 'A', 'B', 'B', 'D', 'A', 'D', 'C', 'C', 'D', 'D', 'A', 'D', 'D', 'A', 'C', 'D', 'B', 'A', 'D', 'A', 'C', 'D', 'C', 'C', 'A', 'B', 'A', 'A', 'D', 'B', 'D', 'D', 'B', 'A', 'B', 'C', 'D', 'B', 'B', 'A', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 'A', 'B', 'A', 'B', 'B', 'B', 'D', 'D', 'C', 'A', 'D', 'C', 'A']
OAB39ANSWERS = ['C', 'A', 'D', 'D', 'A', 'A', 'D', 'B', 'D', 'D', 'B', 'C', 'B', 'A', 'C', 'A', 'C', 'B', 'C', 'A', 'B', 'A', 'A', 'C', 'C', 'C', 'D', 'A', 'D', 'A', 'D', 'A', 'D', 'C', 'C', 'B', 'D', 'B', 'D', 'C', 'D', 'C', 'B', 'B', 'C', 'B', 'A', 'A', 'B', 'D', 'D', 'B', 'D', 'C', 'D', 'D', 'A', 'A', 'B', 'B', 'B', 'D', 'C', 'C', 'C', 'D', 'A', 'A', 'B', 'C', 'B', 'D', 'B', 'B', 'A', 'C', 'C', 'B', 'A', 'A']
OAB40ANSWERS = ['C', 'A', 'C', 'C', 'A', 'B', 'A', 'D', 'C', 'B', 'D', 'B', 'B', 'B', 'B', 'D', 'B', 'A', 'A', 'D', 'D', 'B', 'C', 'A', 'B', 'D', 'A', 'C', 'D', 'B', 'D', 'D', 'C', 'D', 'C', 'A', 'A', 'B', 'C', 'C', 'B', 'C', 'D', 'C', 'D', 'C', 'C', 'A', 'A', 'B', 'C', 'A', 'D', 'B', 'B', 'D', 'A', 'D', 'A', 'A', 'B', 'D', 'A', 'B', 'B', 'A', 'C', 'C', 'A', 'C', 'A', 'C', 'D', 'B', 'D', 'A', 'D', 'C', 'C', 'B']
OAB41ANSWERS = ['B', 'B', 'D', 'C', 'C', 'A', 'B', 'A', 'B', 'B', 'B', 'B', 'A', 'B', 'C', 'B', 'B', 'A', 'C', 'B', 'B', 'A', 'C', 'A', 'D', 'C', 'B', 'D', 'C', 'A', 'D', 'C', 'C', 'D', 'D', 'C', 'A', 'D', 'D', 'D', 'B', 'D', 'B', 'A', 'A', 'A', 'D', 'A', 'B', 'C', 'C', 'A', 'D', 'D', 'B', 'B', 'A', 'D', 'C', 'D', 'C', 'D', 'C', 'C', 'A', 'A', 'C', 'A', 'A', 'D', 'D', 'C', 'B', 'A', 'C', 'A', 'C', 'D', 'B', 'A']

##Questões anuladas
OAB38CANCELEDQUESTIONS = [False] * 80; OAB38CANCELEDQUESTIONS[45] = True; OAB38CANCELEDQUESTIONS[56] = True; OAB38CANCELEDQUESTIONS[58] = True; 
OAB39CANCELEDQUESTIONS = [False] * 80; OAB39CANCELEDQUESTIONS[16] = True; OAB39CANCELEDQUESTIONS[49] = True; OAB39CANCELEDQUESTIONS[63] = True; 
OAB40CANCELEDQUESTIONS = [False] * 80; OAB40CANCELEDQUESTIONS[1] = True
OAB41CANCELEDQUESTIONS = [False] * 80; 

answersList = [ OAB38ANSWERS, OAB39ANSWERS, OAB40ANSWERS, OAB41ANSWERS ]
canceledQuestionsList = [OAB38CANCELEDQUESTIONS, OAB39CANCELEDQUESTIONS, OAB40CANCELEDQUESTIONS, OAB41CANCELEDQUESTIONS]

for index, oabCsvPath in enumerate(oabCsvPathList):
    csvName = oabCsvPath.split('/')[2].split('.')[0]
    oabCsv = pd.read_csv(oabCsvPath)
    oabCsv['answers'] = answersList[index]
    oabCsv['canceledQuestion?'] = canceledQuestionsList[index]
    oabCsv.to_csv(f'../parsedTests/{csvName}.csv', index=False)
    oabCsv.to_excel(f'../parsedTests/{csvName}.xlsx', index=False, engine="openpyxl")

