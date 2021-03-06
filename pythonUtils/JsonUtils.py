# this function can saves some datas retrieving from a list of objects give as input in a json file, nad reading datas from json file as well
# what it saves are :
#   - name of the nodes
#   - name of the first parent (father)
#   - name of the first child
#   - attributes of position like : position in the world, rotation and scale

import pymel.core as pm
import json


class JsonUtils:

    def __init__(self, nameObj, nameDataJson, filePath, fileName):
        self.nameObj = nameObj
        self.nameDataJson = nameDataJson
        self.filePath = filePath
        self.fileName = fileName

    def saveDataOnJson(self, list):
        moduleName = self.nameDataJson

        fatherStr = ''
        childStr = ''
        locPos = []
        locRot = []
        locScl = []
        locPosX = 0
        locPosY = 0
        locPosZ = 0
        locRotX = 0
        locRotY = 0
        locRotZ = 0
        locSclX = 0
        locSclY = 0
        locSclZ = 0

        moduleData = {}
        moduleData[moduleName] = []

        for i in list:
            father = pm.listRelatives(i, p=True)
            child = pm.listRelatives(i, c=True)
            locPos = pm.xform(i, q=True, ws=True, t=True)
            locRot = pm.xform(i, q=True, ws=True, rt=True)
            locScl = pm.xform(i, q=True, ws=True, s=True)

            if father == []:
                fatherStr = 'self'
            else:
                fatherStr = father[0].name()
            if len(child) == 1:
                childStr = 'self'
            else:
                childStr = child[1].name()

            locPosX = locPos[0]
            locPosY = locPos[1]
            locPosZ = locPos[2]
            locRotX = locRot[0]
            locRotY = locRot[1]
            locRotZ = locRot[2]
            locSclX = locScl[0]
            locSclY = locScl[1]
            locSclZ = locScl[2]

            moduleData[moduleName].append({
                'nodeName': i.name(),
                'nodeFather': fatherStr,
                'nodeChild': childStr,
                'nodePosX': locPosX,
                'nodePosY': locPosY,
                'nodePosZ': locPosZ,
                'nodeRotX': locRotX,
                'nodeRotY': locRotY,
                'nodeRotZ': locRotZ,
                'nodeSclX': locSclX,
                'nodeSclY': locSclY,
                'nodeSclZ': locSclZ,
            })

            print ('\nnode : ' + str(i) + '\nfather : ' + fatherStr + '\nchild : ' + childStr)
            print ('position X :' + str(locPosX))
            print ('position Y :' + str(locPosY))
            print ('position Z :' + str(locPosZ))
            print ('rotation X :' + str(locRotX))
            print ('rotation Y :' + str(locRotY))
            print ('rotation Z :' + str(locRotZ))
            print ('scale X :' + str(locSclX))
            print ('scale Y :' + str(locSclY))
            print ('scale Z :' + str(locSclZ))

        if self.filePath[len(self.filePath) - 1] == '\\':
            with open(self.filePath + self.fileName + '.json', 'w') as outfile:
                json.dump(moduleData, outfile)
        else:
            with open(self.filePath + '\\' + self.fileName + '.json', 'w') as outfile:
                json.dump(moduleData, outfile)

    def readingDataFromJson(self):
        if self.filePath[len(self.filePath) - 1] != '\\':
            self.filePath = self.filePath + '\\'

        with open(self.filePath + self.fileName + '.json') as json_file:
            readData = json.load(json_file)

        return readData

    def getJsonName(self):
        return self.nameDataJson

    def getFullFilePath(self):
        return self.nameDataJson + self.fileName + '.json'

    def getFileName(self):
        return self.fileName