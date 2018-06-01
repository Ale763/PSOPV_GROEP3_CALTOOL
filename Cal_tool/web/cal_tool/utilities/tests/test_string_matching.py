def function_eval_match():
    tests = [("event a", "event b", False),
             ("event 1", "evnet 2", False),
             ("event 1", "evnet 1", True),
             ("even t 1", "event 1", True),
             ("eventa", "event b", False),
             ("eventa", "event a", True),
             ("event 1", "event 2", False),
             ("event I", "event II", False),
             ("wisk I", "wsk I", True),
             ("wisk I", "wsk II", False),
             ('aaaaa', 'aabaa', True),
             ("Wiskunde voor Informatica I", "Wiskunde voor Informatica II", False),
             ("Wiskunde voor Informatica I", "Wiskunde Voor Informatica I", True),
             ("Wiskunde voor Informatica I", "Wiskunde Voor informatica I", True),
             ("Wiskunde voor Informatica I;/ Prof. dr. Joyhnny Daenen;/ Corda Campus;/ Voor groepen: A,B,C,D,E,F,G",
              "Wiskunde Voor informatica I;/ Prof. dr. Joyhnny Daenen;/ Corda Campus;/ Voor groepen: A,B,C,D,E,F,G", True),
             ("Wiskunde voor Informatica I;/ Prof. dr. Joyhnny Daenen;/ Corda Campus;/ Voor groepen: A,B,C,D,E,F,G",
              "Wiskunde voor Informatica I;/ Prof. dr. Joyhnny Daenen;/ Corda Campus;/ Voor groepen: A,B,C,D,E,F", True),
             ]
    max_diff = 0
    sum_diff = 0
    matching = modified_damerau_levenshtein_strategy()
    for pair in tests:
        print("Testing: ({0}, {1})".format(pair[0], pair[1]))
        start = time.time()
        match_result = matching.match(pair[0], pair[1])
        stop = time.time()
        diff = stop-start
        if(diff>max_diff):
            max_diff = diff
        sum_diff += diff
        print("\tTime needed: {0} s".format(diff))

        print("\tMatch result: {0} (Expected: {1})".format(match_result, pair[2]))
        if match_result == pair[2]:
            print("\tUnit test: PASSED")
        else:
            print("\tUnit test: FAILED")

    print("Max time needed {0}".format(max_diff))
    print("Total amount of time needed {0}".format(sum_diff))
    return (sum_diff)


# function_eval_match()

from cal_tool.utilities.fuzzy_string_matching import modified_damerau_levenshtein_strategy
import time