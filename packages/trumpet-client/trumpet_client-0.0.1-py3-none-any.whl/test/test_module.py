import unittest
from trumpet_client import version
from trumpet_client import dev_version
from trumpet_client.api import crud as CRUD_API
from trumpet_client.api.api_var import snake_to_camel

'''
1. 웹에서 진행할 부분
    1. 회원가입
    2. API 키 발급
    3. 팀 생성 (혹은 1인 팀)
    4. 해당 팀 안에 워크스페이스 생성 완료
    5. 해당 워크스페이스 안에 프로젝트 생성 완료
2. SDK에서 진행할 부분
    1. API 키를 포함한 init
    2. 목록 반환
        1. 유저가 속해있는 팀 목록 반환
        2. 팀 안에 있는 워크스페이스 목록 반환
        3. 워크스페이스 안에 있는 프로젝트 목록 반환
        4. 프로젝트 안에 있는 실험 목로 반환
    3. 실험 생성
        1. 실험 init 시 워크스페이스, 프로젝트를 지정할 수 있음. 미지정시 유저의 기본 워크스페이스 안에 생성되도록 로직 설계.
        2. 해당 파일의 소스 코드가 전송됨.
        3. 로그 전송이 필요하다면 실험이 시작되는 부분과 종료되는 부분을 명시해줘야함.
    4. 정보 반환
        1. 유저 정보 반환
            1. 유저 아이디
            2. 유저 네임
        2. 팀 정보 반환
            1. 팀 아이디
            2. 팀 네임
            3. 팀 설명
            4. 해당 유저의 팀 내 역할
        3. 워크스페이스 정보 반환
            1. 워크스페이스 아이디
            2. 워크스페이스 네임
            3. 워크스페이스 설명
            4. 해당 유저의 워크스페이스 내 역할
        4. 프로젝트 정보 반환
            1. 프로젝트 아이디
            2. 프로젝트 네임
            3. 프로젝트 설명
            4. 해당 유저의 프로젝트 내 역할
        5. 실험 정보 반환
            1. 실험 아이디
            2. 실험 네임
            3. 실험 설명
    5. 아티팩트 등록 TODO
        현재는 코드, 소스, 메트릭, 로그 등 필드별로 분산되어있어 관리상 불필요한 부분이 있음
        아티팩트 테이블로 통합하거나
        테이블의 형식을 통일시킬 필요가 있음
    6. 기타 기능
        1. versioning
            모델
'''
class Solution:
    def __init__(self, api_key):
        self.api_key = "7e5b91e535c8e8fda2614420a4c1e5ff4e67438e455119c77b6ba65c027948d1"
        self.results = {}
        self.results['user'] = {}
        self.results['team'] = {}
        self.results['workspace'] = {}
        self.results['project'] = {}
        self.results['experiments'] = {}
        self.results['model'] = {}
        self.results['metric'] = {}
        self.API = CRUD_API.CRUD_API(api_key=self.api_key)
        self.headers = self.headers = {"x-api-key":self.api_key}


    def read_user(self):
        json = {
            "api_key":self.api_key
        }
        results = self.API.user().read(headers=self.headers, json=json)
        self.results['user']['read'] = results
        return results

    def read_team(self):
        results = self.results['user']["read"]["resResult"]["teamMembers"]
        self.results['team']['read'] = results
        return results

    def create_workspace(self):
        json = {
            "work_name":"workspace",
            "ac_user_id":self.results['user']['read']["resResult"]["userId"],
            "create_user":self.results['user']['read']["resResult"]["userId"],
        }
        results = self.API.workspace().create(headers=self.headers, json=json)
        self.results["workspace"]["create"] = results
        return results

    def read_workspace(self):
        params = {
            "id":self.results["workspace"]["create"]["resResult"]["workId"]
        }
        results = self.API.workspace().read(headers=self.headers, params=params)
        self.results['workspace']["read"] = results
        return results

    def update_workspace(self):
        params = {
            "id":self.results["workspace"]["create"]["resResult"]["workId"]
        }
        json = {
            "work_name":"update workspace"
        }
        results = self.API.workspace().update(headers=self.headers, params=params, json=json)
        self.results['workspace']["update"] = results
        return results

    def delete_workspace(self):
        params = {
            "id":self.results["workspace"]["create"]["resResult"]["workId"]
        }
        results = self.API.workspace().delete(headers=self.headers, params=params)
        self.results['workspace']["delete"] = results
        return results

    def create_project(self):
        json = {
            "prt_name":"project",
            "ac_user_id":self.results['user']['read']["resResult"]["userId"],
            "work_id": self.results['workspace']['read']["resResult"]["workId"],
        }
        results = self.API.project().create(headers=self.headers, json=json)
        self.results["project"]["create"] = results
        return results

    def read_project(self):
        params = {
            "id":self.results["project"]["create"]["resResult"]["prtId"]
        }
        results = self.API.project().read(headers=self.headers, params=params)
        self.results['project']["read"] = results
        return results

    def update_project(self):
        params = {
            "id":self.results["project"]["create"]["resResult"]["prtId"]
        }
        json = {
            "prt_name":"update project",
            "work_id": self.results['workspace']['read']["resResult"]["workId"],
        }
        results = self.API.project().update(headers=self.headers, params=params, json=json)
        self.results['project']["update"] = results
        return results

    def delete_project(self):
        params = {
            "id":self.results["project"]["create"]["resResult"]["prtId"]
        }
        results = self.API.project().delete(headers=self.headers, params=params)
        self.results['project']["delete"] = results
        return results

    def create_experiments(self):
        json = {
            "exp_name":"experiments",
            "prt_id": self.results['project']['read']["resResult"]["prtId"],
        }
        results = self.API.experiments().create(headers=self.headers, json=json)
        self.results["experiments"]["create"] = results
        return results

    def read_experiments(self):
        params = {
            "id":self.results["experiments"]["create"]["resResult"]["expId"]
        }
        results = self.API.experiments().read(headers=self.headers, params=params)
        self.results['experiments']["read"] = results
        return results

    def update_experiments(self):
        params = {
            "id":self.results["experiments"]["create"]["resResult"]["expId"]
        }
        json = {
            "exp_name":"update experiments",
            "prt_id": self.results['project']['read']["resResult"]["prtId"],
        }
        results = self.API.experiments().update(headers=self.headers, params=params, json=json)
        self.results['experiments']["update"] = results
        return results

    def delete_experiments(self):
        params = {
            "id":self.results["experiments"]["create"]["resResult"]["expId"]
        }
        results = self.API.experiments().delete(headers=self.headers, params=params)
        self.results['experiments']["delete"] = results
        return results

    def create_model(self):
        # data 로 camel case로 쏴줘야함
        data = {
            "model_name":"model",
            "work_id": self.results['workspace']['read']["resResult"]["workId"],
            "prt_id": self.results['project']['read']["resResult"]["prtId"],
            "exp_id": self.results['experiments']['read']["resResult"]["expId"],
        }
        files =[
            ("file",('artifact.art', open('artifact.art', 'rb'), 'application/octet-stream'))
        ]
        data = {snake_to_camel(k):v for k,v in data.items()}
        results = self.API.model().create(headers=self.headers, data=data, files=files)
        self.results["model"]["create"] = results
        return results

    def read_model(self):
        params = {
            "id":self.results["model"]["create"]["resResult"]["modelId"]
        }
        results = self.API.model().read(headers=self.headers, params=params)
        self.results['model']["read"] = results
        return results

    def update_model(self):
        params = {
            "id":self.results["model"]["create"]["resResult"]["modelId"]
        }
        data = {
            "model_name":"update model",
            "work_id": self.results['workspace']['read']["resResult"]["workId"],
            "prt_id": self.results['project']['read']["resResult"]["prtId"],
            "exp_id": self.results['experiments']['read']["resResult"]["expId"],
        }
        files =[
            ("file",('artifact.art', open('artifact.art', 'rb'), 'application/octet-stream'))
        ]
        data = {snake_to_camel(k):v for k,v in data.items()}
        results = self.API.model().update(headers=self.headers, params=params, data=data, files=files)
        self.results['model']["update"] = results
        return results

    def delete_model(self):
        params = {
            "id":self.results["model"]["create"]["resResult"]["modelId"]
        }
        results = self.API.model().delete(headers=self.headers, params=params)
        self.results['model']["delete"] = results
        return results

