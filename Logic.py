from itertools import permutations, combinations

#To all the batches derived from each rule
all_batches= []
#Format Kitchen Coordinates
locs = {
    "K100": (100.5, 100.2),
    "K101": (100.4, 100.2),
    "K102": (100.5, 100.1),
    "C10": (100.7, 100.4),
    "C11": (102, 102.2),
    "C12": (102, 102.2),
}

#Format  OrderID,CustID,KitchenID,ReadyTime
orders = [[1, "C10", "K100", 705], [10, "C10", "K100", 710],
          [2, "C11", "K101", 725], [3, "C11", "K102", 604],
          [4, "C11", "K101", 730], [5, "C10", "K102", 800],
          [6, "C10", "K102", 845], [7, "C12", "K100", 600],
          [8, "C11", "K100", 730], [11, "C10", "K100", 735],
          [12, "C11", "K101", 900], [0, "C12", "K101", 903],
          [9, "C12", "K101", 902]
         ] 

#Defining Required Functions
def dis(a: list, b: list) -> int:
  dist = ((b[0] - a[0])**2 + (b[1] - a[1])**2)**(1 / 2)
  return round(float(dist), 2)

def all_combinations_with_orders(lst):
  all_combinations = []
  for r in range(1, len(lst)+1):
      for comb in combinations(lst, r):
          all_combinations.extend([list(perm) for perm in permutations(comb)])
  return all_combinations

#Generating Distance Matrix 
distances = []
k = []
for i in locs:
  k.append(i)
for i in range(len(k)):
  temp = []
  for j in range(len(k)):
    temp.append(dis(locs[k[i]], locs[k[j]]))
  distances.append(temp)
#Generating Time matrix with (1KM=7min)
time_matrix = []
for i in range(len(distances)):
  temp = []
  for j in range(len(distances[i])):
    temp.append(round(distances[i][j]*7,2))
  time_matrix.append(temp)

##################Rule1########################
# • Two orders - From the same kitchen.
# • To the same customer.
# • Ready at the same time (10 mins apart).
# • Assign the pick-up to the same rider.
#Sort with respect to Ready Time
sorted_orders = sorted(orders, key=lambda x: x[3])
batches = []
THRESHOLD = 10
i = 0
#Batching with Ready Time 10 mins apart
while i < len(sorted_orders):
  start = sorted_orders[i][3]
  batch = []
  j = 0
  while (abs(start - sorted_orders[i + j][3]) <= THRESHOLD):
    batch.append(sorted_orders[i + j])
    j = j + 1
    if (i + j) >= len(sorted_orders):
      break
  batches.append(batch)
  i = i + 1
#Batching Orders with respect to rule1
batch_by_rule_1 = []
for i in batches:
  if len(i) == 1:
    batch_by_rule_1.append(i)
  else:
    #Sort Each batch with respect to both Customer and Kitchen 
    ks = sorted(i, key=lambda x: (x[1], x[2]))
    temp = []
    temp.append(ks[0])
    for j in range(1, len(ks)):
      if ks[j - 1][2] == ks[j][2] and ks[j - 1][1] == ks[j][1]:
        temp.append(ks[j])
      else:
        if temp != []:
          batch_by_rule_1.append(temp)
          temp = []
          temp.append(ks[j])
    else:
      batch_by_rule_1.append(temp)
print("Batches by RULE1:")
for i in batch_by_rule_1:
  all_batches.append(i)
  print(i)
print("\n\n\n")
##################Rule2########################
# • Two orders.
# • From two different kitchens (1 km apart).
# • To the same customer.
# • Ready at the same time (10 mins apart).
# • Assign the pick-up to the same rider. 

#We use the same "batches" list which is Batching Orders with Ready Time 10 mins apart .
batch_by_rule_2 = []
for i in batches:
  if len(i) == 1:
    batch_by_rule_2.append(i)
  else:
    #Sort with respect to Customer for each i
    cs = sorted(i, key=lambda x: x[1])
    temp = []
    temp.append(cs[0])
    for j in range(1, len(cs)):
      if cs[j - 1][1] == cs[j][1]:
        k1 = k.index(cs[j - 1][2])
        k2 = k.index(cs[j][2])
        if (distances[k1][k2] <= 1):
          temp.append(cs[j])
      else:
        if temp != []:
          batch_by_rule_2.append(temp)
          temp = []
          temp.append(cs[j])

    else:
      batch_by_rule_2.append(temp)
print("Batches by RULE2:")
for i in batch_by_rule_2:
  all_batches.append(i)
  print(i)
print("\n\n\n")


##################Rule3########################
# • Two orders.
# • From the same kitchen.
# • To two different customers (1 km apart).
# • Ready at the same time (10 mins apart).
# • Assign the pick-up to the same rider. 

#We use the same "batches" list which is Batching Orders with Ready Time 10 mins apart .
batch_by_rule_3 = []
for i in batches:
  if len(i) == 1:
    batch_by_rule_3.append(i)
  else:
    #Sort with respect to Kitchen for each i
    ks = sorted(i, key=lambda x: x[2])
    temp = []
    temp.append(ks[0])
    for j in range(1, len(ks)):
      if ks[j - 1][2] == ks[j][2]:
        c1 = k.index(ks[j - 1][1])
        c2 = k.index(ks[j][1])
        if (distances[c1][c2] <= 1):
          temp.append(ks[j])
      else:
        if temp != []:
          batch_by_rule_3.append(temp)
          temp = []
          temp.append(ks[j])
    else:
      batch_by_rule_3.append(temp)

print("Batch by RULE3:")
for i in batch_by_rule_3:
  all_batches.append(i)
  print(i)


print("\n\n\n")

#Rule 4 and 5 same as Rule 2

