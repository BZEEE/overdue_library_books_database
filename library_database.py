from datetime import date

def main():
    #set date to compare overdue books to 
    today = date(2018,1,19)
    
    #total cost of all overdue fees
    totalCost = 0
    
    #create a dictionary of members who are referenced through their phone numbers
    membersDict = {}
    #create a dictionary of members who are referenced through their books they signed out 
    booksDict = {}
    #create a final dictionary with just the overdue members from the original members dictionary
    overdueMembers = {}
    
    #Open files of members and books in read mode
    membersOpened = open('members.txt', 'r')
    booksOpened = open('books.txt', 'r')
    
    # convert each line of text into items in the list
    membersFile = membersOpened.read().splitlines()
    booksFile = booksOpened.read().splitlines()
    
    # split items into key value pairs and append to dictionaries, key is the phone numbers, values are name and address
    for member in membersFile:
        items = member.split(',', 1)
        membersDict[items[0]] = items[1]
        
    for book in booksFile:
        #The list items contains the book ID in position[0] and the rest of the info in position[1]
        items = book.split(';', 1)
        
        #append books to dictionary, key is the book ID, values are the rest ofthe information
        booksDict[items[0]] = items[1]
        
        dueDate = items[1].split(';')[1]
        bookPrice = items[1].split(';')[0]
        #convert to datetime type
        dueDate = date( int(dueDate[:4]), int(dueDate[5:7]), int(dueDate[8:]))
        # nbDays is the number of days that book is overdue
        nbDays = (today - dueDate).days
        
        #calculate penalty cost based on overdue days
        #only append members with overdue books to overdueMembers dictionary
        if nbDays > 0:
            phoneNumber = items[1].split(';')[2]
            memberName = membersDict[phoneNumber].split(',')[0]
            
            #extra penalty if book is overdue for more than 90 days
            if nbDays > 90:
                penaltyCost = (0.25*nbDays) + float(bookPrice)
            else:
                penaltyCost = nbDays*0.25
            
            #if member has more than one overdue book, this appends just the new overdue book to their name in the dictionary and keeps track of charging the member for all overdue books
            if phoneNumber in overdueMembers:
                overdueMembers[phoneNumber] += ' [%s](%i days);' % (items[0],nbDays)
                split = overdueMembers[phoneNumber].split(',')
                newPenalty = float(split[1])+penaltyCost
                overdueMembers[phoneNumber] = '%s,%f,%s' % (split[0], newPenalty, split[2])
                                 
                  
            #adds member to overdue dictionary if they are not already in it   
            else:
                overdueMembers[phoneNumber] = '%s,%.2f,[%s](%i days);' % (memberName,penaltyCost,items[0],nbDays)
                
            # total cost of all over due books
            totalCost += penaltyCost
            
            
    #generate text file for overdue members
    summaryFile = open('summary.txt', 'w')
    
    #top format of table
    summaryFile.write('+%s+%s+%s+\n' % ('-'*14, '-'*30, '-'*8))
    summaryFile.write('|%-14s|%-30s|%-8s|\n' % (' Phone Number', ' Name', ' Due'))
    summaryFile.write('+%s+%s+%s+\n' % ('-'*14, '-'*30, '-'*8))
            
    #prints all member in the overdueMembers Dictionary        
    for member in overdueMembers:
        #put phone number in proper format for table
        phoneNumber = '(%s) %s %s' % (member[:3], member[3:6], member[6:])            
        memberName = overdueMembers[member].split(',')[0]
        penaltyCost = float(overdueMembers[member].split(',')[1])
        overdueBooks = overdueMembers[member].split(',')[2]
        summaryFile.write('|%-14s|%-30s|$%7.2f|%s\n' % (phoneNumber, memberName, penaltyCost, overdueBooks))
    
    #bottom of table
    summaryFile.write('+%s+%s+%s+\n' % ('-'*14, '-'*30, '-'*8))
    summaryFile.write('|%-14s|%30s|%8.2f|\n' % (' Total Dues','$ ', totalCost))
    summaryFile.write('+%s+%s+%s+\n' % ('-'*14, '-'*30, '-'*8))
    
    #close files
    membersOpened.close()
    booksOpened.close()
    summaryFile.close()
    
    # open file again and print it to see contents
    file = open('summary.txt', 'r')
    print(file.read())
    file.close()

main()