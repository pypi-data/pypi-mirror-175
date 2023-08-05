import warnings
from trumpet_client.envs import ERROR_STYLE


class TrumpetException(Exception):
    pass


class TrumpetUnverfiedApiKey(TrumpetException):
    def __init__(self, api_key):
        messages = f"""
        {ERROR_STYLE["h1"]}
        Exception
        !!TrumpetUnverfiedApiKey(TrumpetException)!!
        {ERROR_STYLE["h2"]}
        Contents
        you input blank to api_key
        {ERROR_STYLE["h2"]}Code{ERROR_STYLE["end"]}
        trumpet_client.init(api_key={api_key})
        """
        super(TrumpetUnverfiedApiKey, self).__init__(
            messages
        )


class TrumpetNoneApiKey(TrumpetException):
    def __init__(self, api_key):
        messages = f"""
        {ERROR_STYLE["h1"]}
        Exception
        !!TrumpetNoneApiKey(TrumpetException)!!
        {ERROR_STYLE["h2"]}
        Contents
        you input None value to api_key
        The default value is None.
        {ERROR_STYLE["h2"]}Code{ERROR_STYLE["end"]}
        trumpet_client.init(api_key={api_key})
        """
        super(TrumpetNoneApiKey, self).__init__(
            messages
        )


class TrumpetUnverfiedWorkspaceId(TrumpetException):

    def __init__(self, workspace_id=None):
        messages = f"""
        {ERROR_STYLE["h1"]}
        !!TrumpetUnverfiedWorkspaceId!!
        {ERROR_STYLE["end"]}
        {ERROR_STYLE["h2"]}Contents{ERROR_STYLE["end"]}
        you input None to workspace_id
        workspaceId has not been inputted
        {ERROR_STYLE["h2"]}Code{ERROR_STYLE["end"]}
        trumpet_client.init(workspace_id={workspace_id})
        """
        super(TrumpetUnverfiedWorkspaceId, self).__init__(
            messages
        )


class TrumpetUnverfiedProjectId(TrumpetException):

    def __init__(self, project_id=None):
        messages = f"""
        {ERROR_STYLE["h1"]}
        !!TrumpetUnverfiedProjectId!!
        {ERROR_STYLE["h2"]}
        Contents
        Project_id has not been inputted.

        {ERROR_STYLE["h2"]}Code{ERROR_STYLE["end"]}
        trumpet_client.init(project_id={project_id})
        """
        super(TrumpetUnverfiedProjectId, self).__init__(
            messages
        )


class TrumpetUnverfiedUserId(TrumpetException):

    def __init__(self, user_id=None):
        messages = f"""
        {ERROR_STYLE["h1"]}
        !!TrumpetUnverfiedUserId!!
        {ERROR_STYLE["h2"]}
        Contents
        user_id has not been inputted.

        {ERROR_STYLE["h2"]}Code{ERROR_STYLE["end"]}
        trumpet_client.init(user_id={user_id})
        """
        super(TrumpetUnverfiedUserId, self).__init__(
            messages
        )


class TrumpetInfoToUserStartStop(UserWarning):

    def __init__(self, workspace, project_id, api_key):
        messages = f"""
        [WARING] After learning the machine learning model, save the model and stop if you want to see
        the source code you wrote and the saved model.
        [EX] run = trumpet_client.init(workspace={workspace}, project={project_id}, api_key={api_key})
             run.stop()
        """
        warnings.warn(messages)


class TrumpetInfoToSameNameModel(UserWarning):

    def __init__(self, model_name, workspace_id, model_len):
        messages = f"\nthere are {model_len} counts model registered  with the samed {model_name} in workspace ID: {workspace_id}.\nPlease enter model version"
        warnings.warn(messages)


class TrumpetInfoToModelVersion(UserWarning):
    def __init__(self, model_name):
        messages = f"""
        [WARNING] 
        You did not enter a model version. {model_name} is registered with the default value of v-1.
        You can safely ignore this warning.
        """
        warnings.warn(messages)


class TrumpetJupyterFileTimeout(TrumpetException):

    def __init__(self):
        messages = """
        Please can't send your jupyter notebook file to server so that,
        check if your jupyter notebook port is being used elsewhere
        If possible, remove it and try
        run = trumpet_client.init
        run.stop() again.
        """
        super(TrumpetJupyterFileTimeout, self).__init__(
            messages
        )


class TrumpetClientException(TrumpetException):
    def __init__(self, detail=""):
        message = f"""
        Please Check Exception.
        {detail}
        """
        super(TrumpetClientException, self).__init__(
            message
        )


class TrumpetModelSaveFormatException(TrumpetException):
    def __init__(self, format=None):
        message = f"""
        the model file format [{format}] you are trying to register is not supported.
        """
        super(TrumpetModelSaveFormatException, self).__init__(
            message
        )


class TrumpetServerErrorException(TrumpetException):
    def __init__(self):
        message = f"""
        The server is currently down. 
        Please leave your comment on http://www.trumpet.ai/QnA.
        """
        super(TrumpetServerErrorException, self).__init__(
            message
        )


class TrumpetWorkspaceInNothingModel(TrumpetException):
    def __init__(self, workspace_id, model_name):
        messages = f"""
        The {model_name} does not exist in the workspace: {workspace_id}\n
        Make sure the model exists in the model repository
        """
        super(TrumpetWorkspaceInNothingModel, self).__init__(messages)


class TrumpetSameModelException(TrumpetException):
    def __init__(self, model_name, model_version, project_id):
        message = f"""
        {model_name}: {model_version} exists within the current project ID: {project_id}
        Please try to register with the new version
        but if you want to overwrite model, please use overwrite_model parameter default is False.
        """
        super(TrumpetSameModelException, self).__init__(
            message
        )


class TrumpetMetricTypeException(TrumpetException):
    def __init__(self):
        message = f"""
        It is a form of a non-collectible type. Please check the type.
        """
        super(TrumpetMetricTypeException, self).__init__(
            message
        )


class TrumpetDataSetSameNameException(TrumpetException):
    def __init__(self, dataset_name):
        message = f"""
        There is a dataset registered with {dataset_name}. Please try a different name.        
        """
        super(TrumpetDataSetSameNameException, self).__init__(
            message
        )

class TrumpetModelException(TrumpetException):
    def __init__(self):
        message = f"""
            The model could not be downloaded due to a server problem. Please contact us.
        """
        super(TrumpetModelException, self).__init__(
            message
        )


class TrumpetModelDownloadException(TrumpetException):
    def __init__(self, name):
        message = f"""
            The {name} does not exist in the workspace model registry.
        """
        super(TrumpetModelDownloadException, self).__init__(
            message
        )

class TrumpetModelNotFoundException(TrumpetException):
    def __init__(self):
        message = f"""
        The model could not be found in the workspace and could not be loaded.
        """
        super(TrumpetModelNotFoundException, self).__init__(
            message
        )