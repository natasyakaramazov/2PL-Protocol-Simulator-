'''
Kierra Ashford 1002018597
Tsebaot Meron  1001629719
'''
from re import U
import sys

UTimestamp = 1
Transactions = [None,None,None,None,None,None,None,None,None]
LockTableob= []
transCount =0
WaitingQueue = []

#we need to create a locktable and a transaction table 
class Transaction:
    def __init__(self,transID,timestamp,status):
        self.transID=transID
        self.timestamp=timestamp
        self.status=status
        self.lockedDitems=[] # X,Y,Z
        self.OPitems=[] #r1(x), w1(x)

    def setlockData(self,DataItem):
        self.lockedDitems.append(DataItem)
    def setOP(self,op):
        self.OPitems.append(op)

class LockTb:
    def __init__(self,LdataItem,transID,state):
        self.transID=transID  #t1
        self.LdataItem=LdataItem #x
        self.state=state #readLock
        self.lockeditems=[]



def begin(op,transID):
    #timestamp=int(len(Transactions))+1
    Transactions[transID-1] = Transaction(transID,0,"Active")
    global UTimestamp
    Transactions[transID-1].timestamp =   UTimestamp
    UTimestamp = UTimestamp +1
    #print(Transactions[transID-1].timestamp)
    print(op.strip() + " T" +str(transID) + "  begins.TS=" + str(transID) + "  state=Active")
  



def end(transID):
    if Transactions[transID-1].status =="abort":
        print("Transaction " + str(transID) + " has already been aborted")
    
        #Ending the transaction means it has to be removed from the waiting queue
        #if previously blocked
        
        
    
    else:
        commit(transID)



def abort(transId):
    Transactions[transId-1].status="abort"
    print("Transaction " + str(transId) + " is aborted due to wait-die ")
    unlock(transId)

    
    if len(WaitingQueue) !=0:   
            temp =  WaitingQueue.pop(0)
            Transactions[temp.transID-1].status = "Active"
           # print("Transaction " + str(temp.transID) + " is released from the waiting queue")
            fixit(temp.transID)

def fixit (transId):
    index = None
    for i in range (len(Transactions[transId-1].OPitems)):#for loop removes l
        if (Transactions[transId-1].OPitems[i]).find('l') != -1: #Looks through operation list for blocked ops
            if index== None:
                    index = i
                    
                    
            Transactions[transId-1].OPitems[i]= Transactions[transId-1].OPitems[i].replace('l',' ')
                
                

    if index != None:
        for j in range (index,len((Transactions[transId-1].OPitems))):#sends operations through again to be completed
            CheckOp(Transactions[transId-1].OPitems[j])
            #print(Transactions[transId-1].OPitems[index])         
                        
     
def commit(transID):
    Transactions[transID-1].status="commmit"
     
    print("Transaction " + str(transID) + " is committed ")
    unlock(transID)
    if len(WaitingQueue) !=0:   
            temp =  WaitingQueue.pop(0)
            Transactions[temp.transID-1].status = "Active"
            print("Transaction " + str(temp.transID) + " is released from the waiting queue")
            fixit(temp.transID)
   



def wait(transID):
     WaitingQueue.append(Transactions[transID-1])
     print("Transaction "+ str(transID) +  " is blocked/waiting due to wait-die")
     Transactions[transID-1].status = "block"



def wait_die(transId, conflict):
        if Transactions[transId-1].timestamp < Transactions[conflict-1].timestamp:
                return 1  #indicates that the first transaction in the comparison is older, so it is allowed to wait
        else: 
             return 0   #indicates that the first transaction compared is younger, so abort the transaction
    


