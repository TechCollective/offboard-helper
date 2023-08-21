import pprint
import re  # noqa: F401
import six

from offboardhelper.models.jobslist import Jobslist
from offboardhelper.models.google_workspace import GoogleWorkspace

class Project(object):
    swagger_types = {
        'autotask_company_id': 'int',
        'company_name': 'str',
        'google_workspace': 'GoogleWorkspace',
        'ticket': 'str',
        'jobslist': 'Jobslist',
        'slack_channel_id': 'int',
        'config_folder': 'str',
        'project_folder': 'str'
    }

    def __init__(self, autotask_company_id = None, company_name = None, google_workspace = None, ticket = None, jobslist = None, slack_channel_id = None, config_folder = None, project_folder = None):
        self._company_name = None
        self._autotask_company_id = None
        self._google_workspace = None
        self._ticket = None
        self._jobslist = None
        self._slack_channel_id = None
        self._config_folder = None
        self._project_folder = None
        
        if company_name is not None:
            self.company_name = company_name
        if autotask_company_id is not None:
            self.autotask_company_id = autotask_company_id
        if google_workspace is not None:
            self.google_workspace = google_workspace
        if ticket is not None:
            self.ticket = ticket
        if jobslist is not None:
            self.jobslist = jobslist
        if slack_channel_id is not None:
            self.slack_channel_id = slack_channel_id
        if config_folder is not None:
            self.config_folder = config_folder
        if project_folder is not None:
            self.project_folder = project_folder

    @property
    def company_name(self):
        return self._company_name
    
    @company_name.setter
    def company_name(self, company_name):
        self._company_name = company_name

    @property
    def autotask_company_id(self):
        return self._autotask_company_id
    
    @autotask_company_id.setter
    def autotask_company_id(self, autotask_company_id):
        self._autotask_company_id = autotask_company_id

    @property
    def google_workspace(self):
        return self._google_workspace
    
    @google_workspace.setter
    def google_workspace(self, google_workspace):
        self._google_workspace = google_workspace

    @property
    def ticket(self):
        return self._ticket
    
    @ticket.setter
    def ticket(self, ticket):
        self._ticket = ticket

    @property
    def jobslist(self):
        return self._jobslist
    
    @jobslist.setter
    def jobslist(self, jobslist):
        self._jobslist = jobslist

    @property
    def slack_channel_id(self):
        return self._slack_channel_id
    
    @slack_channel_id.setter
    def slack_channel_id(self, slack_channel_id):
        self._slack_channel_id = slack_channel_id
        
    @property
    def config_folder(self):
        return self._config_folder
    @config_folder.setter
    def config_folder(self, config_folder):
        self._config_folder = config_folder

    @property
    def project_folder(self):
        return self._project_folder
    @project_folder.setter
    def project_folder(self, project_folder):
        self._project_folder = project_folder

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Project, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Project):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    