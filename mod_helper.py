from tangle_ import TANGLE,Idempotent, Strands, Simple_Strand, StrandAlgebra
from utility import get_domain, get_range, generate_bijections, combinations, \
                get_domain_dict, get_range_dict, doescross_simple_rc,in_between_list, \
                reorganize_sign, reorganize_sign_2,dict_shift, get_start_dict, get_end_dict,\
                dict_shift_double, doescross_bool,generate_subset,from utility import in_between

def mod_helper(left_strand, right_strand):
    ''' Helper method used for dm, d+, d-.
    left_strands, right_strands, are coordinates.
    Given left_strands, and right strands, consists of strand pairs
    such as [((x_1, y_1),(x_2, y_2))....]
    
    Returns an dictionary object `types` whose value is a list of such 
    stair strands
    
    Option #1: left horizontal ( no cross)
    Option #2: left cross ( cross)
    Option #3: right horizontal strands ( no cross)
    Option #4: right cross( cross)
    Option #5: left below right
    Option #6: left above right
    '''    
    n = len(left_strand)
    m = len(right_strand)
    if not isinstance(left_strand, list):
        if isinstance(left_strand, tuple):
            left_strand = list(left_strand) 
        elif isinstance(left_strand, dict):
            left_strand = list(left_strand.items())
        else:
            raise TypeError("Something is wrong -- Not a list, dict, or tuple")
    if not isinstance(right_strand, list):
        if isinstance(right_strand, tuple):
            right_strand = list(right_strand)
        elif isinstance(right_strand, dict):
            right_strand = list(right_strand.items())
        else:
            raise TypeError("Something is wrong -- Not a list, dict, or tuple")
    types = {1:[],2:[],3:[],4:[],5:[],6:[]}
    #left half
    combin = generate_subset(n -1, 2)
    for combo in combin:
        strand_1 = left_strand[combo[0]]
        strand_2 = left_strand[combo[1]]
        if doescross_bool(strand_1, strand_2):
            types[2].append((strand_1, strand_2))
        else:
            types[1].append((strand_1, strand_2)) 
    #right_half
    combin = generate_subset(m-1, 2)
    for combo in combin:
        strand_1 = right_strand[combo[0]]
        strand_2 = right_strand[combo[1]]
        if doescross_bool(strand_1, strand_2):
            types[4].append((strand_1, strand_2))
        else:
            types[3].append((strand_1, strand_2))      
    # Calculate option#5 and #6
    combin = combinations(n-1,m-1) 
    for combo in combin:
        l_strand  = left_strand[combo[0]]
        r_strand = right_strand[combo[1]]
#        print("Comparison between {0} vs {1}:".format(l_strand, r_strand))
        if l_strand[1][1] < r_strand[0][1]: # left above right, Option 5
            types[5].append((l_strand,r_strand))
        else:
            if not l_strand[1][1] > r_strand[0][1]:
                raise TypeError("Something is wrong.")
            types[6].append((l_strand, r_strand))   
    return types

def mod_between(tangle, pair_left, pair_right, is_left):
    '''given a `tangle` coordinate pair ((x_1, y_1),(x_2, y_2)), 
    with any orientation left to right, tells us whether it hits up(1) down(-1) or middle (0). 
    if is_left is true:
        it means pair_right is the middle strand pair
    if is_right is true:
        it means pair_left is the middle strand pair.
    Assumes that the x coordinates line up well. return 2, if it doesn't even hit. '''
    
    t_1 = tangle[0]
    t_2 = tangle[1]
    if t_2[0] < t_1[0]:
        temp= t_1
        t_1 = t_2
        t_2 = temp      
    y_left_1 = pair_left[0][1]
    y_left_2 = pair_left[1][1]
    y_right_1 = pair_right[0][1]
    y_right_2 = pair_right[1][1]   
    if is_left:
        if in_between(y_right_1, y_right_2, t_2[1]):
            if in_between(y_left_1, y_left_2, t_1[1]): # Mod Relation 2
                return 0
            if t_1[1]> y_left_1 and t_1[1]> y_left_2:# Mod Relation 1
                return 1
            else:
                return -1 # Mod Relation 3
        else:
            return 2
    else:
        if in_between(y_left_1, y_left_2, t_1[1]):
            if in_between(y_right_1, y_right_2,t_2[1]): # Mod Relation 5
                return 0
            if t_2[1] > y_right_1 and t_2[1] > y_right_2:
                return 1
            else:
                return -1
        else:
            return 2
        
    

t_5= {(3,1):(3.5,2),(3,2):(3.5,1),(3.5,3):(3,3),(3,6):(3.5,6),(3.5,1):(4,1),\
       (3.5,2):(4,2),(4,3):(3.5,3),(3.5,6):(4,6), (4,4):(4,5)}

tang= TANGLE(t_5)
ss = Strands(tang, (((3,3),(1,0),(0,1)),((5,5),(4,6),(2,2))))
l_strands = ss.left_converted
r_strands = ss.right_converted
#l_strands = list(ss.left_converted.items())
#r_strands = list(ss.right_converted.items())
#print(l_strands)
#print(r_strands)
a = mod_helper(l_strands,r_strands)
for k in a.keys():
    print("++++++++++++ %s+++++++++++" %(k))
    print(a[k])
    if k==5:
        print(len(a[k]))
    print("++++++++++++++++ \n")