def readLock(dataItem,transId):

    #print("Read lock started on " + dataItem)
    #so here we have to check if the dataitem is free transcount=0 
    #or if it is in use for a read or write lock
    #so if it is in conflict we show the right message 
    #if not we add it to our lock table for the first time 

    used=0 
    downgradable = 0
    conflict = 0
    iteration = 0 #this is to check if the data item comes in 
            #as having already been used 
   
            #its not been used so add it to the lock table
            #LockTableob.append(LockTb(dataItem,transId,"readLock"))
    length = len(LockTableob)
    
    if(length  != 0):
        while(iteration!=2):
            for l in LockTableob:
               
               if Transactions[transId-1].status != "abort" and Transactions[transId-1].status!="block":
                if l.transID == transId and dataItem == l.LdataItem and downgradable==0 and iteration ==0:
                            downgradable = 1
                if dataItem == l.LdataItem and  l.transID != transId and l.state == "write-locked" and conflict == 0 and iteration == 0:
                        conflict = 1
                if l.transID == transId and dataItem == l.LdataItem and downgradable == 1 and iteration ==1:    #KA -> T1, has a write lock on X and read lock is attempting to access X on T1
                    if l.state =="write-locked":
                            l.state = "read-locked"
                            print("Transaction "+ str(transId) + " has been downgraded  from write lock to read locked on data item " + dataItem)

                            break
                elif dataItem == l.LdataItem and l.transID!= transId and l.state =="write-locked" and conflict == 1 and iteration ==1:   #KA -> T1 has a lock of some type on X, and T2 has a lock of some type on X, call wait_die
                                determinant = wait_die(transId, l.transID)
                                if determinant == 0:
                                    abort(transId)
                                    break
                                else:
                                        wait(transId) 
                                        Transactions[transId-1].OPitems.append("lr"+ str(transId) + "("+ dataItem +");\n") 
                                        break
                elif dataItem == l.LdataItem and l.transID!= transId and l.state =="read-locked" and conflict == 0 and downgradable == 0 and iteration == 0: 
                            LockTableob.append(LockTb(dataItem,transId,"read-locked"))
                            print(str(dataItem) + " is read locked by T" + str(transId))
                            #print("iteration  = " + str(iteration))
                            iteration =1
                            break
       
                elif dataItem!= l.LdataItem and conflict == 0 and iteration == 0 and downgradable == 0:  #KA -> T1 is not in the LockTableob list, therefore has no lock, create new lock instance 
                        
                        LockTableob.append(LockTb(dataItem,transId,"read-locked"))
                        print(str(dataItem) + " is read locked by T" + str(transId))
                        #if Transactions[transId-1].lockedDitems.find(dataItem) ==-1:
                             # Transactions[transId-1].setlockData(dataItem)
                        break
                else:
                     pass
            iteration = iteration +1
    else:
            LockTableob.append(LockTb(dataItem,transId,"read-locked"))
            Transactions[transId-1].setlockData(dataItem)
            print(str(dataItem) + " is read locked by T" + str(transId) )
            #print("Read Locked -> successful")
            #print(LockTableob[0].state)
            #for i in length:
            # if LockTableob[i].LdataItem == dataItem:
                # used = 1 #set it to one if the item is in use
                    #now we check for if 

