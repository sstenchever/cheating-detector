import gather_responses
import requests
from datetime import datetime

# Create function to compare student responses to online search results. If match is found, mark for possible cheating.
def compare_to_online_search(student_responses):        

    responses_matching_online_search = []
    headers = {
        # Set x-rapidapi-key to the string value of your API key
        "x-rapidapi-key": "<YOUR API KEY for https://rapidapi.com/apigeek/api/google-search3>",
        "x-rapidapi-host": "google-search3.p.rapidapi.com",
        "h1": "en"
    }

    for key, value in student_responses.items():
        for student_response in value:
            query = student_response.replace(' ', '+')
            URL = f"https://google-search3.p.rapidapi.com/api/v1/search/q={query}"
            resp = requests.get(URL, headers=headers)
            resp_json = resp.json()
            if resp.status_code == 200:
                for values in resp_json["results"]:
                    result_descriptions = []
                    result_descriptions.append(values["description"])
                    for search_string in result_descriptions:
                        if search_string.find(student_response) != -1:
                            responses_matching_online_search.append(f"Found student {key}'s response of: \"{student_response}\" in online search result")
                            # print (f"Found student {key}'s response of: \"{student_response}\" in online search result")
                        # else:
                        #     print("Student response not found in online search result")
            else:
                print("There was an error retrieving the search results")
                return -1
    if responses_matching_online_search == []:
        print ("Did not find any student responses that matched online search results")
        return -1
    return responses_matching_online_search
    

def compare_student_responses(student_responses):

    # New dictionary to store the alike responses where keys are the index of the question number and the values
    # are a list of the students who had matching answers for that question
    alike_responses = {}
    num_of_keys = len(student_responses)
    # Start first loop to track responses for Student A
    for first_key in student_responses.keys():
        if num_of_keys < 2:
            # Not enough student responses to compare
            break
        if student_responses[first_key][0] == []:
            # If there are no responses for a question, skip this iteration
            continue

        num_of_values = len(student_responses[first_key])
        counter = 0

        while (counter < num_of_values):
            # Start the second loop to compare responses for Student A to all other student responses
            for second_key, values in student_responses.items():
                if first_key == second_key:
                    # Don't compare two responses from the same student
                    continue
                # Loop through values of Student B to do comparisons to Student A's responses
                for value in values:
                    # Don't compare responses for different questions
                    if student_responses[first_key].index(student_responses[first_key][counter]) != values.index(value):
                        # print("Dont compare")
                        continue
                    if student_responses[first_key][counter] == value:
                        # print("We have a match!")

                        # If alike_responses is empty, populate it with index of question and values of first_key (student emails) and second_key
                        if alike_responses == {}:
                            alike_responses[str(values.index(value))] = [first_key, second_key]
                        # Else if the index of question is in alike_responses, check to see if first_key or second_key values 
                        # are not added to list of values for that question index. If they aren't, append them to that list
                        elif str(values.index(value)) in alike_responses.keys():
                            if first_key not in alike_responses[str(values.index(value))]:
                                alike_responses[str(values.index(value))].append(first_key)
                            if second_key not in alike_responses[str(values.index(value))]:
                                alike_responses[str(values.index(value))].append(second_key)
                        else:
                            alike_responses[str(values.index(value))] = [first_key, second_key]
            counter += 1
    
    if alike_responses == {}:
        print ("Did not find any alike student responses")
        return -1
    else:
        return "The following students had alike responses on the correlated questions (0) being 1:" + "\n" + str(alike_responses) + "\n"

def write_results_to_file(check_compare_student_responses, check_compare_to_online_search):
    # Check to see if responses matched other student responses or online searches
    if check_compare_student_responses == -1:
        no_alike_student_responses = True
    else:
        no_alike_student_responses = False
    if check_compare_to_online_search == -1:
        no_alike_responses_for_online_search = True
    else:
        no_alike_responses_for_online_search = False

    now = datetime.now()
    date_string = str(now)
    
    with open("cheating_detector_output.txt", "w+") as fd:
        fd.write("Cheating detector - Ran at " + date_string + "\n\n")
        fd.write("Alike student responses:\n")
        if no_alike_student_responses == True:
            fd.write("No alike student responses found!\n")
        else:
            fd.write(check_compare_student_responses)
        
        fd.write("\nStudent responses that match online searches:\n")
        if no_alike_responses_for_online_search == True:
            fd.write("No student responses matched online searches!")
        else:
            for item in check_compare_to_online_search:
                fd.write(item+"\n")

def main():
    # Creates the spreadsheet object 'sheet'
    sheet = gather_responses.setup()
    # Returns student responses in a dictionary where keys are student emails and values are lists of responses for that student
    student_responses = gather_responses.getStudentResponses(sheet)
    # Returns a string which contains all students who had alike responses. Returns -1 if there were no alike responses
    check_compare_student_responses = compare_student_responses(student_responses)
    # Returns a list of student responses that matched an online search. Returns -1 if there is an error checking results or if no responses match an online search
    check_compare_to_online_search = compare_to_online_search(student_responses)
    # Write the results to a file name
    write_results_to_file(check_compare_student_responses, check_compare_to_online_search)

if __name__ == '__main__':
    main()
