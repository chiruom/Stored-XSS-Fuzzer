import anydbm

            
if __name__ == '__main__':
    fout=open(r'.\html.txt','w')
    db = anydbm.open('html', 'r')  
    for c in db: 
        fout.write(c)
        fout.write("\r\n")
        fout.write(db[c])
        fout.write("\r\n__________________________________________________\r\n")
    db.close()
    fout.flush()
    fout.close()
    #raw_input("Press Enter to continue: ")
