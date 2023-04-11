def generate(cord_xyz, i):
    print(cord_xyz, i)
    old_cord = list(cord_xyz)
    new_cord_1 = [cord_xyz[0] + 1, cord_xyz[1], cord_xyz[2]]
    new_cord_2 = [cord_xyz[0] - 1, cord_xyz[1], cord_xyz[2]]
    new_cord_3 = [cord_xyz[0], cord_xyz[1] + 1, cord_xyz[2]]
    new_cord_4 = [cord_xyz[0], cord_xyz[1] - 1, cord_xyz[2]]
    new_cord_5 = [cord_xyz[0], cord_xyz[1], cord_xyz[2] + 1]
    new_cord_6 = [cord_xyz[0], cord_xyz[1], cord_xyz[2] - 1]
    cord_array = []
    if sum(new_cord_1) > sum(old_cord):
        cord_array.append(new_cord_1)
    if sum(new_cord_2) > sum(old_cord):
        cord_array.append(new_cord_2)
    if sum(new_cord_3) > sum(old_cord):
        cord_array.append(new_cord_3)
    if sum(new_cord_4) > sum(old_cord):
        cord_array.append(new_cord_4)
    if sum(new_cord_5) > sum(old_cord):
        cord_array.append(new_cord_5)
    if sum(new_cord_6) > sum(old_cord):
        cord_array.append(new_cord_6)
    return cord_array, i + 1


def generate_2(size):
    cord_array = [[0, 0, 0]]
    i = 0
    while i < size:
        for j in range(i+1):
            if i!=0:
                cord, i = generate(cord_array[i][j], i)
            else:
                cord, i = generate(cord_array[i], i)
            for q in cord:
                cord_array.append(cord)
    return cord_array

print(generate_2(4))