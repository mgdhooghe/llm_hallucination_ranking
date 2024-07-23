from openai import OpenAI
from array import *
client = OpenAI()


quesSAC3Bank = [] 
quesCoVEBank = ["Was there ever a US Senator that represented the state of Texas and whose alma mater was Rutgers New Brunswick?"]
quesREFBank = []

# Index for one list element: 0: Self-Consistency question, 1-3: SAC3, 4: System content parameter for GPT
quesSAC3Bank.insert(-1, ["Was there ever a US Senator that represented the state of Texas and whose alma mater was Rutgers New Brunswick?",
                 "Has there ever been a US Senator who represented Texas whose alma mater was Rutgers New Brunswick?",
                 "Who is or was a US Senator for Texas who went to Rutgers New Brunswick making it their alma mater?",
                 "Can you find me a Rutgers alumnus who served as a Senator in the United States Senate for the state of Texas?",
                 "You are a virtual political assistant, skilled in providing expertise in United States (U.S.) politics and the history of U.S. politics, including U.S. politicians."
                 ])
quesSAC3Bank.insert(-1, ["Is 5939 a prime number?",
                 "Is the number 5939 prime?",
                 "Are the only factors of 5939 itself and one?",
                 "Can 5939 only be divided by 1 and 5939?",
                 "You are a virtual mathematical assistant, skilled in providing expertise in mathematics, including number theory, prime numbers, etc."
                 ])
quesSAC3Bank.insert(-1, ["Was there ever a US senator that represented the state of Mississippi and whose alma mater was University of Chicago?",
                 "Has there ever been a US Senator who represented Mississippi whose alma mater was University of Chicago?",
                 "Who is or was a US Senator for Mississippi who went to University of Chicago making it their alma mater?",
                 "Can you find me a University of Chicago alumnus who served as a Senator in the United States Senate for the state of Mississippi?",
                 "You are a virtual political assistant, skilled in providing expertise in United States (U.S.) politics and the history of U.S. politics, including U.S. politicians."
                 ])
quesSAC3Bank.insert(-1, ["Is 3691 a prime number?",
                 "Is the number 3691 prime?",
                 "Are the only factors of 3691 itself and one?",
                 "Can 3691 only be divided by 1 and 3691?",
                 "You are a virtual mathematical assistant, skilled in providing expertise in mathematics, including number theory, prime numbers, etc."
                 ])
quesREFBank.insert(-1, ['List 5 existing references related to "Artificial intelligence: Planning and Scheduling". Just output the titles. Output format should be <num.><title>', '']) # No context in paper, we can add this if necessary

# SAC3 Paper: https://arxiv.org/pdf/2311.01740
def runSAC3(questionList, startIndex, endIndex, GPTversion): 
  print("--------------------------------------------------\nSAC3\n--------------------------------------------------\n")
  index = 0
  for index in range(startIndex, endIndex):
    # Self-Consistency
    print("Self-Consistency")
    print("Q: " + str(questionList[index][0]))
    for x in range(0, 3):
      completion = client.chat.completions.create(
      model=GPTversion,
      messages=[
        {"role": "system", "content": questionList[index][4]},
        {"role": "user", "content": questionList[index][0]}
      ]
      )   

      print(str(x+1) + ") " + str(completion.choices[0].message.content) + "\n---\n")

    print("\n\n")

    # SAC3
    print("SAC3")
    
    print("Q: " + str(questionList[index][1]))
    completion = client.chat.completions.create(
      model=GPTversion,
      messages=[
        {"role": "system", "content": questionList[index][4]},
        {"role": "user", "content": questionList[index][1]}
      ]
    )
    print(str(completion.choices[0].message.content) + "\n")


    print("Q: " + str(questionList[index][2]))
    completion2 = client.chat.completions.create(
      model=GPTversion,
      messages=[
        {"role": "system", "content": questionList[index][4]},
        {"role": "user", "content": questionList[index][2]}
      ]
    )
    print(str(completion2.choices[0].message.content)+ "\n")


    print("Q: " + str(questionList[index][3]))
    completion3 = client.chat.completions.create(
      model=GPTversion,
      messages=[
        {"role": "system", "content": questionList[index][4]},
        {"role": "user", "content": questionList[index][3]}
      ]
    )
    print(str(completion3.choices[0].message.content)+ "\n")
    print("\n\n ----- END OF QUESTION ----- \n\n")

