import json

def cleanStr4SQL(s):
  return s.replace("'","''").replace("\n"," ")

def getAttributes(attributes):
  L = []
  for (attribute, value) in list(attributes.items()):
      if isinstance(value, dict):
          L += getAttributes(value)
      else:
          L.append((attribute,value))
  return L


def parseBusinessData():
  print("Parsing businesses...")
  # opens the business json file in read mode
  with open('Yelp_JSONs/yelp_business.JSON', 'r') as f:
      # opens/creates 'yelp_business.txt' file for writing
      outfile = open('yelp_business.txt', 'w')
      # count our lines
      count_line = 0
      # for each line in file
      for line in f:
          # load the line into a dictionary data
          data = json.loads(line)
          # business string looks for values using keys
          # use cleanStr4SQL on strings, numbers do not need this
          businessStr = (
              # key = business_id
              f"'{cleanStr4SQL(data['business_id'])}',"
              # key = name
              f"'{cleanStr4SQL(data['name'])}',"
              f"'{cleanStr4SQL(data['address'])}',"
              f"'{cleanStr4SQL(data['city'])}',"
              f"'{data['state']}',"
              f"'{data['postal_code']}',"
              f"{data['latitude']},"
              f"{data['longitude']},"
              f"{data['stars']},"
              f"{data['review_count']},"
              f"{data['is_open']}"
          )

          # write our string out to 'yelp_business.txt'
          outfile.write(businessStr + '\n')
        
          # go through each catagory in our dict
          for category in data['categories']:
              # print the category along with the business ID
              category_str = f"'{data['business_id']}', '{category}'"
              outfile.write(category_str + '\n')
            
          # for each day, and hour
          for day, hours in data['hours'].items():
              # create a hour string that
              hours_str = (
                  # grabs our business ID
                  f"'{data['business_id']}',"
                  # the day
                  f"'{day}',"
                  # split into two parts ex: 9:00-12:00
                  # opening hours
                  f"'{hours.split('-')[0]}',"
                  # closing hours
                  f"'{hours.split('-')[1]}'"
              )

              # write this info to our txt
              outfile.write(hours_str + '\n')

          # iterates over the items of the 'attributes' dictionary
          for attr, value in data['attributes'].items():
              # checks if the value associated with the current attribute is a dictionary
              if isinstance(value, dict):
                  # iterates over its items, assigning each sub-attribute and its corresponding sub-value
                  for sub_attr, sub_value in value.items():
                      attrStr = (
                          f"'{data['business_id']}',"
                          f"'{attr} - {sub_attr}',"
                          f"'{sub_value}'"
                      )

                      # write this info to our txt
                      outfile.write(attrStr + '\n')
              # value is a simple value like a string or number
              else:
                  attrStr = (
                      f"'{data['business_id']}',"
                      f"'{attr}',"
                      f"'{value}'"
                  )

                  # write this info to our txt
                  outfile.write(attrStr + '\n')
          # increment our line count
          count_line +=1

  # print our line count
  print(count_line)
  # close our outfile
  outfile.close()
  # close f
  f.close()

def parseReviewData():
  print("Parsing reviews...")
  # opens the user json file in read mode
  with open('Yelp_JSONs/yelp_review.JSON', 'r') as f:
      # opens/creates 'yelp_review.txt' file for writing
      outfile = open('yelp_review.txt', 'w')
      # count our lines
      count_line = 0
      # for each line in file
      for line in f:
          # load the line into a dictionary data
          data = json.loads(line)
          # review string looks for values using keys
          reviewStr = (
              f"'{data['review_id']}',"
              f"'{data['user_id']}',"
              f"'{data['business_id']}',"
              f"'{str(data['stars'])}',"
              f"'{data['date']}',"
              f"'{cleanStr4SQL(data['text'])}',"
              f"'{str(data['useful'])}',"
              f"'{str(data['funny'])}',"
              f"'{str(data['cool'])}',"
          )
          # write our string out to 'yelp_business.txt'
          outfile.write(reviewStr +'\n')
          # increment our line count
          count_line +=1

  # print our line count
  print(count_line)
  # close our outfile
  outfile.close()
  # close f
  f.close()

def parseUserData():
  print("Parsing users...")
  with open('Yelp_JSONs/yelp_user.JSON','r') as f:
      outfile =  open('yelp_user.txt', 'w')
      # count our lines
      count_line = 0
      # for each line in file
      for line in f:
          # load the line into a dictionary data
          data = json.loads(line)
          # user string looks for values using keys
          usrStr = (
              f"'{data['user_id']}',"
              f"'{cleanStr4SQL(data["name"])}',"
              f"'{cleanStr4SQL(data["yelping_since"])}',"
              f"'{str(data["review_count"])}',"
              f"'{str(data["fans"])}',"
              f"'{str(data["average_stars"])}',"
              f"'{str(data["funny"])}',"
              f"'{str(data["useful"])}',"
              f"'{str(data["cool"])}',"
          )
          # write our string out to 'yelp_user.txt'
          outfile.write(usrStr + '\n')

          for friend in data["friends"]:
              friendStr = f"'{data['user_id']}', '{friend}'"
              outfile.write(friendStr)
              # write our string out to 'yelp_user.txt'
              outfile.write(friendStr +'\n')
          # increment our line count
          count_line +=1

  # print our line count
  print(count_line)
  # close our outfile
  outfile.close()
  # close f
  f.close()

def parseCheckinData():
  print("Parsing checkins...")
  with open('Yelp_JSONs/yelp_checkin.JSON','r') as f:
      outfile =  open('yelp_checkin.txt', 'w')
      # count our lines
      count_line = 0
      # for each line in file
      for line in f:
          # load the line into a dictionary data
          data = json.loads(line)
          # find times for checkin
          for dayofweek, time in data['time'].items():
              for hour, count in time.items():
                  # user string looks for values using keys
                  checkinStr = (
                      f"'{data['business_id']}',"
                      f"'{dayofweek}',"
                      f"'{hour}',"
                      f"'{str(count)}',"
                  )
                  # write our string out to 'yelp_checkin.txt'
                  outfile.write(checkinStr + "\n")
          # increment our line count
          count_line +=1

  # print our line count
  print(count_line)
  # close our outfile
  outfile.close()
  # close f
  f.close()

parseBusinessData()
parseUserData()
parseCheckinData()
parseReviewData()