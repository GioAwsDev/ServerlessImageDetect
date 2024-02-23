# ServerlessImageDetect

In this project, I will be implementing an Image Detection Event Driven architecture based around S3, DynamoDB, Lambda and Amazon Rekognition. 

Upon uploading an image of a vehicle to S3, the image will be analyzed and the vehicle license plate number will be detected and put into a DynamoDB table. 

In effect, we are simulating how toll roads would capture a license plate number.