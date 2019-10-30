def compare1(matched_counter, comment_counter, argument_counter):
    n_in_argument = sum(argument_counter.values())
    n_matches = sum(matched_counter.values())

    return n_matches / n_in_argument

def compare2(matched_counter, comment_counter, argument_counter):
    n_in_comment = sum(comment_counter.values())
    n_matches = sum(matched_counter.values())

    return n_matches / n_in_comment

def compare3(matched_counter, comment_counter, argument_counter):
    n_in_argument = sum(argument_counter.values())
    n_in_comment = sum(comment_counter.values())
    n_matches = sum(matched_counter.values())

    return n_matches / max(n_in_argument, n_in_comment)

def compare4(matched_counter, comment_counter, argument_counter):
    n_in_argument = sum(argument_counter.values())
    n_in_comment = sum(comment_counter.values())
    n_matches = sum(matched_counter.values())

    return n_matches / min(n_in_argument, n_in_comment)