def writeLock(dataItem, transId):
    
    
    upgradgable = 0
    conflict = 0

    iteration = 0
    length = len(LockTableob)
    
    if length !=0 :
        while(iteration!=2):

            for l in LockTableob:
                    if Transactions[transId-1].status != "abort" and Transactions[transId-1].status != "blocked":
                        if transId == l.transID and dataItem == l.LdataItem and upgradgable == 0 and iteration == 0:
                                upgradgable = 1
                                #print("found possible upgrade")
                        if dataItem == l.LdataItem and l.transID != transId and conflict == 0 and iteration == 0:
                                conflict = 1
                                #print("found possible conflict")
                        if transId == l.transID and dataItem == l.LdataItem and upgradgable == 1 and conflict ==0 and iteration == 1: #W1 X - >  1== 1 and If  ==X
            
                            if l.state == "read-locked":
                                l.state = "write-locked"
                                print("T" + str(transId) + " has been upgraded from read locked to write locked on data item "+ dataItem)
                               # print(l.state + " on" + str(l.transID) )
                                break
                            
                        elif dataItem == l.LdataItem and l.transID!= transId and conflict == 1 and iteration == 1:
                                
                                
                            # print(l.LdataItem + " " + l.transID)  #X  and 3
                                            #call wait_die, conflict found
                                determinant =  wait_die(transId,l.transID) 
                                if determinant == 0:
                                    abort(transId)
                                    break
                                else:
                                    wait(transId) 
                                    Transactions[transId-1].OPitems.append("lw"+ str(transId) + "("+ dataItem +");\n") 
                                    break

                        elif dataItem!= l.LdataItem and conflict == 0 and upgradgable == 0 and iteration == 1:
                        
                        
                            LockTableob.append(LockTb(dataItem,transId,"write-locked"))
                            print(str(dataItem) + " is write locked by T" + str(transId))
                            #if Transactions[transId-1].lockedDitems.find(dataItem) ==-1:
                                #Transactions[transId-1].setlockData(dataItem)
                            break
                        
                        else:
                            pass

            iteration = iteration + 1               
                            
    else: 
         LockTableob.append(LockTb(dataItem,transId,"write-locked"))
         Transactions[transId-1].setlockData(dataItem)
         print(str(dataItem) + " is write locked by T" + str(transId) )
         #print("Write lock successful")
def unlock(transId):
       #Transactions[transId-1].lockedDitems.clear()
      found = 0
      for l in LockTableob:
           
            if transId == l.transID:
                 found = found + 1
      while(found != 0):
       for l in LockTableob:
            

            if l.transID == transId:
            
                 #print(l.state + " removed on " + l.LdataItem + " for transaction" + str(l.transID))
                 LockTableob.remove(l) 
                 found = found - 1

                             
            

               
       
            #print(str(l.transID) + "still here")
def read(dataItem,transId):
     pass


def write(dataItem,transId):
   pass




def CheckOp(op):
    #is digit checks if there is numbers in the string 
    #returns true or fialse but we can save the character 
    #in a variable to use it 
    print(op)
    id=""
    dataItem = ""
    for m in op:
        if m.isdigit():
           id=int(id+m)
    #print("id ="+str(id))
    if op.find("X")!=-1:
        dataItem='X'
        #print(dataItem)
    if op.find("Y")!=-1:
         dataItem='Y'
        # print(dataItem)
    if op.find("Z")!=-1:
        dataItem='Z'
       # print(dataItem)
        #print("this is z")
    #KA -> we might have to change the above chunk of code to work for any uppercase letter
    #but it can wait till the end because it's probably only a few points off
    
    if op.find('b') != -1:
           
        begin(op,id)

    if op.find('r') != -1:
        Transactions[id-1].setOP(op)  
        if Transactions[id-1].status != "block"and Transactions[id-1].status!="abort":
            readLock(dataItem,id)
           
        #KA -> adds the read to the list of operations so that if it is blocked,
        # we can reference the last attempted operation
        #once unlocked
        
            read(dataItem,id)

    if op.find('w')!= -1:
       
         Transactions[id-1].setOP(op)
         if Transactions[id-1].status != "block" and Transactions[id-1].status!="abort":  
              writeLock(dataItem,id)
              write(dataItem,id)# KA -> only comples write if Transaction is not blocked
             
    if op.find('e')!=-1:
        Transactions[id-1].setOP(op)
        if Transactions[id-1].status != "block": 
             end(id)
            
        else:
             Transactions[id-1].OPitems.append("l"+ op)   
             print("T" +str(id) + "is going to be committed soon")          



def main():
    a=[]  
   
    with open(sys.argv[1],'r')as line:
    #a=line.read()
        for i in line:
            # a=line.read()
            a.append(i)
        for j in a:
            CheckOp(j)
        for t in Transactions:
                if t!=None:
                    print("T"+str(t.transID)+" is "+ t.status + "ed")
    #print(Transactions[0].OPitems)
if __name__ == "__main__":
     main()
    #print(a)