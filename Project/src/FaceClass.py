class AnalyzedFaces:
    def __init__(self, ref, other, percentage, count ):
        self.ref = ref
        self.other = other
        self.percentage = percentage
        self.count = count
def findDetectedFace(ROI, detectedFacesArr):
    for i in range(0, len(detectedFacesArr)):
        if ROI in detectedFacesArr[i]: return detectedFacesArr[i]
def findROIInDetectedFaces(ROI, DetectedFacesArr):
    for i in range(0, len(DetectedFacesArr)):
        if ROI in DetectedFacesArr[i]: return True
    return False
def isFaceExistedInDetected(name, DetectedFacesArr):
    for i in range(0, len(DetectedFacesArr)):
        if name in DetectedFacesArr[i]: return True
    return False