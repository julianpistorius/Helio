from controller_exceptions import UnattachedControllerError


class BaseViewController(object):
    def __init__(self):
        self._named_children = {}
        self._indexed_children = []
        self._view_state = None

        self._local_id = None
        self.parent = None
        self.is_root = False

    @property
    def local_id(self):
        return self._local_id if self._local_id else 'page'

    @local_id.setter
    def local_id(self, new_id):
        self._local_id = new_id

    @property
    def path(self):
        if self.parent:
            return '{0}.{1}'.format(self.parent.path, self.local_id)
        elif self.is_root:
            return self.local_id

        raise UnattachedControllerError("Cannot retrieve a path for an unattached controller.")

    @property
    def view_state(self):
        return self.parent.view_state if self.parent else self._view_state

    def make_root(self, view_state):
        self._view_state = view_state
        self.is_root = True
        self._post_attach()

    def attach(self, parent, local_id):
        self.parent = parent
        self.local_id = local_id

    def set_named_child(self, child_key, child):
        if child_key in self._named_children and len(self._named_children[child_key]):
            replaced_child = self._named_children[child_key][-1]
            replaced_child._pre_detach()
        else:
            replaced_child = None

        self._named_children[child_key] = [child]
        child.attach(self, child_key)

        if replaced_child:
            replaced_child._post_detach()

        child._post_attach()

    def get_named_child(self, child_key):
        return self._named_children[child_key][-1]

    def push_named_child(self, child_key, child):
        if not child_key in self._named_children:
            self._named_children[child_key] = []
            replaced_child = None
        else:
            replaced_child = self._named_children[child_key][-1]
            replaced_child._pre_detach()

        self._named_children[child_key].append(child)
        child.attach(self, child_key)

        if replaced_child:
            replaced_child._post_detach()

        child._post_attach()

    def pop_named_child(self, child_key):
        final_child = self._named_children[child_key].pop(-1)
        final_child._pre_detach()
        final_child._post_detach()

        if self._named_children[child_key]:
            self._named_children[child_key][-1].attach(self, child_key)
            self._named_children[child_key][-1]._post_attach()

        return final_child

    def _post_attach(self):
        self.post_attach()

    def _pre_detach(self):
        self.pre_detach()

    def _post_detach(self):
        self.parent = None
        self.post_detach()

    # Controllers should override the following methods, as appropriate

    def post_attach(self):
        pass

    def pre_detach(self):
        pass

    def post_detach(self):
        pass
