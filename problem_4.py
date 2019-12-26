class Group(object):
    def __init__(self, _name):
        self.name = _name
        self.groups = []
        self.users = []

    def add_group(self, group):
        self.groups.append(group)

    def add_user(self, user):
        self.users.append(user)

    def get_groups(self):
        return self.groups

    def get_users(self):
        return self.users

    def get_name(self):
        return self.name
    
    def has_groups(self):
        return len(self.groups) > 0
    
    def has_users(self):
        return len(self.users) > 0


parent = Group("parent")
child = Group("child")
sub_child = Group("subchild")

sub_child_user = "sub_child_user"
sub_child.add_user(sub_child_user)

sub_parent_user = "sub_parent_user"
sub_baby_user = "sub_baby_user"
sub_baby = Group("Baby")
sub_baby.add_user(sub_baby_user)
sub_child.add_group(sub_baby)
no_user = ""

child.add_group(sub_child)
parent.add_group(child)

def is_user_in_group(user, group):
    """
    Return True if user is in the group, False otherwise.

    Args:
      user(str): user name/id
      group(class:Group): group to check user membership against
    """
    if user == "" or user == None:
        print("No user to look for!")
        return False
    if not isinstance(group, Group):
        print("Not a group!")
        return False
    if group.has_users() is True:
        users = group.get_users()
        for i in range(len(users)):
            if user == users[i]:
                return True
    result = False
    if group.has_groups() is True:
        groups = group.get_groups()
        for i in range(len(groups)):
            result = is_user_in_group(user, groups[i])
            if result == True:
                break
    return result

# Test Case
# print(is_user_in_group(sub_child_user, parent))
# print(is_user_in_group(sub_parent_user, parent))
# print(is_user_in_group(sub_baby_user, parent))
# print(is_user_in_group(no_user , parent))
# print(is_user_in_group(None , parent))
# print(is_user_in_group(sub_child_user , sub_child_user))