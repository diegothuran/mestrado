import cv2
import numpy as np
import math



def binaryImage(image):

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #ret2,th2 = cv2.threshold(gray_image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        ret2,th2 = cv2.threshold(gray_image,1,200,cv2.THRESH_BINARY)

        median = cv2.medianBlur(th2,5)

        #element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
        #temp = cv2.dilate(th2,element)

        return  th2


def createWhiteImage(image):
        for x in range(len(image)):
            for y in range(len(image[x])):
                image[x][y] = 0
        return image


def extractFeatureVector(points):
        features = []

        for i in range(len(points) -1 ):
            if(i == 0):
                features.append(distanceCalculator(points[0],points[len(points) -2],points[1]))
            elif (i == len(points) - 2):
                features.append(distanceCalculator(points[len(points) -2],points[len(points) -3], points[0]))
            else:
                features.append(distanceCalculator(points[i],points[i -1], points[i + 1]))

        return features


def distanceCalculator( farPoint, point1, point2):

        term1 = math.pow( (point1[1] - point2[1]) ,2)
        term2 = math.pow( (point1[0] - point2[0]) ,2)
        vi = math.pow( (term1 + term2) ,0.5)
        ui = farPoint[0]*(point1[1] - point2[1]) + farPoint[1]*(point1[0] - point2[0]) +  point2[1]*point2[0] - point1[1]*point1[0]

        return ui / vi

def calculateAngle( point1, point2, point3, point4, biggestX, biggestY):

        angle =  math.atan2(point2[1] - point1[1], point2[0]/biggestX-point1[0]) - math.atan2(point4[1] - point3[1], point4[0]-point3[0])

        return math.atan2(math.sin(angle), math.cos(angle))


def amplitudeNormalization(features):

        features.sort()
        newFeatures = []

        bigger = 0
        for feature in features:
            if(feature > bigger):
                bigger = feature

        for feature in features:
            newFeatures.append(feature/bigger)


        return newFeatures


def lenghtNormalization(features, lenght):

        normalizedFeatures = []
        if(len(features) < lenght):
            normalizedFeatures = features
            while(len(normalizedFeatures) < lenght):
                normalizedFeatures.append(0)

        else:
            runner = (len(features) / lenght) + 1
            i = 0
            positionsToBeInserted = []
            while(i < len(features)):
                positionsToBeInserted.append(i)
                i += runner

            while(len(positionsToBeInserted) != lenght):
                i = random.randint(len(features))
                haveItem = False
                for h in positionsToBeInserted:
                    if(h == i):
                        haveItem = True

                if(not haveItem):
                    positionsToBeInserted.append(i)

            positionsToBeInserted.sort()
            for x in positionsToBeInserted:
                normalizedFeatures.append(features[x])

        return normalizedFeatures

def doConvexityApproach(img, img2, lenght,directory):

    #thresh = binaryImage(img)
    img2 = createWhiteImage(img2)

    contours,hierarchy = cv2.findContours(img,cv2.CHAIN_APPROX_NONE,cv2.RETR_LIST)
    cnt = contours[0]

    for i in range(len(contours)):
        if(cv2.contourArea(cnt) < cv2.contourArea(contours[i])):
           cnt = contours[i]

    hull = cv2.convexHull(cnt, clockwise=True, returnPoints = False)

    storage = cv2.cv.CreateMemStorage(0)

    defects = cv2.convexityDefects(cnt,hull)

    biggestX = 0
    biggestY =  0
    points = []
    centerPoints = []
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        points.append(start)
        points.append(far)
        points.append(end)
        centerPoints.append(far)
        #cv2.circle(img2,far,1,[255,255,255],-1)
        #cv2.circle(img2,start,1,[255,255,255],-1)
        #cv2.circle(img2,end,1,[255,255,255],-1)
        if(start[0] >= biggestX):
           biggestX = start[0]
        if(end[0] >= biggestX):
           biggestX = end[0]
        if(far[0] >= biggestX):
           biggestX = far[0]

        if(start[1] >= biggestY):
           biggestY = start[1]
        if(end[1] >= biggestY):
           biggestY = end[1]
        if(far[1] >= biggestY):
           biggestY = far[1]



    lista = []
    lista.append(centerPoints)

    momentPoints2 = np.array(lista)

    moments = cv2.moments(momentPoints2)
    #x = moments['m10'] / moments['m00']
    #y = moments['m01'] / moments['m00']
    #central = tuple( [int(x),int(y)])
    #cv2.circle(img2,central,1,[255,255,255],-1)

    finalAngle = 0

    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])

    points = extractFeatureVector(points)


    #points = amplitudeNormalization(points)
    #points = lenghtNormalization(points,lenght)

    #points.append(finalAngle)

    return points

   # -*- coding: utf-8 -*-
