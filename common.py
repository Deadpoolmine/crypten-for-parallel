ORIGINAL_DATA_PATH_PREFIX="./data/original/original-data"
USER_DATA_PATH_PREFIX="./data/user/user-data"
USER_SORTED_DATA_PATH_PREFIX="./data/user-sorted/user-sorted-data"

def build_fpath(uid=None, type="user"):
    if type == "original":
        return ORIGINAL_DATA_PATH_PREFIX
    elif type == "user":
        return USER_DATA_PATH_PREFIX + "-" + str(uid)
    elif type == "user-sorted":
        return USER_SORTED_DATA_PATH_PREFIX + "-" + str(uid)