solution = Solution()


class Testclass(unittest.TestCase):
    # 테스트 호출 하기 이전에 작업 하는 내용 예를들어 테스트 변수 선언
    def setUp(self):
        # self.testValueW, self.testValueP, self.test_ValueA = "workspace", "project", "api_key"
        # self.params = {"random_state": 42, "epochs": 100, "train_test_split": 0.75}
        # self.init = init(workspace=self.testValueW, project=self.testValueP, api_key=self.test_ValueA)
        # self.init["parames"] = self.params

        self.api_key = "7e5b91e535c8e8fda2614420a4c1e5ff4e67438e455119c77b6ba65c027948d1"
        self.headers = {"api_key":self.api_key}
        self.API = CRUD_API.CRUD_API(api_key=self.api_key)

        # '''
        # ***** USER START *****
        # '''
        # # USER ID
        # self.user_results = {}
        # json = {
        #     "api_key":self.api_key
        # }
        # # results={'resCode':200,'resResult':{'userId':'admin','teamMembers':[{'teamId':'MLOps-1','teamName':'MLOps-1'}]}}
        # results = self.API.user().read(headers=self.headers, json=json)
        # self.user_results["read"] = results
        # '''
        # ***** USER END *****
        # '''
        # '''
        # ***** TEAM START *****
        # '''
        # self.team_results = {}
        # # # TEAM
        # # json = {
        # #     "user_id":self.user_results["read"]["resResult"]["userId"]
        # # }
        # # results = self.API.team().read(headers=self.headers, json=json)
        # results = self.user_results["read"]["resResult"]["teamMembers"]
        # self.team_results['read'] = results
        # '''
        # ***** TEAM END *****
        # '''
        # # WORKSPACE
        # '''
        # ***** WORKSPACE START *****
        # '''
        # self.workspace_results = {}
        #
        # # # CREATE
        # # json = {
        # #     "work_id":workspace['workId'],
        # #     "prt_name":"workspace",
        # # }
        # # results = self.workspace_API.create(headers=self.headers, json=json)
        # # self.workspace_results["create"] = results
        #
        # # READ
        # json = {
        #     "ac_user_id":self.user_results['read']["resResult"]["userId"],
        #     "team_id":self.team_results['read'][0]["teamId"],
        # }
        # results = self.API.workspace().read(headers=self.headers, json=json)
        # self.workspace_results["read"] = results
        #
        # # # UPDATE
        # # updated_name = "updated workspace"
        # # json = {
        # #     "prt_id":self.workspace_results["create"]["resResult"]['prtId'],
        # #     "prt_name":updated_name,
        # # }
        # # results = self.API.workspace().update(headers=self.headers, json=json)
        # # self.workspace_results["update"] = results
        #
        # # # DELETE
        # # json = {
        # #     "prt_id":self.workspace_results["update"]["resResult"]['prtId'],
        # #     "ac_user_id":self.user_id
        # # }
        # # results = self.API.workspace().delete(headers=self.headers, json=json)
        # # self.workspace_results["delete"] = results
        # '''
        # ***** WORKSPACE END *****
        # '''
        # '''
        # ***** PROJECT START *****
        # '''
        # self.project_results = {}
        #
        # # # CREATE
        # # json = {
        # #     "work_id":workspace['workId'],
        # #     "prt_name":"project",
        # # }
        # # results = self.project_API.create(headers=self.headers, json=json)
        # # self.project_results["create"] = results
        #
        # # READ
        # json = {
        #     "work_id":self.workspace_results["read"]["resResult"][1]['workId']
        # }
        # results = self.API.project().read(headers=self.headers, json=json)
        # self.project_results["read"] = results
        #
        # # # UPDATE
        # # updated_name = "updated project"
        # # json = {
        # #     "prt_id":self.project_results["create"]["resResult"]['prtId'],
        # #     "prt_name":updated_name,
        # # }
        # # results = self.API.project().update(headers=self.headers, json=json)
        # # self.project_results["update"] = results
        #
        # # # DELETE
        # # json = {
        # #     "prt_id":self.project_results["update"]["resResult"]['prtId'],
        # #     "ac_user_id":self.user_id
        # # }
        # # results = self.API.project().delete(headers=self.headers, json=json)
        # # self.project_results["delete"] = results
        # '''
        # ***** PROJECT END *****
        # '''
        # '''
        # ***** EXPERIMENTS START *****
        # '''
        # self.experiments_results = {}
        #
        # # CREATE
        # json = {
        #     "exp_name":"experiments",
        #     "work_id":self.workspace_results["read"]["resResult"][1]['workId'],
        #     "prt_id":self.project_results["read"]["resResult"][1]['prtId'],
        #     "status":"T",
        #     "tag":["test"],
        #     "start_time": "2022-04-12T19:00:12",
        #     "end_time": "2022-04-12T19:00:12",
        #     "duration_time": "1234567",
        # }
        # results = self.API.experiments().create(headers=self.headers, json=json)
        # self.experiments_results["create"] = results
        #
        # # READ
        # json = {
        #     "prt_id":self.project_results["read"]["resResult"][0]['prtId'],
        # }
        # results = self.API.experiments().read(headers=self.headers, json=json)
        # self.experiments_results["read"] = results
        #
        # # UPDATE
        # updated_name = "updated experiments"
        # json = {}
        # for key, item in self.experiments_results["create"]["resResult"].items():
        #     json[CRUD_API.camel_to_snake(key)] = item
        # json['tag'] = json['tag'].split()
        # json['exp_name'] = updated_name
        # results = self.API.experiments().update(headers=self.headers, json=json)
        # self.experiments_results["update"] = results
        #
        # # DELETE
        # json = {
        #     "exp_id":self.experiments_results["update"]["resResult"]['expId'],
        #     # "ac_user_id":self.user_results['read']["resResult"]["userId"],
        # }
        # results = self.API.experiments().delete(headers=self.headers, json=json)
        # self.experiments_results["delete"] = results
        # '''
        # ***** EXPERIMENTS END *****
        # '''
        # '''
        # ***** USER CODE START *****
        # '''
        # # self.usercode_results = {}
        # #
        # # # CREATE
        # # json = {
        # #     "exp_name":"usercode",
        # #     # "work_id":self.workspace_results["read"]["resResult"][0]['workId'],
        # #     "prt_id":self.project_results["read"]["resResult"][0]['prtId'],
        # #     "status":"T",
        # #     "tag":["test"],
        # #     "start_time": "2022-04-12T19:00:12",
        # #     "end_time": "2022-04-12T19:00:12",
        # #     "duration_time": "1234567",
        # # }
        # # results = self.API.usercode().create(headers=self.headers, json=json)
        # # self.usercode_results["create"] = results
        # #
        # # # READ
        # # json = {
        # #     "prt_id":self.project_results["read"]["resResult"][0]['prtId'],
        # # }
        # # results = self.API.usercode().read(headers=self.headers, json=json)
        # # self.usercode_results["read"] = results
        # #
        # # # UPDATE
        # # updated_name = "updated usercode"
        # # json = {}
        # # for key, item in self.usercode_results["create"]["resResult"].items():
        # #     json[CRUD_API.camel_to_snake(key)] = item
        # # json['tag'] = json['tag'].split()
        # # json['exp_name'] = updated_name
        # # results = self.API.usercode().update(headers=self.headers, json=json)
        # # self.usercode_results["update"] = results
        # #
        # # # DELETE
        # # json = {
        # #     "exp_id":self.usercode_results["update"]["resResult"]['expId'],
        # #     # "ac_user_id":self.user_results['read']["resResult"]["userId"],
        # # }
        # # results = self.API.usercode().delete(headers=self.headers, json=json)
        # # self.usercode_results["delete"] = results
        # '''
        # ***** USER CODE END *****
        # '''
        #
        # '''
        # ***** MODEL START *****
        # '''
        # self.model_results = {}
        #
        # # CREATE
        # json = {
        #     "exp_name":"model",
        #     # "work_id":self.workspace_results["read"]["resResult"][0]['workId'],
        #     "prt_id":self.project_results["read"]["resResult"][0]['prtId'],
        #     "status":"T",
        #     "tag":["test"],
        #     "start_time": "2022-04-12T19:00:12",
        #     "end_time": "2022-04-12T19:00:12",
        #     "duration_time": "1234567",
        # }
        # results = self.API.model().create(headers=self.headers, json=json)
        # self.model_results["create"] = results
        #
        # # READ
        # json = {
        #     "prt_id":self.project_results["read"]["resResult"][0]['prtId'],
        # }
        # results = self.API.model().read(headers=self.headers, json=json)
        # self.model_results["read"] = results
        #
        # # UPDATE
        # updated_name = "updated model"
        # json = {}
        # for key, item in self.model_results["create"]["resResult"].items():
        #     json[CRUD_API.camel_to_snake(key)] = item
        # json['tag'] = json['tag'].split()
        # json['exp_name'] = updated_name
        # results = self.API.model().update(headers=self.headers, json=json)
        # self.model_results["update"] = results
        #
        # # DELETE
        # json = {
        #     "exp_id":self.model_results["update"]["resResult"]['expId'],
        #     # "ac_user_id":self.user_results['read']["resResult"]["userId"],
        # }
        # results = self.API.model().delete(headers=self.headers, json=json)
        # self.model_results["delete"] = results
        # '''
        # ***** MODEL END *****
        # '''

        # '''
        # ***** ARTIFACT_SET AND ARTIFACT START *****
        # '''
        # self.artifact_set_results = {}
        # # CREATE ARTIFACT SET
        # json = {
        #     "artifact_set_name":"artifact",
        #     # TODO
        #     # "work_id":self.workspace_results["read"]["resResult"][0]['workId'],
        #     # "prt_id":self.project_results["read"]["resResult"][0]['prtId'],
        #     "tag":["test"],
        # }
        # results = self.API.artifact_set().create(headers=self.headers, json=json)
        # self.artifact_set_results["create"] = results
        #
        # # READ ARTIFACT SET
        # json = {
        #     "id":self.artifact_set_results["create"]["resResult"]['artifactSetId'],
        # }
        # results = self.API.artifact_set().read(headers=self.headers, params=json)
        # self.artifact_set_results["read"] = results
        #
        # self.artifact_results = {}
        # # CREATE ARTIFACT
        # f = open('artifact.art', 'rb')
        # data = {
        #     "artifactSetId":self.artifact_set_results["create"]["resResult"]['artifactSetId'],
        #     # "file":f,
        #     # TODO
        #     # "work_id":self.workspace_results["read"]["resResult"][0]['workId'],
        #     # "prt_id":self.project_results["read"]["resResult"][0]['prtId'],
        #     "tag":["test"],
        # }
        # files =[
        #     ("file",('artifact.art', open('artifact.art', 'rb'), 'application/octet-stream'))
        # ]
        # results = self.API.artifact().create(headers=self.headers, data=data, files=files)
        # self.artifact_results["create"] = results
        #
        # # READ ARTIFACT
        # params = {
        #     "id":self.artifact_results["create"]["resResult"]['artifactId'],
        # }
        # results = self.API.artifact().read(headers=self.headers, params=params)
        # self.artifact_results["read"] = results
        #
        #
        # # UPDATE
        # updated_name = "updated artifact set"
        # json = {}
        # for key, item in self.artifact_set_results["create"]["resResult"].items():
        #     json[CRUD_API.camel_to_snake(key)] = item
        # json['tag'] = json['tag'].split()
        # json['artifact_set_name'] = updated_name
        # params = {
        #     "id":self.artifact_results["create"]["resResult"]['artifactId'],
        # }
        # results = self.API.artifact_set().update(headers=self.headers, params=params, json=json)
        # self.artifact_set_results["update"] = results
        #
        # # DELETE
        # json = {
        #     "exp_id":self.model_results["update"]["resResult"]['expId'],
        #     # "ac_user_id":self.user_results['read']["resResult"]["userId"],
        # }
        # results = self.API.model().delete(headers=self.headers, json=json)
        # self.model_results["delete"] = results
        # '''
        # ***** ARTIFACT_SET AND ARTIFACT END *****
        # '''

    # def test__is_valid_api_key(self):
    #     with self.assertRaises(Exception): _is_valid_api_key(api_key="")
    #     with self.assertRaises(Exception): _is_valid_api_key()

    # def test_getParams(self):
    #     self.assertEqual(self.init.info_param()[0]["parames"], self.params)
    #
    # def test_userInfo(self):
    #     self.assertEqual(self.init.userinfo()["apikey"], self.test_ValueA)

    def test_version(self):
        self.assertEqual(version(), dev_version)

    # def test_project_CRUD_create(self):
    #     self.assertEqual(self.project_results['create']['resCode'], 200)

    # def test_project_CRUD_read(self):
    #     self.assertEqual(self.project_results['read']['resCode'], 200)

    # def test_project_CRUD_update(self):
    #     self.assertEqual(self.project_results['update']['resCode'], 200)
    #
    # def test_project_CRUD_delete(self):
    #     self.assertEqual(self.project_results['delete']['resCode'], 200)
    def test_workspace(self):
        solution.read_user()
        solution.read_team()
        solution.create_workspace()
        solution.read_workspace()

        solution.create_project()
        solution.read_project()

        solution.create_experiments()
        solution.read_experiments()

        solution.create_model()
        solution.read_model()

        solution.update_model()
        solution.delete_model()

        solution.update_experiments()
        solution.delete_experiments()


        solution.update_project()
        solution.delete_project()

        solution.update_workspace()
        solution.delete_workspace()
    def main(self):
        unittest.main()
