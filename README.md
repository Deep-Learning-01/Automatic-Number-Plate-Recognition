<h1 align="center">Automatic-Number-Plate-Recognition</h1>

<h5>   License plate detection and recognition is the technology that uses computer vision to detect and recognize a license plate from an input image of a car.In the following project, we will understand how to recognize License number plates using deep learning. We will utilize OpenCV for this project in order to identify the license number plates and the python Paddle OCR for the characters and digits extraction from the plate.
 </h5>

 </br>

## <img src="https://c.tenor.com/NCRHhqkXrJYAAAAi/programmers-go-internet.gif" width="25">  <b>Built With</b>

- Python
- Flask
- Deep learning
- Docker
- AWS

## 🌐 Infrastructure Required.

1. AWS S3
2. AWS EC2
3. AWS ECR
4. Git Actions
5. Terraform

 ## <img src="https://media2.giphy.com/media/QssGEmpkyEOhBCb7e1/giphy.gif?cid=ecf05e47a0n3gi1bfqntqmob8g9aid1oyj2wr3ds3mg700bl&rid=giphy.gif" width ="25"><b> Snippets </b>
 <b>Image Upload Interface</b><img src= "https://github.com/satyazmx/dataset/blob/main/one.png">

<b>Interface allows user to input only image</b><img src= "https://github.com/satyazmx/dataset/blob/main/two.png">

<b>Interface for correct file format</b><img src= "https://github.com/satyazmx/dataset/blob/main/three.png">

<b>Result with cropped number plate and OCR text of number</b><img src= "https://github.com/satyazmx/dataset/blob/main/4.png">

## <img src="https://media.giphy.com/media/iY8CRBdQXODJSCERIr/giphy.gif" width="25"> <b> Data Understanding</b>


- Data consist of 400 car images with their number plates.
- Data consists of 400 XML annotations.


 ## 💻 How to setup:


Creating conda environment
```
conda create -p venv python==3.8 -y
```

activate conda environment
```
conda activate ./venv
```

Install requirements
```
pip install -r requirements.txt
```

Export the environment variable
```
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

export AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>


```
Run the live server using uvicorn
```
python app.py
```
To launch ui
```
http://127.0.0.1:5000/
```

## 🏭 Industrial Use-cases 
<h5>This technology applies in many areas. On roads, it is used to identify the cars that are breaking the traffic rules. In security, it is used to capture the license plates of the vehicles getting into and out of certain premises. In parking lots, it is used to capture the license plates of the cars being parked. The list of its applications goes on and on.</h5>

1. Vehicle Parking 
2. Toll Enforcement
3. vehicle Surveillance
4. Traffic control

 ## <img src="https://media2.giphy.com/media/QssGEmpkyEOhBCb7e1/giphy.gif?cid=ecf05e47a0n3gi1bfqntqmob8g9aid1oyj2wr3ds3mg700bl&rid=giphy.gif" width ="25"><b> Languages & Libraries Used</b>


 
<p>
<a><img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen" alt="Seaborn"/></a>
 <a><img src="https://matplotlib.org/_static/logo2_compressed.svg" alt="cplusplus" width="110"/></a>
<a><img src="https://seaborn.pydata.org/_static/logo-wide-lightbg.svg" alt="Seaborn"width="110"/></a>
  <code> <img height="50" src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Spyder_logo.svg"> </code>
  <code> <img height="50" src="https://www.vectorlogo.zone/logos/jupyter/jupyter-ar21.svg"> </code>
  <code> <img height="50" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pandas_logo.svg/768px-Pandas_logo.svg.png"> </code>
  <code> <img height="50" src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-ar21.svg"> </code>
  <code> <img height="50" src="https://www.vectorlogo.zone/logos/numpy/numpy-ar21.svg"> </code>
  <code> <img height="50" src="https://raw.githubusercontent.com/valohai/ml-logos/master/scipy.svg"> </code>
  <code> <img height="50" src="https://seeklogo.com/images/S/scikit-learn-logo-8766D07E2E-seeklogo.com.png"> </code>
</p>
