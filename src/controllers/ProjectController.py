from .BaseController import BaseController
from fastapi import FastAPI
from models import ResponseSignal
import os

class ProjectController(BaseController):

    def __init__(self):
        super().__init__()


    # hayde l function btjeb l project id mn l project dir w eza msh mawjood bta3malo create w 
    # btreddelak l project dir
    
    def getProjectPath(self, project_id: str):
        project_dir = os.path.join(self.file_dir, project_id)

        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        return project_dir