from fractions import Fraction




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
	sum_a = Fraction(0,1)
	

	for label in config:
		if label[0] != 'A':
			return False
		sum_a += label[1]

	return (sum_a == 1)


def isActive2(config):

	d=len(config)

	#Iterate for the index j
	for j in range(d):
		if(config[j][0] != 'B'):
			continue
		sum_ab = config[j][1]
		possible=True
		#Iterate over all i given a j
		for i in range(d):
			if i == j:
				continue
			label = config[i]
			if label[0] != 'A':
				possible=False
				break
			sum_ab += label[1]

		if possible and sum_ab == 1:
			return True

	return False

def isActive3(config):
	sum_d = Fraction(0,1)
	

	for label in config:
		if label[0] != 'D':
			return False
		sum_d += label[1]

	return (sum_d == 1)


def isPassive(config):
	a_exists = False
	sum_d = Fraction(0,1)
	total = Fraction(0,1)

	for label in config:
		if label[0]=='A':
			a_exists=True
		total += label[1]
		if(label[0] == 'D'):
			sum_d += label[1]

	if a_exists:
		return total >= 1 and sum_d <=1
	else:
		return sum_d <= 1

	



def printConfigs(active_config, passive_config):

	f=open("configs-1-relax.txt","w")

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
	n,act_deg,pass_deg = map(int,input("Enter three space seperated integers: ").split())
	values = [Fraction(i,n) for i in range(n+1)]

	
	a_label = [ ('A', x) for x in values]
	b_label = [('B',x) for x in values]
	d_label = [('D',x) for x in values]


	sigma = a_label + b_label + d_label
	possible_active_multiset = []
	possible_passive_multiset = []
	active_config = []
	passive_config = []

	#map labels in sigma to printable configurations
	labelMap={}
	indexCount=0
	for label in sigma:
			labelMap[label] = "(X" + str(indexCount) + ") "
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
		if isPassive(config):
			passive_config.append(config)

	printConfigs(active_config, passive_config)

	for label in sigma:
		print(label, labelMap[label])
		

	





