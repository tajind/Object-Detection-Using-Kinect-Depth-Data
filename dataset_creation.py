from argparse import ArgumentParser

from FreenectPlaybackWrapper.PlaybackWrapper import FreenectPlaybackWrapper
import cv2
import numpy
import pandas as pd
import os


# used to get the Set1 Labels from the text file
def RetrieveTrainingLabels():
    # Open file
    with open('Set1Labels.txt', 'r') as file:
        # Return the array wih the labels split into different elements
        lines = [line.rstrip() for line in file]
        return lines

# used to get the Set2 Labels from the text file
def getset2labels():
    with open('Set2Labels.txt', 'r') as file:
        # Return the array wih the labels split into different elements
        lines = [line.rstrip() for line in file]
        return lines

# Main functions
def main():
    iCount = 0 # the index of the object on screen

    # if object is on screen
    bObjectAppear = False

    # console args parser
    oParser = ArgumentParser(description="Group 3 Kinect Coursework")
    oParser.add_argument("videofolder", help="Folder containing Kinect video. Folder must contain INDEX.txt.",
                         default="Set1", nargs="?")
    oParser.add_argument("--no-realtime", action="store_true", default=True)
    oArgs = oParser.parse_args()
    data_type = str(oArgs.videofolder)
    # Print on console
    print("CHECK || main() || Arguments: " + str(oArgs))

    # Invoke function
    arTrainingLabels = RetrieveTrainingLabels()
    # Invoke function
    labels = ", ".join(arTrainingLabels)
    print(labels, "\n", len(labels))

    # create the dirs with labels names if they dont exist
    for i in arTrainingLabels:
        if not os.path.exists(f"dataset/{data_type}/{i}"):
            os.makedirs(f'dataset/{data_type}/{i}')

    # Default parameters for threshold/offsets
    iThreshold = 77
    iOffsetX = -40
    iOffsetY = 20

    def on_threshold_change(iValue):
        """
        Handler to change iThreshold value

        :param iValue: Value to set the iThreshold to
        """
        nonlocal iThreshold

        iThreshold = iValue

    # Attach Trackbar to Thresholded Depth Window
    sThresholdWindowName = "Thresholded Depth"
    cv2.namedWindow(sThresholdWindowName)
    cv2.createTrackbar("Threshold", sThresholdWindowName,
                       iThreshold, 100, on_threshold_change)

    oBoundaryBox = None

    counter = 0

    print("Starting to train!")
    for oStatus, oRGB, oDepth in FreenectPlaybackWrapper(oArgs.videofolder, not oArgs.no_realtime):
        # If we have an updated Depth image, then start processing
        if oStatus.updated_depth:
            # Threshold the image
            _, oThresholdDepth = cv2.threshold(
                oDepth, iThreshold, 255, cv2.THRESH_BINARY)

            # Get set of arPoints where value in thresholded image is equal to 0
            # arPoints in format (iY, iX)
            arPoints = numpy.argwhere(oThresholdDepth == 0)

            # custom depth values for each object
            if iCount == 0 or iCount == 2:
                on_threshold_change(78)
            if iCount == 1:
                on_threshold_change(75)
            if iCount == 3 or iCount == 4:
                on_threshold_change(73)
            if iCount == 5:
                on_threshold_change(74)
            if iCount == 6 or iCount == 7 or iCount == 8:
                on_threshold_change(80)
            if iCount == 9:
                on_threshold_change(76)
            if iCount == 10:
                on_threshold_change(75)
            if iCount == 11:
                on_threshold_change(73)
            if iCount == 12:
                on_threshold_change(77)
            if iCount == 13:
                on_threshold_change(71)

            # If an object appears
            if len(arPoints) > 1000 and not len(arPoints) == 0:
                # Set boolean variable to true
                bObjectAppear = True
                # Calculate Bounding Box around arPoints
                oBoundaryBox = cv2.boundingRect(arPoints)

                # Extract out bounding box components
                (iY, iX, iHeight, iWidth) = oBoundaryBox
                iX = iX + iOffsetX
                iY = iY + iOffsetY
                try:
                    # drawing a rectangle on the threadholddepth window
                    # cv2.rectangle(oThresholdDepth, [int(iX / 2), int(iY / 2)], [int(iX + 224), int(iY + 224)],
                    #               (0, 0, 255))
                    if len(arPoints) > 2000:
                        # if there are more than 2000 arpoints on screen, start saving the frame as images
                        cv2.imwrite(f"dataset/{data_type}/{arTrainingLabels[iCount]}/{counter}.jpg",
                                    oThresholdDepth)

                except Exception as e:
                    print(e)

                counter += 1

            else:
                oBoundaryBox = None
                # Only increment the counter if the previous frame contain an object
                if bObjectAppear:
                    iCount += 1
                    bObjectAppear = False

            # Show oDepth/thresholded oDepth images
            cv2.imshow("Depth", oThresholdDepth)
            cv2.imshow(sThresholdWindowName, oThresholdDepth)

        # If we have an updated RGB image, then display
        if oStatus.updated_rgb:
            # If we have a current bounding box, then draw that on the RGB image with offset
            if oBoundaryBox is not None:
                # Extract out bounding box components
                (iY, iX, iHeight, iWidth) = oBoundaryBox

                # Add iX/iY offsets for oRGB image
                iX = iX + iOffsetX
                iY = iY + iOffsetY

                # Draw bounding box on RGB image
                rect = cv2.rectangle(oRGB, [int(iX / 2), int(iY / 2)], [
                    int(iX + iWidth), int(iY + iHeight)], (0, 255, 255))
                try:
                    cv2.putText(oRGB,
                                f'Label: {arTrainingLabels[iCount]} | iCount: {iCount} | PointLen: {len(arPoints)} | Depth: {iThreshold}',
                                (0, 0 + 20),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6, (0, 255, 255), 2)
                except Exception as e:
                    print(e)
            # Show RGB image
            cv2.imshow("RGB", oRGB)

        # Check for Keyboard input.
        iKey = cv2.waitKey(5)

        # Break out of the program if ESC is pressed (OpenCV KeyCode 27 is ESC key)
        if iKey == 27:
            break

if __name__ == "__main__":
    exit(main())
