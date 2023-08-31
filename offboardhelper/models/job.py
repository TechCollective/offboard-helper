import pprint
import re  # noqa: F401
import six

# FIXME ether get rid of estimated_size and messages are use them
class Job(object):
    swagger_types = {
        'source_email': 'str',
        'distination_archive': 'str',
        'distination_group': 'str',
        'distination_user': 'str',
        'estimated_size': 'str', # Size of the Inbox
        'messages': 'str' # Number of emails
    }

    def __init__(self, source_email=None, distination_archive=None, distination_group=None, distination_user=None, estimated_size=None, messages=None):
        self._source_email = None
        self._distination_archive = None
        self._distination_group = None
        self._distination_user = None
        self._estimated_size = None
        self._messages = None
        
        if source_email is not None:
            self.source_email = source_email
        if distination_archive is not None:
            self.distination_archive = distination_archive
        if distination_group is not None:
            self.distination_group = distination_group
        if distination_user is not None:
            self.distination_user = distination_user

    @property
    def source_email(self):
        return self._source_email
    @source_email.setter
    def source_email(self, source_email):
        self._source_email = source_email

    @property
    def distination_archive(self):
        return self._distination_archive
    @distination_archive.setter
    def distination_archive(self, distination_archive):
        self._distination_archive = distination_archive

    @property
    def distination_group(self):
        return self._distination_group
    @distination_group.setter
    def distination_group(self, distination_group):
        self._distination_group = distination_group

    @property
    def distination_user(self):
        return self._distination_user
    @distination_user.setter
    def distination_user(self, distination_user):
        self._distination_user = distination_user
    
    @property
    def estimated_size(self):
        return self._estimated_size
    @estimated_size.setter
    def estimated_size(self, estimated_size):
        self._estimated_size = estimated_size

    @property
    def messages(self):
        return self._messages
    @messages.setter
    def messages(self, messages):
        self._messages = messages
        
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
        if issubclass(Job, dict):
            for key, value in self.items():
                result[key] = value
        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def from_tinydb(self, job):
        self.source_email = job['source_email']
        self.distination_archive = job['distination_archive']
        self.distination_group = job['distination_group']
        self.distination_user = job['distination_user']
        self.estimated_size = job['estimated_size']
        self.messages = job['messages']
        return self



    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()