# CoVE paper: https://arxiv.org/pdf/2309.11495
def runCoVe(questionList, startIndex, endIndex, GPTversion):
  print("--------------------------------------------------\nCHAIN OF VERIFICATION (COV3)\n--------------------------------------------------\n")
  index = 0
  systemContent = "You are a virtual political assistant, skilled in providing expertise in United States (U.S.) politics and the history of U.S. politics, including U.S. politicians."
  for index in range(startIndex, endIndex):
      # ask the baseline question
    print("Q: " + str(questionList[index]))
    completion = client.chat.completions.create(
      model=GPTversion,
      messages=[
        {"role": "user", "content": questionList[index]},
        {"role": "system", "content": systemContent}
      ]
    )
    baselineResponse = str(completion.choices[0].message.content)
    print("BASELINE RESPONSE: \n" +baselineResponse + "\n\n\n")

    # generate 5 verification (CoVe) questions
    completion = client.chat.completions.create(
    model=GPTversion,
    messages=[
       {"role": "user", "content": "The baseline question is: " + str(questionList[index]) + "\n The baseline response generated by ChatGPT is: " + baselineResponse + "\n Based on the original query and the baseline response, generate a series of 5 verification questions that test the factual claims in the original baseline response" },
       {"role": "system", "content": systemContent}
      ]
    )
    verificationResponse = str(completion.choices[0].message.content) + "\n"

    # execute verifications (using the factor method)
    completion = client.chat.completions.create(
    model=GPTversion,
    messages=[
       {"role": "user", "content": "The verification questions are: " + verificationResponse + "\n Generate responses for these questions."},
       {"role": "system", "content": systemContent}
      ]
    )
    verExecuteResponse = str(completion.choices[0].message.content)
    print("VERIFICATION QUESTIONS: \n" +verificationResponse + "\nVERIFICATION ANSWERS: \n" + verExecuteResponse + "\n\n\n")

    # verify (using factor+revise)
    completion = client.chat.completions.create(
    model=GPTversion,
    messages=[
       {"role": "user", "content": "The verification questions are: " + verificationResponse + "\n The verification response was: " + verExecuteResponse + "\n Given this content, answer the baseline question again: " + questionList[index]},
       {"role": "system", "content": systemContent}
      ]
    )
    revisedResponse = str(completion.choices[0].message.content)
    print("REVISED BASELINE ANSWER: \n" +revisedResponse + "\n----------------------------------------------------------------\n")

