if __name__ == '__main__':
    import torch 
    from ultralytics import YOLO  

    
    model = YOLO('yolov8n.pt')  
    model.train(data='hello.yaml', epochs=500)
