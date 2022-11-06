from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid
from dotenv import load_dotenv
# Replace with valid values
load_dotenv()

prediction_endpoint = os.getenv('prediction_endpoint')
prediction_key = os.getenv('prediction_key')
prediction_resource_id = os.getenv('prediction_resource_id')
publish_iteration_name=os.getenv('publish_iteration_name')
project_id=os.getenv('project_id')


prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(prediction_endpoint, prediction_credentials)

test_images_folder_path='D:/BOB_Hackathon/Test/'

print("Testing the prediction endpoint...")
for img_num in range(1,9):
    test_image_filename = str(img_num) + ".jpg"
    with open(os.path.join(test_images_folder_path, test_image_filename),mode="rb") as image_contents:
        results = predictor.detect_image(project_id, publish_iteration_name, image_contents.read())
        # Display the results
        print(f"Testing image {test_image_filename}...")
        for prediction in results.predictions:
            print(f"\t{prediction.tag_name}: {prediction.probability*100 :.2f}%")

              