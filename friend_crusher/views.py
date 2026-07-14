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
        visual_mask = []
        pattern_string = '^'
        min_word_length = int(numbers[0])
        min_anchor_letter = 0
        max_anchor_letter = 0
        multiplier_list = []
        for i in range(0,int(numbers[0])):
            #print('letter'+str(i+1))
            anchor_letter = request.POST.get('letter'+str(i+1))
            multiplier = request.POST.get('multiplier'+str(i+1))
            print("Anchor letter[i]:", anchor_letter + "[" + str(i) + "]")
            anchor_letters_array.append(anchor_letter.lower())
            print("Multiplier:", multiplier)
            if multiplier == "1":
                multiplier_list.append("")
            else:
                multiplier_list.append(multiplier)
            if mask != "":
                mask += " "
            if multiplier == "1":
                mask += "_"
            else:
                mask += multiplier
            if anchor_letter == "":
                #mask += "_"
                pattern_string += '\w?'
                visual_mask.append("")
                '''
                
                
                
                NEED TO CODE FOR WHEN ITS \w and not \w? so that it can be a letter in the middle of the word.
                
                
                
                
                '''
            else:
                mask += anchor_letter.lower()
                
                pattern_string += '[' +anchor_letter.lower() + ']'
                visual_mask.append(anchor_letter.lower())
                if min_anchor_letter == 0:
                    min_anchor_letter = i+1
                max_anchor_letter = i+1
        pattern_string += '\Z'
        print("Mask:", mask)
        min_word_length = max_anchor_letter - min_anchor_letter + 1
        print("Min word length:", min_word_length)

        letters = np.array(list(playable_letters))
        print("Letters:", letters)
        anchor_letters = np.array(anchor_letters_array)
        print(" == > Anchor letters:", anchor_letters)

        words_list = trainboard.load_dictionary()
        weighted_alphabet = trainboard.load_weighted_alphabet()
        print("about to match words...")
        matched_words = trainboard.engage(letters,anchor_letters,numbers[0])
        #matched_words = trainboard.make_it_so_number_one(letters, anchor_letters, pattern_string, words_list)
        print("Matched words:", matched_words)
        
    
        prioritized_matching_words = trainboard.prioritize_matching_words(matched_words, weighted_alphabet)
        word_scores = []
        letter_values = []

        for word in prioritized_matching_words:
            letter_values = []
            word_formatted_for_display = []
            if len(word) >= min_word_length:
                
                for i in range(len(word)):
                    formatted_position = ""
                    letter = word[i]
                    letter_values.append(weighted_alphabet[letter])
                    if letter == visual_mask[i]:
                        formatted_position += "<td style=\"border: 1px solid black; background-color: #e5e2e2;\">" + letter
                    else:
                        formatted_position += "<td style=\"border: 1px solid black;\">" + letter
                    formatted_position += "<sub>" + str(weighted_alphabet[letter]) + "</sub>"+ "</td>"
                    word_formatted_for_display.append(formatted_position)
                score = trainboard.multiplier_word_score(word, mask)
                for i in range(len(word),int(numbers[0])):
                    word_formatted_for_display.append("<td style=\"border: 1px solid black;\">&nbsp;</td>")
                word_scores.append([word, word_formatted_for_display, score])
        
        word_scores.sort(key=lambda x: x[2], reverse=True)
        print("exit")
        print(word_scores)
        return render(request, 'crossplay.html', {'message': 'Play analysis complete.', 'status': 'success', 'matching_words': prioritized_matching_words, 'playable_letters': playable_letters, 'visual_mask': visual_mask, 'word_scores': word_scores, 'max_anchor_letter': max_anchor_letter, 'min_anchor_letter': min_anchor_letter, 'multiplier_list': multiplier_list, 'numbers': [2, 3, 4, 5, 6, 7, 8, 9, 10]})
    else:
        return render(request, 'crossplay.html', {'message': 'Hello Newman', 'numbers': [2, 3, 4, 5, 6, 7, 8, 9, 10]})