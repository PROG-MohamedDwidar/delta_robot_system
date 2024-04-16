from ultralytics import YOLO
from roboflow import Roboflow
# Load a model
rf = Roboflow(api_key="kjo7aNtqeeTbpsnA56ef")
project = rf.workspace("modwi").project("garbagedetectandclassify")
dataset = project.version(1)

project.version(dataset.version).deploy(model_type="yolov8", model_path=f"runs/detect/train/")