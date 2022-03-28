import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
from dataset_creation import *
from model import *

def getset2labels():
    with open('Set2Labels.txt', 'r') as file:
        # Return the array wih the labels split into different elements
        lines = [line.rstrip() for line in file]
        return lines

# main functions
def main():
    iCount = 0
    # if object is on screen
    bObjectAppear = False

    # console args parser
    oParser = ArgumentParser(description="Group 3 Kinect Coursework")
    oParser.add_argument("videofolder", help="Folder containing test Kinect video. Folder must contain INDEX.txt.",
                         default="Set2", nargs="?")
    oParser.add_argument("--no-realtime", action="store_true", default=True)
    oArgs = oParser.parse_args()
    data_type = str(oArgs.videofolder)
    # Print on console
    print("CHECK || main() || Arguments: " + str(oArgs))


    # variables for preds, true labels and getting set2 labels
    preds = []
    iCount = 0
    set2_labels = getset2labels()
    true = []

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
    threshold_win_name = "Thresholded Depth"
    cv2.namedWindow(threshold_win_name)
    cv2.createTrackbar("Threshold", threshold_win_name, iThreshold, 85, on_threshold_change)
    print(set2_labels)

    # if train is true, then train the model otherwise pass

    # Attach Trackbar to Thresholded Depth Window
    sThresholdWindowName = "Thresholded Depth"
    cv2.namedWindow(sThresholdWindowName)
    cv2.createTrackbar("Threshold", sThresholdWindowName,
                       iThreshold, 100, on_threshold_change)


    for oStatus, oRGB, oDepth in FreenectPlaybackWrapper(oArgs.videofolder, not oArgs.no_realtime):
        # If we have an updated Depth image, then start processing
        if oStatus.updated_depth:
            # Threshold the image
            _, oThresholdDepth = cv2.threshold(
                oDepth, iThreshold, 255, cv2.THRESH_BINARY)

            # Get set of arPoints where value in thresholded image is equal to 0
            # arPoints in format (iY, iX)
            arPoints = numpy.argwhere(oThresholdDepth == 0)
            if len(arPoints) > 500 and not len(arPoints) == 0:
                oBoundaryBox = cv2.boundingRect(arPoints)
                bObjectAppear = True
                try:

                    # resize the image
                    resize = cv2.resize(oThresholdDepth, (180, 180))
                    # add the 3 channels to pass to the model
                    resize = cv2.merge((resize, resize, resize))

                    # turn the image into an array
                    img_array = tf.keras.utils.img_to_array(resize)
                    img_array = tf.expand_dims(img_array, 0)  # Create a batch

                    # make a prediction on the array of the image using softmax
                    predictions = model.predict(img_array)
                    score = tf.nn.softmax(predictions[0])
                    f_score = 100 * np.max(score)  # convert the result into percentage
                    cLabel = set2_labels[iCount]

                    # score threshold to eliminate random display of output
                    if f_score < 80:
                        label_on_screen = "Not sure"
                    else:
                        label_on_screen = f_score

                    # building truelables and predictions
                    true.append(cLabel)
                    preds.append(class_names[np.argmax(score)])

                    # displaying text on depth window
                    cv2.putText(oDepth,
                                f'True: {iCount} | Predicted: {class_names[np.argmax(score)]} | Confidence: {label_on_screen}',
                                (0, 0 + 20),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6, (0, 255, 255), 2)
                except Exception as e:
                    print(e)
            else:
                # Only increment the counter if the previous frame contain an object
                if bObjectAppear:
                    iCount += 1
                    bObjectAppear = False
            cv2.imshow("Depth", oDepth)
            cv2.imshow(sThresholdWindowName, oThresholdDepth)
        # If we have an updated RGB image, then display
        if oStatus.updated_rgb:
            # If we have a current bounding box, then draw that on the RGB image with offset
            cv2.imshow("RGB", oRGB)

        # Check for Keyboard input.
        iKey = cv2.waitKey(5)

        # Break out of the program if ESC is pressed (OpenCV KeyCode 27 is ESC key)
        if iKey == 27:
            break
    cv2.destroyAllWindows()

    # classification report using sklearn metrics
    class_report = classification_report(true, preds)
    print(class_report)

    # confusion matrix using heatmap from seaborn
    cf_matrix = confusion_matrix(true, preds)
    sns.heatmap(cf_matrix, annot=True, fmt=".0f")

    # show the matrix
    plt.show()


if __name__ == '__main__':
    main()