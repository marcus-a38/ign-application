# extract queries from ./sqlite/queries/queries.sql

ABCDE = ["aaa", "bbb", "ccc", "ddd", "eee",]

# ABCDE[x] must be wrapped in brackets (as a list) to avoid bug with iterables in connections.py
# this is because this is an index rather than a list range, and you obviously can't iterate over a literal

def get_query_strings(filepath): # read queries.sql, grab each query as a substring of lines and declare number of values to insert

    file = open(filepath)
    content = file.readlines()

    add_user = r'\n'.join(content[2:4]).replace(r'\n', '')
    add_option = r'\n'.join(content[7:9]).replace(r'\n', '')
    add_poll = r'\n'.join(content[12:14]).replace(r'\n', '')
    add_vote = r'\n'.join(content[17:23]).replace(r'\n', '')
    rm_poll = r'\n'.join(content[26:32]).replace(r'\n', '')
    rm_vote = r'\n'.join(content[35:43]).replace(r'\n', '')
    get_user = r'\n'.join(content[46:49]).replace(r'\n', '')
    get_u_polls = r'\n'.join(content[52:55]).replace(r'\n', '')
    get_o_votes = r'\n'.join(content[58:61]).replace(r'\n', '')
    get_t_votes = r'\n'.join(content[64:66]).replace(r'\n', '')
    get_poll = r'\n'.join(content[69:72]).replace(r'\n', '')
    get_l_poll = r'\n'.join(content[75:77]).replace(r'\n', '')
    get_poll_ops = r'\n'.join(content[80:83]).replace(r'\n', '')
    get_u_vote = r'\n'.join(content[86:90]).replace(r'\n', '')
    delete_votes = r'\n'.join(content[93:95]).replace(r'\n', '')
    get_all_votes = r'\n'.join(content[98:101]).replace(r'\n', '')
    get_m_uid = r'\n'.join(content[104:106]).replace(r'\n', '')
    get_e_vote = r'\n'.join(content[109:113]).replace(r'\n', '')
    delete_acc = r'\n'.join(content[116:124]).replace(r'\n', '')

    # dictionary to map short key strings to queries.sql substring and total number of to-replace values

    query_dict = { 
        'add_user': (add_user, ABCDE[0:3]),
        'add_option': (add_option, ABCDE[0:3]),
        'add_poll': (add_poll, ABCDE[0:3]),
        'add_vote': (add_vote, ABCDE[0:3]),
        'rm_poll': (rm_poll, [ABCDE[0]]),
        'rm_vote': (rm_vote, ABCDE[0:3]),
        'get_user': (get_user, [ABCDE[0]]),
        'get_u_polls': (get_u_polls, [ABCDE[0]]),
        'get_o_votes': (get_o_votes, [ABCDE[0]]),
        'get_t_votes': (get_t_votes, [ABCDE[0]]),
        'get_poll': (get_poll, [ABCDE[0]]),
        'get_l_poll': (get_l_poll, None),
        'get_options': (get_poll_ops, [ABCDE[0]]),
        "get_votes": (get_u_vote, ABCDE[0:2]),
        "reset_votes": (delete_votes, [ABCDE[0]]),
        "get_all_votes": (get_all_votes, [ABCDE[0]]),
        "get_max_userid": (get_m_uid, None),
        "get_existing_vote": (get_e_vote, ABCDE[0:2]),
        "delete_acc": (delete_acc, [ABCDE[0]]),
    }

    return query_dict