import sys
import os

voting_data = list(open("voting_record_dump109.txt"))

def create_affiliation_dict():
    affiliation_dict = {}
    for row in voting_data:
      columns = row.split(' ')
      senator = columns[0]
      affiliation = columns[1]
      if affiliation in affiliation_dict:
        affiliation_dict[affiliation].append(senator)
      else:
        affiliation_dict[affiliation] = [senator]
    return affiliation_dict

## Task 1

def create_voting_dict():
    """
    Input: None (use voting_data above)
    Output: A dictionary that maps the last name of a senator
            to a list of numbers representing the senator's voting
            record.
    Example: 
        >>> create_voting_dict()['Clinton']
        [-1, 1, 1, 1, 0, 0, -1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1]

    This procedure should return a dictionary that maps the last name
    of a senator to a list of numbers representing that senator's
    voting record, using the list of strings from the dump file (strlist). You
    will need to use the built-in procedure int() to convert a string
    representation of an integer (e.g. '1') to the actual integer
    (e.g. 1).

    You can use the split() procedure to split each line of the
    strlist into a list; the first element of the list will be the senator's
    name, the second will be his/her party affiliation (R or D), the
    third will be his/her home state, and the remaining elements of
    the list will be that senator's voting record on a collection of bills.
    A "1" represents a 'yea' vote, a "-1" a 'nay', and a "0" an abstention.

    The lists for each senator should preserve the order listed in voting data. 
    """
    voting_dict = {}
    for row in voting_data:
      columns = row.split(' ')
      senator = columns[0]
      affiliation = columns[1]
      state = columns[2]
      record = [int(x) for x in columns[3:len(columns)]]
      voting_dict[senator] = record
    return voting_dict
    

## Task 2

def policy_compare(sen_a, sen_b, voting_dict):
    """
    Input: last names of sen_a and sen_b, and a voting dictionary mapping senator
           names to lists representing their voting records.
    Output: the dot-product (as a number) representing the degree of similarity
            between two senators' voting policies
    Example:
        >>> voting_dict = {'Fox-Epstein':[-1,-1,-1,1],'Ravella':[1,1,1,1]}
        >>> policy_compare('Fox-Epstein','Ravella', voting_dict)
        -2
    """
    u = voting_dict[sen_a]
    v = voting_dict[sen_b]
    return sum([u[i]*v[i] for i in range(len(u))])


## Task 3

def most_similar(sen, voting_dict):
    """
    Input: the last name of a senator, and a dictionary mapping senator names
           to lists representing their voting records.
    Output: the last name of the senator whose political mindset is most
            like the input senator (excluding, of course, the input senator
            him/herself). Resolve ties arbitrarily.
    Example:
        >>> vd = {'Klein': [1,1,1], 'Fox-Epstein': [1,-1,0], 'Ravella': [-1,0,0]}
        >>> most_similar('Klein', vd)
        'Fox-Epstein'

    Note that you can (and are encouraged to) re-use you policy_compare procedure.
    """
    senators = voting_dict.keys()
    likeness = []
    for comp_sen in senators:
      if comp_sen != sen:
        likeness.append((comp_sen, policy_compare(sen, comp_sen, voting_dict)))
    return sorted(likeness,key=lambda x: -x[1])[0][0]
    

## Task 4

def least_similar(sen, voting_dict):
    """
    Input: the last name of a senator, and a dictionary mapping senator names
           to lists representing their voting records.
    Output: the last name of the senator whose political mindset is least like the input
            senator.
    Example:
        >>> vd = {'Klein': [1,1,1], 'Fox-Epstein': [1,-1,0], 'Ravella': [-1,0,0]}
        >>> least_similar('Klein', vd)
        'Ravella'
    """
    senators = voting_dict.keys()
    likeness = []
    for comp_sen in senators:
      if comp_sen != sen:
        likeness.append((comp_sen, policy_compare(sen, comp_sen, voting_dict)))
    return sorted(likeness,key=lambda x: x[1])[0][0]
    
    

## Task 5

voting_dict = create_voting_dict()
most_like_chafee    = most_similar('Chafee',voting_dict)
least_like_santorum =  least_similar('Santorum',voting_dict)

# Task 6

def find_average_similarity(sen, sen_set, voting_dict):
    """
    Input: the name of a senator, a set of senator names, and a voting dictionary.
    Output: the average dot-product between sen and those in sen_set.
    Example:
        >>> vd = {'Klein': [1,1,1], 'Fox-Epstein': [1,-1,0], 'Ravella': [-1,0,0]}
        >>> find_average_similarity('Klein', {'Fox-Epstein','Ravella'}, vd)
        -0.5
    """
    likeness_list = []
    for comp_sen in sen_set:
      if comp_sen != sen:
        likeness_list.append(policy_compare(sen, comp_sen, voting_dict))
    return sum(likeness_list)/len(likeness_list)

democrats = create_affiliation_dict()['D']
dem_set = {sen for sen in democrats}

avg_sim_by_sen = []
for dem in dem_set:
  avg = find_average_similarity(dem,dem_set,voting_dict)
  avg_sim_by_sen.append((dem,avg))

most_average_Democrat = sorted(avg_sim_by_sen,key=lambda x: -x[1])[0][0] # give the last name (or code that computes the last name)

# Task 7

def find_average_record(sen_set, voting_dict):
    """
    Input: a set of last names, a voting dictionary
    Output: a vector containing the average components of the voting records
            of the senators in the input set
    Example: 
        >>> voting_dict = {'Klein': [-1,0,1], 'Fox-Epstein': [-1,-1,-1], 'Ravella': [0,0,1]}
        >>> find_average_record({'Fox-Epstein','Ravella'}, voting_dict)
        [-0.5, -0.5, 0.0]
    """
    sum_rec = []
    avg_rec = []
    for sen in sen_set:
      sen_rec = voting_dict[sen]
      if len(sum_rec) == 0:
        sum_rec = sen_rec
      else:
        sum_rec = [sum_rec[i]+sen_rec[i] for i in range(len(sen_rec))]
    avg_rec = [v/len(sen_set) for v in sum_rec]
    return avg_rec 

average_Democrat_record = find_average_record(dem_set, voting_dict) # (give the vector)

# Task 8

def bitter_rivals(voting_dict):
    """
    Input: a dictionary mapping senator names to lists representing
           their voting records
    Output: a tuple containing the two senators who most strongly
            disagree with one another.
    Example: 
        >>> voting_dict = {'Klein': [-1,0,1], 'Fox-Epstein': [-1,-1,-1], 'Ravella': [0,0,1]}
        >>> bitter_rivals(voting_dict)
        ('Fox-Epstein', 'Ravella')
    """
    comp_dict = {}
    senators = voting_dict.keys()
    for sen_a in senators:
      for sen_b in senators:
        if sen_a != sen_b:
          if (sen_b,sen_a) not in comp_dict:
            comp_dict[(sen_a,sen_b)] = policy_compare(sen_a, sen_b, voting_dict)

    #this is ugly
    comp_list = []
    for key in comp_dict:
      comp_list.append([key,comp_dict[key]])
    sorted_comp_list = sorted(comp_list, key = lambda x: x[1])

    return sorted_comp_list[0][0]

