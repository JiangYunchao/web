def main():
    f = open('tuples_train_posi', 'r')
    ftop = open('image_list_top', 'r')
    fbottom = open('image_list_bottom', 'r')
    fshoe = open('image_list_shoe', 'r')

    oft_list = f.readlines()
    top_list = ftop.readlines()
    bottom_list = fbottom.readlines()
    shoe_list = fshoe.readlines()

    new = open('111111111111', 'w')
    for n, oft in enumerate(oft_list):

        temp = oft.strip()
        oft = temp.split(',')

        user_id = oft[0]
        top_id = int(oft[1])
        bottom_id = int(oft[2])
        shoe_id = int(oft[3])

        top_name = top_list[top_id].strip()
        bottom_name = bottom_list[bottom_id].strip()
        shoe_name = shoe_list[shoe_id].strip()

        new.write(user_id + ',' + top_name + ',' + bottom_name + ',' + shoe_name + ',' + str(n))
    f.close()
    ftop.close()
    fbottom.close()
    fshoe.close()
    new.close()

if __name__ == "__main__":
    main()