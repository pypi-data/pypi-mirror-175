import requests


class DealWithDatasets:
    def __init__(self,
                 user_id=None,
                 workspace_id=None,
                 project_id=None,
                 exp_id=None,
                 team_id=None,
                 artifact_set_id=None,
                 artifact_type_id=None,
                 api_key=None,
                 dataset_name=None,
                 file_path=None,
                 description=None,
                 ):
        self.user_id = user_id
        self.workspace_id = workspace_id
        self.project_id = project_id
        self.exp_id = exp_id
        self.team_id = team_id
        self.api_key = api_key
        self.artifact_id=artifact_set_id
        self.artifact_type_id=artifact_type_id
        self.dataset_name = dataset_name
        self.file_path = file_path
        self.file = None
        self.description = description

    def process_datasets(self):
        if self.file_path.split("/")[-1].split('.')[-1] == 'csv':
            self.file = {'file': open(self.file_path, "rb")}
        elif self.file_path.split("/")[-1].split('.')[-1] == 'zip':
            self.file = {'file': open(self.file_path, "rb")}

        return self.file

    def register_dataset(self):
        res = requests.post("http://127.0.0.1:8000/save/datasets",
                            params={"user_id": self.user_id,
                                    "workspace_id": self.workspace_id,
                                    "project_id": self.project_id,
                                    "exp_id": self.exp_id,
                                    "team_id": self.team_id,
                                    "artifact_type_id": self.artifact_type_id,
                                    "artifact_id":self.artifact_id,
                                    "dataset_name": self.dataset_name,
                                    "description": self.description}
                            ,
                            files=self.process_datasets())
        print(res.json(), "datasets")
        return res.json()


# if __name__ == "__main__":
#     import time
#     start = time.time()
#     dataset = DealWithDatasets(
#         user_id="dbdudska113@naver.com",
#         workspace_id="sadalksdjaksd2223",
#         project_id="sdsdsdsad2335zcv",
#         exp_id="sdsadadqerghnvcv",
#         team_id="sdsdjskhdj3",
#         api_key="sdkjdvcewkejwrioewjrkl2",
#         dataset_name="hell",
#         file_path="/Users/youyoungnam/PycharmProjects/trumpet-client-dev/trumpet_client/launch/train.csv",
#         description="ajasjcvv2"
#     )
#     print(dataset.register_dataset())
#     end = time.time()
#     print("걸리는 시간: ", end - start)