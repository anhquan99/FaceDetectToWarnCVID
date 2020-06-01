import JsonReader
from FaceClass import AnalyzedFaces
initialParams = JsonReader.loadData()

# analyze percentage of predictions by contact range
def analyzePercentByContactRange(distance, maskRef, maskOther):
    # check if mask on or off
    if maskRef == "Mask": percentRef = initialParams["mask_lower_percent"] 
    else: percentRef = 0
    if maskOther == "Mask": percentOther = initialParams["mask_lower_percent"] 
    else: percentOther = 0
    # calcualte the lower percent of mask by combine percent of ref and other
    percentArgMask = (percentRef + percentOther)/2
    # percent by contact range
    percentDis = (initialParams["contact_range"] / distance) * 100
    # if percent of contact is higher than 100% ten make it 100%
    if percentDis > 100: percentDis = 100
    # finnal calculation 
    return percentDis - percentArgMask

# analyze wrong prdiction by count percent
def analyzeWrongPrediction(AnalyzedFacesArr):
    totalCount = 0
    # calculate total count
    for i in AnalyzedFacesArr:
        totalCount += i.count
    # calculate each analyze count to clear out wrong predictions
    for i in AnalyzedFacesArr:
        # remove analyze if count percent is smaller than 
        if (i.count / totalCount) * 100 <= initialParams["wrong_count"]:
            AnalyzedFacesArr.remove(i)
    return AnalyzedFacesArr

# analyze predicted if it already exists in array
def analyzePredicted(AnalyzedFacesArr, Predicted):
    # iterate over array
    for  i in AnalyzedFacesArr:
        # if it already exists
        if (Predicted.ref == i.ref and Predicted.other == i.other) or (Predicted.ref == i.other and Predicted.other == i.ref):
            # increase count by 1
            i.count += 1
            # if new percentage > old percentage 
            if Predicted.percentage > i.percentage:
                i.percentage
            # end
            return AnalyzedFacesArr
    # if predicted not in array add to array
    AnalyzedFacesArr.append(AnalyzedFaces(Predicted.ref, 
        Predicted.other, 
        Predicted.percentage, 
        1))
    # end
    return AnalyzedFacesArr
    