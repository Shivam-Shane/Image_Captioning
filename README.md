
# Image Caption Generator

# Descriptions
The "Image to Caption Generator" project aims to develop an AI-driven system that automatically generates descriptive captions for images. By leveraging advanced deep learning models, aws, and CICD, particularly in the fields of computer vision and natural language processing, the system interprets visual content and converts it into coherent and contextually relevant text descriptions. This project has applications in accessibility, content creation, and enhancing user experiences across various digital platforms.


## License

[GNU GENERAL PUBLIC LICENSE](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)


## Prerequisites.
1. Python. (version>3.10)
2. Machine learning.
3. NLP(Natural Language Processing).
4. Github Action (Deployment).
5. Aws Pipelines (Deployment).
6. Transformer.
7. OOPS concepts.
8. Pytorch.
9. Django.
10. Deep Learning Frameworks

# Installation Instructions
1. Create an anaconda environment. visit https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands to know how to create a conda environment.
2. Clone the Repository
3. https://github.com/Shivam-Shane/Image_Captioning.git
Note: If you encounter an issue with LFS data being exhausted while cloning, download the files manually from the Google Drive link provided below. 

https://tinyurl.com/bdhvctuj

4. Once all the files are downloaded move them to the project directory(root level) 
5. run Command pip install. (The dot is mandatory as it specifies to find setup.py in the current directory, not to mark the end of a sentence.)

6. run Command python .\IC_django\manage.py runserver 0.0.0.0:8080
You can customize the port as desired.

7. Open http://localhost:8080 in browser.
8. Input the desired image and see the result.
## Deployment

To deploy this project run

## 1. Login to AWS console, or other cloud providers

## 2. Create an IAM user for deployment

	  With specific access

	1. EC2 access: It is a virtual machine

## 3 Create EC2 machine (Ubuntu) 
  #### With Accurate CPU/memory and storage. 

## 4 Run the below commands in your ec2 instance.
  sudo apt-get update 
  sudo apt-get install -y ca-certificates curl  gnupg lsb-release 
  sudo mkdir -p /etc/apt/keyrings curl -fsSL https://download.docker.com/linux/ubuntu/gpg | 
sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null 

sudo apt-get update 

sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin 

sudo systemctl start docker 

sudo systemctl enable docker 

sudo usermod -aG docker current_logged_in_user/ or the user_name you would like you use.

### 5 Now Pull the latest image from my dockerhub. (Note use sudo before any command if you are not a root user.)
docker pull shivamshane/imagecaption:latest

##### This will take some time to download and extract images. once done, run the below command to start the container.
    Command: docker images
This will list the image name and its ID.

    Command docker run -d -p 8080:8080 container_name or container_ID(Got from the above command)

This will start the container having container and host port 8080:8080 learn more about docker here https://docs.docker.com/

Make sure you have configured your Ec2 instance inbound rule to accept connections from all or specific IP and port 8080 is allowed. 

    Learn here about security groups https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html





## 🚀 About Me
Hi 👋, I'm Shivam

I am a highly skilled and decisive 
professional with developed expertise in various AI/ML technologies.

## Demo
https://github.com/Shivam-Shane/My_portfolio_website/blob/main/images/project/imagecaption.gif

## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://shivam-shane.github.io/My_portfolio_website/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shivam-2641081a0/)
[![Medium](https://img.icons8.com/?size=60&id=XVNvUWCvvlD9&format=png&color=000000)](https://medium.com/@sk0551460)



## Feedback

If you have any feedback, please reach out to us at sk0551460@gmail.com

## FAQ for Image Captioning Project
### 1. What is the Image Captioning project about?
The Image Captioning project implements a deep learning model that generates descriptive captions for images. It uses convolutional neural networks (CNNs) for feature extraction and recurrent neural networks (RNNs) for generating captions.
### 2. What are the key components of this project?
The key components include:
Data Preprocessing: Converting images and captions into a suitable format for training.
Feature Extraction: Using a pre-trained CNN (like InceptionV3) to extract features from images.
Captioning Model: An RNN (GRU) that generates captions based on the extracted image features.
Training: The process of training the model using a dataset of images and their corresponding captions.
### 3. Which dataset is used for training the model?
The project uses the Flickr30k dataset, which consists of 30,000 images with five different captions provided for each image.
### 4. How can I set up the project locally?
To set up the project locally:
Follow the installation instructions.
### 5. What are the dependencies required for this project?
The project requires Python 3. 10 and the following Python libraries:
TensorFlow or Keras
NumPy
Pandas
Keras
Matplotlib
Pillow
Django
You can install all dependencies using the provided requirements.txt file.
### 6. How does the model generate captions?
The model first uses a pre-trained CNN (resnet50) to extract feature vectors from the input image. These features are then passed to a GRU network, which generates the caption word by word.
### 7. How can I evaluate the model's performance?
The model’s performance can be evaluated using metrics like the BLEU score, which measures the similarity between the generated captions and the reference captions in the dataset.
### 8. Can I use a different dataset for training the model?
Yes, you can use a different dataset. You will need to ensure that the dataset is structured similarly, with images and corresponding captions. Modifications to the data preprocessing pipeline may be required.
### 9. Is the model pre-trained, or do I need to train it from scratch?
The model provided is designed to be trained from scratch. However, you can use pre-trained models or weights to fine-tune and accelerate the training process which is already there in the artifacts directory.
### 10. How do I run the model inference on new images?
To generate captions for new images:
Follow the installation instructions.
### 11. What are some common issues I might face while running the project?
Some common issues include:
Dependency conflicts: Make sure all required libraries are installed in the correct versions.
Memory issues: Training the model can be memory-intensive; using a machine with sufficient GPU/CPU resources is recommended.
Dataset path errors: Ensure that the dataset is placed in the correct directory if training from scratch, and the paths are correctly specified in the code.
### 12. Can I contribute to this project?
Yes, contributions are welcome! You can fork the repository, make improvements or fix issues, and submit a pull request. 
### 13. Where can I find the model checkpoints and saved models?
Model checkpoints and saved models are stored in the specified directories[artifacts] within the project structure. You may need to create these directories before training if they don't exist.

## Contact

For questions, suggestions, or support, reach out at 
- **sk0551460@gmail.com** 
- **shivam.hireme@gmail.com**.

## Support the Project

Help support continued development and improvements:

- **Follow on LinkedIn**: Stay connected for updates – [LinkedIn Profile](https://www.linkedin.com/in/shivam-hireme/)
- **Buy Me a Coffee**: Appreciate the project? [Buy Me a Coffee](https://buymeacoffee.com/shivamshane)
- **Visit my Portfolio**: [Shivam's Portfolio](https://shivam-portfoliio.vercel.app/)
