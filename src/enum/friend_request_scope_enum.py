from enum import Enum


class FriendRequestScope(Enum):
    all = 'all'
    id_search = 'id_search'
    reject = 'reject'