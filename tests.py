import trainboard
import numpy as np

def test_word_matches(words_list):
    
    try:
        letters = np.array(['a','g','l','z','y','i'])
        anchor_letters = np.array(['a'])
        pattern_string = r"^\w?\w?\w[a]\Z"
        #pattern_string = "oo*A"
        #pattern = trainboard.build_pattern(pattern_string)
        matched_words = trainboard.make_it_so_number_one(letters, anchor_letters, pattern_string, words_list)

        assert 'gala' in matched_words, 'gala not in word list.'
        print('TEST PASSED: gala found in ' + str(matched_words) + ' for pattern ' + pattern_string)

        assert 'vwbeetle' not in matched_words, 'vwbeetle not in word list.'
        print('TEST PASSED: vwbeetle not found in ' + str(matched_words))

        letters = np.array(['a','m','l','z','o','i'])
        anchor_letters = np.array(['a','l'])
        matched_words = trainboard.make_it_so_number_one(letters, anchor_letters, r"^[a]\w[a]\w?\w?\Z", words_list)

        assert 'alamo' in matched_words, 'alamo not in word list.'
        print('TEST PASSED: alamo found in ' + str(matched_words))

        assert 'alamony' not in matched_words, 'alamony not in word list.'
        print('TEST PASSED: alamony not found in ' + str(matched_words))

    except AssertionError as assert_error:
        print('TEST FAILED: ' + str(assert_error))
        return False

    return True

def test_letter_scores(words_list):
    try:
        for word, expected_score in words_list:
            score = trainboard.word_score(word)
            assert score == expected_score, word + ' score returned ' + str(score) + ', expected ' + str(expected_score) +'.'
            print('TEST PASSED: ' + word + ' scored correctly.')


    except AssertionError as assert_error:
        print('TEST FAILED: ' + str(assert_error))
        return False

    return True

def test_grid_scores(words_list, grid_definition):
    try:
        for i in range(len(words_list)):
            word, expected_score = words_list[i]
            mask = grid_definition[i]
            score = trainboard.multiplier_word_score(word, mask)
            assert score == expected_score, word + ' score returned ' + str(score) + ', expected ' + str(expected_score) +'.'
            print('TEST PASSED: ' + word + ' scored correctly.')
    except AssertionError as assert_error:
        print('TEST FAILED: ' + str(assert_error))
        return False
    return True


if __name__ == '__main__': 
    words_list = trainboard.load_dictionary()
    weighted_alphabet = trainboard.load_weighted_alphabet()
    words_matched_status = test_word_matches(words_list)
    letters_scored_status = test_letter_scores([
        ['alpha',10],
        ['beta',7],
        ['yellow',15],
        ['spam',8],
        ['just',14]
        ])
    grid_scored_status = test_grid_scores([
        ['alpha',13],
        ['beta',7],
        ['yellow',45],
        ['justified',24],
        ['just',28]
        ],[
        '_ _ _ 2L _',
        '_ _ _ _',
        '_ 3W _ _ _ _',
        '_ _ _ _ 2L _ _ _ _',
        '_ 2W _ _'
        ])

    if words_matched_status and letters_scored_status and grid_scored_status:
        print('All Tests Passed for Module Trainboard')