##################Rule6########################
# • Two orders.
# • To the same customer.
# • 2nd kitchens pick up on the way to the customer.
# • Ready at the time the rider reaches the second kitchen (10 mins apart).
# • Assign the pick-up to the same rider. 
batch6 = []
#Sort by Customers
sorted_orders = sorted(orders, key=lambda x: x[1])
i = 0
#Batch with respect to customers
while i < len(sorted_orders):
  start = sorted_orders[i][1]
  batch = []
  j = 0
  while (start == sorted_orders[i + j][1]):
    batch.append(sorted_orders[i + j])
    j = j + 1
    if (i + j) >= len(sorted_orders):
      break
  batch6.append(batch)
  i = i + j
batch_by_rule_6 = []
for i in batch6:
  if len(i) == 1:
    batch_by_rule_6.append(i)
  else:
    #Sort by 
    ts = sorted(i, key=lambda x: (x[3]))
    temp = []
    temp.append(ts[0])
    start_time = ts[0][3]
    for j in range(1, len(ts)):
      k1 = ts[j - 1][2] 
      k2 = ts[j][2]
      t1 = k.index(k1)
      t2 = k.index(k2)
      l_range = ts[j][3] - THRESHOLD
      u_range = ts[j][3] + THRESHOLD
      if (l_range <= (start_time+time_matrix[t1][t2]) <=u_range):
        temp.append(ts[j])
        start_time = ts[j][3]
      else:
        if temp != []:
          batch_by_rule_6.append(temp)
          temp = []
          temp.append(ts[j])
          start_time = ts[j][3]
    else:
      batch_by_rule_6.append(temp)
      
print("Batch by RULE6:")
for i in batch_by_rule_6:
  all_batches.append(i)
  print(i)

print("\n\n\n")

#############Rule7###########
# • Two orders.
# • 2nd customers drop on the way to the 1st customer (Vice Versa).
# • 2nd kitchens pick up on the way to the customer.
# • Ready at the same time (10 mins apart or by the time rider reaches the kitchen).
# • Assign the pick-up to the same rider.

#Sort with Respect to Ready Time
sorted_orders = sorted(orders, key=lambda x: x[3])
batches = []
THRESHOLD = 35
i = 0
#Split with Ready Time Difference Threshold 
while i < len(sorted_orders):
  start = sorted_orders[i][3]
  batch = []
  j = 0
  while (abs(start - sorted_orders[i + j][3]) <= THRESHOLD):
    batch.append(sorted_orders[i + j])
    j = j + 1
    if (i + j) >= len(sorted_orders):
      break
  batches.append(batch)
  i = i + j

#Finding all combinations for each i
all_combi = []
for i in batches:
  result = all_combinations_with_orders(i)
  all_combi.extend(result)

#Maximum time than can be taken to deliver the order
MAX_TIME = 45
valid = []
THRESHOLD = 10

for i in all_combi:
  first_c = i[0][1]
  first_c_i = k.index(first_c)
  time = 0
  for j in range(1,len(i)):
    k1 = i[j-1][2] 
    k2 = i[j][2]
    t1=k.index(k1)
    t2=k.index(k2)
    check = time + time_matrix[t2][first_c_i] 
    if (abs(i[j][3] - (i[j-1][3]+ time_matrix[t1][t2])) <= THRESHOLD) and check<=MAX_TIME:
      time = time + time_matrix[t1][t2]
    else:
      break
  else:
      valid.append(i)  

print("Batch by RULE7:")
for i in valid:
  all_batches.append(i)
  print(i)
print("\n\n\n")

#############Rule8###########
# • Two orders.
# • From the same kitchen.
# • 2nd customers drop on the way to the customer 1st (Vice Versa).
# • Ready at the same time (10 mins apart).
# • Assign the pick-up to the same rider.

#Sort with Respect to Kitchen
batch8 = []
sorted_orders = sorted(orders, key=lambda x: x[2])
i = 0
MAX_TIME = 45
#Batching Each Kitchens Separately
while i < len(sorted_orders):
  start = sorted_orders[i][2]
  batch = []
  j = 0
  while (start == sorted_orders[i + j][2]):
    batch.append(sorted_orders[i + j])
    j = j + 1
    if (i + j) >= len(sorted_orders):
      break
  batch8.append(batch)
  i = i + j
#Batching according to rule 8
batch_by_rule_8 = []
for i in batch8:
  if len(i) == 1:
    batch_by_rule_8.append(i)
  else:
    #Sort with respect to Kitchen
    ks = sorted(i, key=lambda x: (x[3]))
    temp = []
    time = 0
    temp.append(ks[0])
    for j in range(1, len(ks)):
      c1 = k.index(ks[j-1][1])
      c2 = k.index(ks[j][1])
      time = time + abs(ks[j - 1][3]-ks[j][3]) + time_matrix[c1][c2]
      if abs(ks[j - 1][3]-ks[j][3])<= 10 and time<=MAX_TIME:
        temp.append(ks[j])
      else:
        if temp != []:
          batch_by_rule_8.append(temp)
          temp = []
          time = 0
          temp.append(ks[j])
    else:
      batch_by_rule_8.append(temp)

print("Batch by RULE8:")
for i in batch_by_rule_8:
  all_batches.append(i)
  print(i)
print("\n\n\n")

print(len(all_batches))

all_batches_with_len = sorted(all_batches, key=lambda x: len(x),reverse=True)



order_id = []
final = []
for i in all_batches_with_len:
  for j in i:
    if j[0] in order_id:
      break
  else:
    final.append(i)
    for j in i:
        order_id.append(j[0])
      

print("Number of Riders Required:",len(final))
print("Batching with least number of Riders:")
for i in final:
  print(i)

    
