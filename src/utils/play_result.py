play_results = [
    'full_perfect',
    'full_combo',
    'clear',
    'not_clear'
]

def compare_play_result_gt(r1, r2):
    i1 = play_results.index(r1)
    i2 = play_results.index(r2)
    return r1 if i1 < i2 else r2