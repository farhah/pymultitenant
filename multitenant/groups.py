

def objectify_group(attrs):
    group = GroupDescriptor(attrs)
    return group


def list_groups(attrs_dict):
    """user_dict = [{'raw_attrs': {}, 'attrs': {}, 'type': 'something'},
                                 {'raw_attrs': {}, 'attrs': {}, 'type': 'something'}, ..]
    """
    groups = list()
    for attrs in attrs_dict:
        group = objectify_group(attrs)
        groups.append(group)
    return groups


class GroupDescriptorMembers(object):

    def __init__(self, attrs):
        if attrs is None:
            return None
        self.attrs = attrs
    #
    # @property
    # def members(self):
    #     return self.attrs['member']


class GroupDescriptor(GroupDescriptorMembers):

    @property
    def name(self):
        name = self.attrs['dn'].split(',')[0].split('cn=')[1]
        return name

    @property
    def dn(self):
        return self.attrs['dn']



