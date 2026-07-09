import json
from django.http import JsonResponse
from django.shortcuts import render
import trainboard
from django.views.decorators.csrf import csrf_exempt
import numpy as np

@csrf_exempt
def crossplay(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Process the data as needed
        return JsonResponse({'status': 'success', 'data': data})
    else:
        #return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
        return render(request, 'crossplay.html', {'message': 'Play below', 'numbers': [2, 3, 4, 5, 6, 7, 8, 9, 10]})

def word_options(request):
    if request.method == 'POST':
        numbers = request.POST.getlist('selected_letter')
        print("Selected letters:", numbers[0])
        playable_letters = request.POST.get('playable_letters').lower()
        print("Playable letters:", playable_letters)
        anchor_letters_array = []
        mask = ""
        pattern_string = '^'
        for i in range(0,int(numbers[0])):
            #print('letter'+str(i+1))
            anchor_letter = request.POST.get('letter'+str(i+1))
            multiplier = request.POST.get('multiplier'+str(i+1))
            print("Anchor letter:", anchor_letter)
            print("Multiplier:", multiplier)
            if mask != "":
                mask += " "
            if multiplier == "1":
                mask += "_"
            else:
                mask += multiplier
            if anchor_letter == "":
                #mask += "_"
                pattern_string += '\w?'
            else:
                #mask += anchor_letter.lower()
                anchor_letters_array.append(anchor_letter.lower())
                pattern_string += '[' +anchor_letter.lower() + ']'
        pattern_string += '\Z'
        print("Mask:", mask)

        letters = np.array(list(playable_letters))
        print("Letters:", letters)
        anchor_letters = np.array(anchor_letters_array)
        print("Anchor letters:", anchor_letters)

        words_list = trainboard.load_dictionary()
        weighted_alphabet = trainboard.load_weighted_alphabet()
        matched_words = trainboard.make_it_so_number_one(letters, anchor_letters, pattern_string, words_list)
        print("Matched words:", matched_words)
        
    
        prioritized_matching_words = trainboard.prioritize_matching_words(matched_words, weighted_alphabet)
        word_scores = []
        
        for word in prioritized_matching_words:
            score = trainboard.multiplier_word_score(word, mask)
            print("Word: " + word + ", Score: " + str(score))
            word_scores.append([word, score])
        
        #prioritized_matching_words = ['a', 'b', 'c', 'd', 'e']  # Placeholder for the actual prioritized matching words
        return render(request, 'crossplay.html', {'message': 'Play analysis complete.', 'status': 'success', 'matching_words': prioritized_matching_words, 'playable_letters': playable_letters, 'word_scores': word_scores, 'numbers': [2, 3, 4, 5, 6, 7, 8, 9, 10]})
    else:
        return render(request, 'crossplay.html', {'message': 'Hello Newman', 'numbers': [2, 3, 4, 5, 6, 7, 8, 9, 10]})