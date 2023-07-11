from fractions import Fraction

def addLabels(sigma, x_label, y_label):

	#Adds all the relevant labels to sigma

	#Add labels of type X(1,b) or X(a,0) or X(a,a)
	sigma += [a for a in x_label if a[1] == 1 or a[2] == 0 or a[1] == a[2]]

	#Add labels of type Y(1,b,c) or Y(a,0,c) or Y(a,a,c)
	sigma += [a for a in y_label if 1==a[1] or a[2]==0 or a[1]==a[2]]



def possibleMultiset(sigma, length, targetSet):
	# finds all multisets of elements in sigma of input length
	# and outputs it in targetSet 

	#Using the star and bar technique to come up with all the required multiset
	no_of_labels = len(sigma)
	count = [0]*no_of_labels

	for i in range(2**(no_of_labels + length - 1)):
		if i.bit_count() == no_of_labels-1:
			last_one = -1
			index = 0
			for j in range(no_of_labels + length - 1):
				if ( i & (1<<j) ) > 0:
					count[index] = j-last_one - 1
					last_one = j
					index += 1
			count[index] = no_of_labels + length - 1 - last_one - 1
			toadd = []
			for j in range(no_of_labels):
				for k in range(count[j]):
					toadd.append(sigma[j])
			targetSet.append(toadd)




def isActive1(config):
	sum_c= Fraction(0,1)
	exists_c = False
	valid = True

	for label in config:
		if label[0] == 'X':
			if label[1] != 1 or label[2] != 0:
				valid = False
		else:
			if label[1] != 1 or label[2] != 0:
				valid = False
			exists_c = True
			sum_c += label[3]

	if exists_c:
		valid = valid and (sum_c == 1)

	return valid


def isActive2(config):

	d=len(config)

	#Iterate for the index j
	for j in range(d):
		sum_c = Fraction(0,1)
		exists_c = False
		valid = True
		if config[j][2] != 0:
			continue

		sum_1 = config[j][1]
		sum_c = Fraction(0,1)

		#Iterate over all i given a j
		for i in range(d):
			if i == j:
				continue

			label = config[i]
			if label[0] == 'X':
				if label[1] != 1:
					valid = False
				else:
					sum_1 += label[2]

			else:
				exists_c = True
				sum_c += label[3]
				if label[1] != 1:
					valid = False
				else:
					sum_1 += label[2]

		if valid:
			if exists_c:
				if sum_1 == 1 and sum_c == 1:
					return True
			else:
				if sum_1 == 1:
					return True

	return False

def isActive3(config):
	sum_1=Fraction(0,1)
	sum_c= Fraction(0,1)
	exists_c = False
	valid = True
	for label in config:
		if label[0] == 'X':
			if label[1] != label[2]:
				valid = False
			else:
				sum_1 += label[1]
		else:
			if label[1] != label[2]:
				valid = False
			else:
				sum_1 += label[1]
			exists_c = True
			sum_c += label[3]

	if exists_c:
		valid = valid and (sum_c == 1) and (sum_1 == 1)
	else:
		valid = valid and (sum_1 == 1)
	return valid


def isPassive1(config):
	sum_a = Fraction(0,1)

	for label in config:
		sum_a += label[1]

	return (sum_a <= 1)

def isPassive2(config):
	sum_c = Fraction(0,1)
	sum_b = Fraction(0,1)
	for label in config:
		if label[0] == 'X':
			return False
		sum_c += label[3]
		sum_b += label[2]

	return (sum_c >= 1 and sum_b <= 1)

def isPassive3(config):
	
	d = len(config)

	for j in range(d):
		sum_1 = config[j][2]
		for i in range(d):
			if i != j:
				sum_1 += config[i][1]
		if(sum_1 <=1):
			return True

	return False

def printConfigs(active_config, passive_config, labelMap):

	f=open("configs-2.txt","w")

	f.write("Active configurations:\n\n")

	for config in active_config:
		for label in config:
			f.write(labelMap[label])
		f.write("\n")

	f.write("\n\nPassive configurations:\n\n")
	
	for config in passive_config:
		for label in config:
			f.write(labelMap[label])
		f.write("\n")

	f.close()



if __name__ == '__main__':

	# This code creates the problem Pi_2 discussed in my thesis for (act_deg, pass_deg)-biregular
	# tree. This can be fed in the round eliminator tool to understand the necessary complexity.

	#First, we will define all the variables that are used
	# n = fractional denominator, act_deg=active degree and pass_deg = passive degree
	n,act_deg,pass_deg = map(int,input().split())

	#Contains set of fractional value used
	values = [Fraction(i,n) for i in range(n+1)]

	#Create all labels of type X: X(a,b) with a >= b
	x_label = [ ('X',a,b) for a in values for b in values if a >= b]

	#Create all labels of type Y: Y(a,b,c) with a>=b and c>=b
	y_label = [('Y',a,b,c) for a in values for b in values for c in values if a >=b and c>=b]

	# sigma holds all the valid labels for the problem Pi_2
	sigma = []
	
	#list to store all multisets of length act_deg
	possible_active_multiset = []

	#list to store all multisets of length pass_deg
	possible_passive_multiset = []

	# set to store all active and passive configurations
	active_config = []
	passive_config = []
	
	#Add valid labels to sigma
	addLabels(sigma, x_label, y_label)

	#map labels in sigma to printable configurations
	labelMap={}
	indexCount=0
	for label in sigma:
			labelMap[label] = "(A" + str(indexCount) + ") "
			indexCount += 1

	#Create all possible multiset of len act_deg
	possibleMultiset(sigma, act_deg, possible_active_multiset)

	#Create all possible multiset of len pass_deg
	if(act_deg == pass_deg):
		possible_passive_multiset = possible_active_multiset
	else:
		possibleMultiset(sigma, pass_deg, possible_passive_multiset)

	for config in possible_active_multiset:
		if isActive1(config) or isActive2(config) or isActive3(config):
			active_config.append(config)

	for config in possible_passive_multiset:
		if isPassive1(config) or isPassive2(config) or isPassive3(config):
			passive_config.append(config)

	printConfigs(active_config, passive_config , labelMap)
		

	





