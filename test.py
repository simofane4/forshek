from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, create_session
from models import ModelAnnonces


engine = create_engine('sqlite:///database.db')
Base = declarative_base()
session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = session()




field_titre = [r.titre for r in session.query(ModelAnnonces.titre)]
file_content = []
resultant_list = []
repeated_element_list = []




for line in field_titre:
    # This will strip('\n') and
    # split the line with spaces and stored as list
    temp = line.strip('\n').split(" ")
    for _ in temp:
        resultant_list.append(_)

print("\n debug resultant_list", resultant_list)

# Now this is the main for loop to 
# check the string with the adjacent string
for ii in range(0, len(resultant_list)):
    # is_repeated will check the element count is greater than 1. 
    # If so it will proceed with identifying duplicate logic
    is_repeated = resultant_list.count(resultant_list[ii])
    if is_repeated > 1:
        if ii not in repeated_element_list:
            for2count = ii + 1
            # This for loop for shifting the 
            # iterator to the adjacent string
            for jj in range(for2count, len(resultant_list)):
                if resultant_list[ii] == resultant_list[jj]:
                    repeated_element_list.append(resultant_list[ii])

print("The repeated strings are {}\n and total counts {}".format(
    repeated_element_list, len(repeated_element_list)))


session.close()
