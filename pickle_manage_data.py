import pickle


def load_data(file_Name):
    """ load an object from a file using pickle """
    
    with open(file_Name, 'rb') as file:
        obj = pickle.load(file)
    print( "Object Extracted: {}".format(obj) )    
    return obj 


def save_data(obj, file_Name ):
    """ save an obj into a file using pickle """
    
    # open the file for writing
    with open(file_Name, 'wb') as file:
        # writes the object a to the file
        pickle.dump(obj, file)
   