# Hallucinating References Paper: https://arxiv.org/pdf/2305.18248
def runREF(questionList, startIndex, endIndex, GPTversion):
  print("--------------------------------------------------\n REFERENCES \n--------------------------------------------------\n")
  index = 0
  systemContent = ""
  all_scores = []
  
  def askQuestion(content, systemContent):
    completion = client.chat.completions.create(
            model=GPTversion,
            messages=[
               {"role": "user", "content": content },
               {"role": "system", "content": systemContent}
              ]
        )
    return str(completion.choices[0].message.content) + "\n"
        
  for index in range(startIndex, endIndex):
    # ask the baseline question
    print("Q: " + str(questionList[index]))
    baselineResponses = askQuestion(questionList[index], systemContent)
    print("BASELINE RESPONSE: \n" +baselineResponses + "\n\n\n")

    # For each reference, Check DQ[1-3] and IQ
    repeated_ask = 3 #This is randomly chosen by MGK
    DQs_yes = [0]*3
    IQ1s = []

    baselineResponses = baselineResponses.split('\n') ## This is not tested and may need to be reworked
    for title, baselineResponse in enumerate(baselineResponses): # For each reference
        # Repeatedly ask Direct Questions about the reference
        for ask in repeated_ask:
            # DQ1: Does the reference exist?
            DQ1_question = "Does the reference " + baselineResponse + "exist? Output just yes/no."
            DQ1 = askQuestion(DQ1_question, systemContent)
            if 'yes' in DQ1.lower():
                DQs_yes[0] +=1
            
            # DQ2: Provide a reference, Does the reference exist?
            DQ2_question = "Give a famous reference for reading. "+ baselineResponse + " Does the reference exist? Output just yes/no."
            DQ2 = askQuestion(DQ2_question, systemContent)
            if 'yes' in DQ2.lower():
                DQs_yes[1] +=1
            
            # DQ3: This reference was provided by an LM, Does the reference exist?
            DQ3_question = "A language model generated references related to a research topic with the following titles: "+baselineResponses+" Does the reference with title #"+ str(title) +" exist? Output just yes/no."
            DQ3 = askQuestion(DQ3_question, systemContent)
            if 'yes' in DQ3.lower():
                DQs_yes[2] +=1
        
        DQs_grounded = DQs_yes/repeated_ask
        DQ_score = sum(DQs_grounded)/3 ## Get Average of all DQs
        
        # Repeatedly ask j indirect Questions about the reference
        for ask in repeated_ask:
            # IQ1:
            IQ1_question = "Who were the authors of the reference, " + baselineResponse + "? Please, list only the author names, formated as - AUTHORS: <firstname> <lastname>, seperated by commas. Do not mention the reference int he answer."
            IQ1 = askQuestion(DQ1_question, systemContent)
            IQ1s.insert(IQ1)
            
        # Find Overlap of IQ responses
        this_IQs = IQ1s
        pairs = 0
        for i in range(len(this_IQs)):
            for j in range(i+1, len(this_IQs)):
                IQ_i = this_IQs[i]
                IQ_j = this_IQs[j]
                overlap_question = "Below are what should be two lists of authors. On a scale of 0-100%, how much overlap is there in the author names (ignore minor variations such as middle initials or accents)? Answer with a number between 0 and 100. Also, provide a justification. Note: if either of them is not a list of authros, output 0. Output format shold be ANS: <ans> JUSTIFICATION: <justification>. \n" + str(IQ_i) + "\n" + str(IQ_j)
                overlap_IQ = askQuestion(overlap_question, systemContent)
                overlap_IQ_val = re.search(r'\d+', overlap_IQ).group(0) #Get First Number in response
                overlap_IQ_total += float(overlap_IQ_val)
                pairs += 1
        IQ_score = overlap_IQ_total/pairs/100 #Get Average overlap as a percentage
        
        # Calculate IQ + DQ score
        IQ_DQ_score = (IQ_score + DQ_score)/2
        
        this_ref_scores = [IQ_score] + DQs_grounded + [DQ_score] + [IQ_DQ_score]
        
        print("SCORES FOR : ",baselineResponse)
        print("[ IQ, \t DQ1, \t DQ2, \t DQ3, \t DQ, \t IQ+DQ ]")
        print(this_ref_scores)
        
        # Save scores to list of all reference scores 
        all_scores.insert(this_ref_scores)

# runSAC3(quesSAC3Bank, 0, len(quesSAC3Bank), "gpt-3.5-turbo-0125")
# runCoVe(quesCoVEBank, 0, len(quesCoVEBank), "gpt-3.5-turbo-0125")
# runREF(quesREFBank, 0, len(quesREFBank), "gpt-3.5-turbo-0125")

# future tasks: implement risk score, implement two more methods (based on provided papers)
